#!/usr/bin/env python3
"""
Setup script for the OpenAPI to MCP Generator package.
"""

from setuptools import setup, find_packages

setup(
    name="openapi-mcp-generator",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,  # This should make it read MANIFEST.in
    install_requires=[
        "pyyaml>=6.0",
        "jinja2>=3.1.2",
        "httpx>=0.24.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-generator=openapi_mcp_generator.cli:main",
        ],
    },
)
