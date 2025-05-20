# OpenAPI Reference and `oneOf` Test Case

This example provides an OpenAPI specification (`openapi.yaml`) specifically designed to test the generator's handling of:
- Parameter definitions using `$ref` to shared components.
- Schema definitions using `oneOf` for alternative structures.

This test case helps ensure the `openapi-mcp-generator` correctly parses these constructs and generates functional MCP server code.

## Setup and Testing Instructions

1.  **Navigate to the root directory** of the `openapi-mcp-generator` project.

2.  **Generate the MCP server** using the `openapi.yaml` from this test case. You can specify an output directory, for example, within the `tests/oneOftestcase/` directory:

    ```bash
    python generator.py \
      samples/oneOftestcase/openapi.yaml \
      --output-dir ./tests/oneOftestcase/ \
      --api-url http://localhost:8000/api \
      --api-token "test-token"
    ```

    *   The `openapi.yaml` file used is [samples/oneOftestcase/openapi.yaml](samples/oneOftestcase/openapi.yaml).
    *   The generator script is [generator.py](../../generator.py).
    *   The output will be a new directory, e.g., `./tests/oneOftestcase/openapi-mcp-reference-test-api-xxxxxxx/` (where `xxxxxxx` is a unique ID).

3.  **Inspect the generated server code**, particularly the `mcp_server.py` file within the newly created output directory.
    *   Verify that the tool definitions correctly resolve `$ref` parameters (e.g., `id: int`, `verbose: bool` for the `getItems` tool).
    *   Check the resource definitions for schemas like `BadRequestDetails` to see how `oneOf` is represented (it will be dumped as YAML).

4.  **Build and run the Docker container** for the generated server:

    ```bash
    cd ./tests/oneOftestcase/openapi-mcp-reference-test-api-xxxxxxx/ 
    ./docker.sh build
    ./docker.sh start --transport=sse
    ```
    *(Replace `openapi-mcp-reference-test-api-xxxxxxx` with the actual generated directory name)*

## Key Aspects Tested

-   **Parameter Referencing (`$ref`)**: The `/items` path in [samples/oneOftestcase/openapi.yaml](samples/oneOftestcase/openapi.yaml) uses `parameters` with `$ref` to point to definitions in `components/parameters`. The generator should resolve these references to include the correct parameter names and types in the generated tool function signature.
-   **Schema `oneOf`**: The `BadRequestDetails` schema in `components/schemas` uses `oneOf` to indicate that the `details` property can be either a string or a reference to `ErrorModel`. The [`generate_resource_definitions`](../../generator.py) function should include this structure in the generated resource.

## Verification

-   After running the generator, open the generated `mcp_server.py` file.
-   Locate the `getItems` tool definition. Its signature should reflect the resolved parameters: `async def getItems(id: int, verbose: bool, limit: int, ctx: Context) -> str:`.
-   Locate the `get_BadRequestDetails_schema` resource definition. The returned YAML string should include the `oneOf` structure for the `details` property.
-   Running the server in Docker and attempting to interact with the tools (if a live API backend matching the spec were available) would further confirm runtime correctness. For this specific test case, static code inspection is the primary verification method.