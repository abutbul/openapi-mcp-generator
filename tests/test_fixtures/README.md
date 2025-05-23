# Test Fixtures

This directory contains JSON fixtures used for testing the generated API server code.

Each JSON file corresponds to the expected output of a method in the generated server:

- `api_info.json`: Expected output from `get_api_info()`
- `bad_request_details_schema.json`: Expected schema for BadRequestDetails
- `error_model_schema.json`: Expected schema for ErrorModel
- `data_returned_schema.json`: Expected schema for DataReturned

These fixtures are sanitized representations of the original schemas and are used to verify the correctness of the generated code.
