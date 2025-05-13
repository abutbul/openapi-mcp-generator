---
name: Bug report
about: Create a report to help us improve the OpenAPI to MCP Server Generator
title: ''
labels: 'bug'
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is. Is it related to:
- Generator functionality
- Generated MCP server
- Docker container
- API communication
- Other

**OpenAPI Specification**
Provide details about your OpenAPI spec:
- Path to spec file: [e.g. ./api/openapi.yaml]
- API version: [e.g. 3.0.0]
- Link to spec (if public):

**To Reproduce**
Steps to reproduce the behavior:
1. Generator command run: [e.g. `python generator.py openapi.yaml --output-dir ./output`]
2. Generated project location: [e.g. ./output/openapi-mcp-example-abc123]
3. Any modifications made to generated files
4. Steps that triggered the issue:
   - Docker commands run
   - API calls made
   - Error messages received

**Expected behavior**
A clear and concise description of what you expected to happen.

**Actual behavior**
What actually happened, including any error messages, stack traces, or logs.

**Environment (please complete the following information):**
 - OS: [e.g. Ubuntu 22.04, macOS 13.0]
 - Python version: [e.g. 3.10.4]
 - Docker version: [e.g. 24.0.5]
 - Generator version/commit: [e.g. main branch, commit abc123]

**Configuration**
- Authentication type used: [bearer/token/basic]
- Transport protocol: [SSE/IO]
- Other relevant settings:

**Logs**
<details>
<summary>Generator Logs</summary>

```
Paste generator logs here
```
</details>

<details>
<summary>Docker Logs</summary>

```
Paste docker logs here (if applicable)
```
</details>

<details>
<summary>MCP Server Logs</summary>

```
Paste MCP server logs here (if applicable)
```
</details>

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Additional context**
- Any workarounds attempted
- Related issues
- Additional context that might be helpful