# OpenAPI MCP Generator Test Suite

This directory contains comprehensive test cases for the `openapi-mcp-generator` project, ensuring it correctly handles various OpenAPI specification formats and generates functional MCP servers.

## Test Coverage

The test suite validates the generator's ability to:
- **Parse OpenAPI YAML specifications** with complex structures
- **Handle JSON specification directories** containing multiple API definitions  
- **Resolve `$ref` references** to shared components (parameters, schemas, responses)
- **Process `oneOf` constructs** for alternative schema structures
- **Generate working MCP servers** from different input formats
- **Create appropriate tools and resources** for each API specification

## Test Structure

### Input Formats Tested

1. **Single OpenAPI YAML File** (`openapi.yaml`)
   - Tests `$ref` parameter resolution
   - Tests `oneOf` schema constructs
   - Generates: `openapi-mcp-reference-test-api-*` directories

2. **JSON Specification Directory** (`test_fixtures/`)
   - Tests multi-file JSON API specifications
   - Tests directory-based generation
   - Generates: `openapi-mcp-generated-api-from-json-specifications-*` directories

### Test Files

- `test_generated_server.py` - Automated tests for generated servers
- `test_fixtures/` - JSON specification files and test data
- `openapi.yaml` - Reference OpenAPI specification for testing
- `out/` - Generated MCP server output directory

## Setup and Testing Instructions

### Running the Full Test Suite

1. **Navigate to the root directory** of the `openapi-mcp-generator` project.

2. **Generate both types of MCP servers** for comprehensive testing:

   **From OpenAPI YAML:**
   ```bash
   python generator.py \
     tests/openapi.yaml \
     --output-dir ./tests/out/ \
     --api-url http://localhost:8000/api \
     --api-token "test-token"
   ```

   **From JSON Specifications Directory:**
   ```bash
   python generator.py \
     tests/test_fixtures/ \
     --output-dir ./tests/out/ \
     --api-url http://localhost:8000/api \
     --api-token "test-token"
   ```

3. **Run the automated test suite:**
   ```bash
   pytest tests/test_generated_server.py -v
   ```

   The tests will automatically detect and validate both generated servers:
   - Tests for `openapi-mcp-reference-test-api-*`: Full schema validation
   - Tests for `openapi-mcp-generated-api-from-json-specifications-*`: API info validation

### Manual Verification

4. **Inspect the generated server code** in the `tests/out/` directory:
   - `openapi-mcp-reference-test-api-*/mcp_server.py` - YAML-generated server
   - `openapi-mcp-generated-api-from-json-specifications-*/mcp_server.py` - JSON-generated server

5. **Build and run Docker containers** for either generated server:
   ```bash
   cd ./tests/out/[generated-directory-name]/
   ./docker.sh build
   ./docker.sh start --transport=sse
   ```

## Test Cases in Detail

### 1. OpenAPI YAML Test Case (`openapi.yaml`)

This test case specifically validates:

**Parameter Referencing (`$ref`)**: 
- The `/items` endpoint uses `$ref` to reference shared parameter definitions
- Generator resolves references to include correct parameter names and types
- Expected tool signature: `async def getItems(id: int, verbose: bool, limit: int, ctx: Context) -> str:`

**Schema `oneOf` Constructs**:
- The `BadRequestDetails` schema uses `oneOf` for the `details` property
- Can be either a string or a reference to `ErrorModel`
- Generator includes this structure in resource definitions

**Response References**:
- Uses `$ref` for response definitions in `components/responses`
- Tests proper resolution of response schemas

### 2. JSON Specifications Test Case (`test_fixtures/`)

This test case validates:

**Multi-file JSON Processing**:
- Processes multiple JSON specification files in a directory
- Combines specifications into a single generated server
- Handles different API structures and naming conventions

**Directory-based Generation**:
- Tests the generator's ability to work with directory inputs
- Validates proper file discovery and parsing
- Ensures consistent output structure

## Automated Test Details

The `test_generated_server.py` file implements parametrized tests that:

1. **Detect Available Servers**: Automatically finds generated servers in `tests/out/`
2. **Adaptive Testing**: Runs appropriate tests based on server type:
   - **YAML servers**: Full validation including schema functions
   - **JSON servers**: API info validation, skips unavailable schema functions
3. **Comprehensive Coverage**: Tests API info, schema resources, and tool availability
4. **Clear Reporting**: Uses descriptive test names showing which server is being tested

### Test Output Example
```
test_get_api_info[openapi-mcp-reference-test-api-207c6a52] PASSED
test_get_api_info[openapi-mcp-generated-api-from-json-specifications-320a71cd] PASSED
test_get_BadRequestDetails_schema[openapi-mcp-reference-test-api-207c6a52] PASSED
test_get_BadRequestDetails_schema[openapi-mcp-generated-api-from-json-specifications-320a71cd] SKIPPED
```

## Verification

### Generated Code Verification

**For YAML-generated servers** (`openapi-mcp-reference-test-api-*`):
- ✅ Tool definitions correctly resolve `$ref` parameters
- ✅ Schema resources include `oneOf` structures  
- ✅ Resource functions available: `get_BadRequestDetails_schema`, `get_ErrorModel_schema`, `get_DataReturned_schema`
- ✅ API info matches OpenAPI specification

**For JSON-generated servers** (`openapi-mcp-generated-api-from-json-specifications-*`):
- ✅ API info reflects combined JSON specifications
- ✅ Tools generated from multiple specification files
- ✅ Proper naming and organization of generated content

### CI/CD Integration

The test suite is integrated into the GitHub Actions workflow (`../.github/workflows/generate-and-test.yml`) which:

1. **Generates both server types** during CI runs
2. **Runs comprehensive tests** against all generated servers
3. **Validates multiple generation methods**:
   - Direct script execution (`python generator.py`)
   - CLI tool usage (`mcp-generator`)
   - Python module execution (`python -m openapi_mcp_generator.cli`)
4. **Ensures cross-platform compatibility** and consistent behavior

### Manual Testing

For runtime verification with live API backends:
1. Deploy the generated server using Docker
2. Configure MCP client to connect to the server
3. Test tool invocation and response handling
4. Verify resource access and schema validation

This comprehensive test suite ensures the `openapi-mcp-generator` reliably produces functional MCP servers from diverse OpenAPI specifications.