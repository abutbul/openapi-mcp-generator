#!/usr/bin/env python3
"""
MCP Server Implementation for ETAPI

This MCP server exposes the API operations defined in the OpenAPI specification
as MCP tools and resources.
"""

import os
import argparse
import logging
import httpx
from typing import Dict, List, Any, Optional, Union
from mcp.server.fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP(name=os.environ.get("MCP_SERVER_NAME", "ETAPI API"))

# API configuration
API_URL = os.environ.get("API_URL", "http://localhost:8021")
API_TOKEN = os.environ.get("API_TOKEN", "")
API_AUTH_TYPE = os.environ.get("API_AUTH_TYPE", "bearer")
API_USERNAME = os.environ.get("API_USERNAME", "")
API_PASSWORD = os.environ.get("API_PASSWORD", "")

# Async HTTP client for API calls
async def get_http_client():
    """Create and configure the HTTP client with appropriate authentication."""
    headers = {}
    
    if API_AUTH_TYPE == "bearer":
        headers["Authorization"] = f"Bearer {API_TOKEN}"
    elif API_AUTH_TYPE == "token":
        headers["Authorization"] = API_TOKEN
    
    return httpx.AsyncClient(
        base_url=API_URL,
        headers=headers,
        auth=(API_USERNAME, API_PASSWORD) if API_AUTH_TYPE == "basic" else None
    )

# MCP tools for API operations

@mcp.tool(description="Create a note and place it into the note tree")
async def createNote(ctx: Context) -> str:
    """
    Create a note and place it into the note tree
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/create-note"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.post(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Search notes")
async def searchNotes(search: str, fastSearch: bool, includeArchivedNotes: bool, ancestorNoteId: str, ancestorDepth: str, orderBy: str, orderDirection: str, limit: int, debug: bool, ctx: Context) -> str:
    """
    Search notes
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/notes"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Returns a note identified by its ID")
async def getNoteById(ctx: Context) -> str:
    """
    Returns a note identified by its ID
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/notes/{noteId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="patch a note identified by the noteId with changes in the body")
async def patchNoteById(ctx: Context) -> str:
    """
    patch a note identified by the noteId with changes in the body
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/notes/{noteId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.patch(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="deletes a single note based on the noteId supplied")
async def deleteNoteById(ctx: Context) -> str:
    """
    deletes a single note based on the noteId supplied
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/notes/{noteId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.delete(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Returns note content identified by its ID")
async def getNoteContent(ctx: Context) -> str:
    """
    Returns note content identified by its ID
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/notes/{noteId}/content"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Updates note content identified by its ID")
async def putNoteContentById(ctx: Context) -> str:
    """
    Updates note content identified by its ID
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/notes/{noteId}/content"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.put(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Exports ZIP file export of a given note subtree. To export whole document, use \"root\" for noteId")
async def exportNoteSubtree(ctx: Context) -> str:
    """
    Exports ZIP file export of a given note subtree. To export whole document, use \"root\" for noteId
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/notes/{noteId}/export"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Imports ZIP file into a given note.")
async def importZip(ctx: Context) -> str:
    """
    Imports ZIP file into a given note.
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/notes/{noteId}/import"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.post(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Create a note revision for the given note")
async def createRevision(ctx: Context) -> str:
    """
    Create a note revision for the given note
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/notes/{noteId}/revision"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.post(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Create a branch (clone a note to a different location in the tree). In case there is a branch between parent note and child note already,  then this will update the existing branch with prefix, notePosition and isExpanded. ")
async def postBranch(ctx: Context) -> str:
    """
    Create a branch (clone a note to a different location in the tree). In case there is a branch between parent note and child note already,  then this will update the existing branch with prefix, notePosition and isExpanded. 
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/branches"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.post(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Returns a branch identified by its ID")
async def getBranchById(ctx: Context) -> str:
    """
    Returns a branch identified by its ID
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/branches/{branchId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="patch a branch identified by the branchId with changes in the body. Only prefix and notePosition can be updated. If you want to update other properties, you need to delete the old branch and create a new one.")
async def patchBranchById(ctx: Context) -> str:
    """
    patch a branch identified by the branchId with changes in the body. Only prefix and notePosition can be updated. If you want to update other properties, you need to delete the old branch and create a new one.
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/branches/{branchId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.patch(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="deletes a branch based on the branchId supplied. If this is the last branch of the (child) note,  then the note is deleted as well. ")
async def deleteBranchById(ctx: Context) -> str:
    """
    deletes a branch based on the branchId supplied. If this is the last branch of the (child) note,  then the note is deleted as well. 
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/branches/{branchId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.delete(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="create an attachment")
async def postAttachment(ctx: Context) -> str:
    """
    create an attachment
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/attachments"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.post(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Returns an attachment identified by its ID")
async def getAttachmentById(ctx: Context) -> str:
    """
    Returns an attachment identified by its ID
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/attachments/{attachmentId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="patch an attachment identified by the attachmentId with changes in the body. Only role, mime, title, and position are patchable.")
async def patchAttachmentById(ctx: Context) -> str:
    """
    patch an attachment identified by the attachmentId with changes in the body. Only role, mime, title, and position are patchable.
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/attachments/{attachmentId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.patch(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="deletes an attachment based on the attachmentId supplied.")
async def deleteAttachmentById(ctx: Context) -> str:
    """
    deletes an attachment based on the attachmentId supplied.
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/attachments/{attachmentId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.delete(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Returns attachment content identified by its ID")
async def getAttachmentContent(ctx: Context) -> str:
    """
    Returns attachment content identified by its ID
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/attachments/{attachmentId}/content"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Updates attachment content identified by its ID")
async def putAttachmentContentById(ctx: Context) -> str:
    """
    Updates attachment content identified by its ID
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/attachments/{attachmentId}/content"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.put(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="create an attribute for a given note")
async def postAttribute(ctx: Context) -> str:
    """
    create an attribute for a given note
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/attributes"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.post(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Returns an attribute identified by its ID")
async def getAttributeById(ctx: Context) -> str:
    """
    Returns an attribute identified by its ID
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/attributes/{attributeId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="patch an attribute identified by the attributeId with changes in the body. For labels, only value and position can be updated. For relations, only position can be updated. If you want to modify other properties, you need to delete the old attribute and create a new one.")
async def patchAttributeById(ctx: Context) -> str:
    """
    patch an attribute identified by the attributeId with changes in the body. For labels, only value and position can be updated. For relations, only position can be updated. If you want to modify other properties, you need to delete the old attribute and create a new one.
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/attributes/{attributeId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.patch(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="deletes an attribute based on the attributeId supplied.")
async def deleteAttributeById(ctx: Context) -> str:
    """
    deletes an attribute based on the attributeId supplied.
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/attributes/{attributeId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.delete(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="notePositions in branches are not automatically pushed to connected clients and need a specific instruction.  If you want your changes to be in effect immediately, call this service after setting branches' notePosition.  Note that you need to supply \"parentNoteId\" of branch(es) with changed positions. ")
async def postRefreshNoteOrdering(ctx: Context) -> str:
    """
    notePositions in branches are not automatically pushed to connected clients and need a specific instruction.  If you want your changes to be in effect immediately, call this service after setting branches' notePosition.  Note that you need to supply \"parentNoteId\" of branch(es) with changed positions. 
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/refresh-note-ordering/{parentNoteId}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.post(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="returns an \"inbox\" note, into which note can be created. Date will be used depending on whether the inbox is a fixed note (identified with #inbox label) or a day note in a journal. ")
async def getInboxNote(date: str, ctx: Context) -> str:
    """
    returns an \"inbox\" note, into which note can be created. Date will be used depending on whether the inbox is a fixed note (identified with #inbox label) or a day note in a journal. 
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/inbox/{date}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="returns a day note for a given date. Gets created if doesn't exist.")
async def getDayNote(date: str, ctx: Context) -> str:
    """
    returns a day note for a given date. Gets created if doesn't exist.
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/calendar/days/{date}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="returns a week note for a given date. Gets created if doesn't exist.")
async def getWeekFirstDayNote(date: str, ctx: Context) -> str:
    """
    returns a week note for a given date. Gets created if doesn't exist.
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/calendar/weeks/{date}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="returns a week note for a given date. Gets created if doesn't exist.")
async def getMonthNote(month: str, ctx: Context) -> str:
    """
    returns a week note for a given date. Gets created if doesn't exist.
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/calendar/months/{month}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="returns a week note for a given date. Gets created if doesn't exist.")
async def getYearNote(year: str, ctx: Context) -> str:
    """
    returns a week note for a given date. Gets created if doesn't exist.
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/calendar/years/{year}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="get an ETAPI token based on password for further use with ETAPI")
async def login(ctx: Context) -> str:
    """
    get an ETAPI token based on password for further use with ETAPI
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/auth/login"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.post(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="logout (delete/deactivate) an ETAPI token")
async def logout(ctx: Context) -> str:
    """
    logout (delete/deactivate) an ETAPI token
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/auth/logout"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.post(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="returns information about the running Trilium instance")
async def getAppInfo(ctx: Context) -> str:
    """
    returns information about the running Trilium instance
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/app-info"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.get(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


@mcp.tool(description="Create a database backup under a given name")
async def createBackup(ctx: Context) -> str:
    """
    Create a database backup under a given name
    """
    async with await get_http_client() as client:
        try:
            # Build the URL with path parameters
            url = "/backup/{backupName}"
            
            # Extract query parameters
            query_params = {}
            # ... build query params from function args
            
            # Make the request
            response = await client.put(
                url,
                params=query_params,
                # Add other parameters as needed
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the response
            return str(response.text)
        
        except httpx.HTTPStatusError as e:
            return f"API Error: {e.response.status_code} - {e.response.text}"
        except Exception as e:
            return f"Error: {str(e)}"


# MCP resources

@mcp.resource("api://info")
def get_api_info() -> str:
    """
    Get API information
    """
    return f"""
    Title: ETAPI
    Version: 1.0.0
    Description: External Trilium API
    """


@mcp.resource("schema://CreateNoteDef")
def get_CreateNoteDef_schema() -> str:
    """
    Get the CreateNoteDef schema definition
    """
    return """
    properties:
  branchId:
    $ref: '#/components/schemas/EntityId'
    description: DON'T specify unless you want to force a specific branchId
  content:
    type: string
  dateCreated:
    $ref: '#/components/schemas/LocalDateTime'
    description: Local timestap of the note creation. Specify only if you want to
      override the default (current datetime in the current timezone/offset).
  isExpanded:
    description: true if this note (as a folder) should appear expanded
    type: boolean
  mime:
    description: this needs to be specified only for note types 'code', 'file', 'image'.
    example: application/json
    type: string
  noteId:
    $ref: '#/components/schemas/EntityId'
    description: DON'T specify unless you want to force a specific noteId
  notePosition:
    description: 'Position of the note in the parent. Normal ordering is 10, 20, 30
      ...  So if you want to create a note on the first position, use e.g. 5, for
      second position 15, for last e.g. 1000000

      '
    type: integer
  parentNoteId:
    $ref: '#/components/schemas/EntityId'
    description: Note ID of the parent note in the tree
  prefix:
    description: 'Prefix is branch (placement) specific title prefix for the note.  Let''s
      say you have your note placed into two different places in the tree,  but you
      want to change the title a bit in one of the placements. For this you can use
      prefix.

      '
    type: string
  title:
    type: string
  type:
    enum:
    - text
    - code
    - file
    - image
    - search
    - book
    - relationMap
    - render
    type: string
  utcDateCreated:
    $ref: '#/components/schemas/UtcDateTime'
    description: UTC timestap of the note creation. Specify only if you want to override
      the default (current datetime).
required:
- parentNoteId
- title
- type
- content
type: object

    """


@mcp.resource("schema://Note")
def get_Note_schema() -> str:
    """
    Get the Note schema definition
    """
    return """
    properties:
  attributes:
    $ref: '#/components/schemas/AttributeList'
    readOnly: true
  blobId:
    description: ID of the blob object which effectively serves as a content hash
    type: string
  childBranchIds:
    $ref: '#/components/schemas/EntityIdList'
    readOnly: true
  childNoteIds:
    $ref: '#/components/schemas/EntityIdList'
    readOnly: true
  dateCreated:
    $ref: '#/components/schemas/LocalDateTime'
  dateModified:
    $ref: '#/components/schemas/LocalDateTime'
    readOnly: true
  isProtected:
    readOnly: true
    type: boolean
  mime:
    type: string
  noteId:
    $ref: '#/components/schemas/EntityId'
    readOnly: true
  parentBranchIds:
    $ref: '#/components/schemas/EntityIdList'
    readOnly: true
  parentNoteIds:
    $ref: '#/components/schemas/EntityIdList'
    readOnly: true
  title:
    type: string
  type:
    enum:
    - text
    - code
    - render
    - file
    - image
    - search
    - relationMap
    - book
    - noteMap
    - mermaid
    - webView
    - shortcut
    - doc
    - contentWidget
    - launcher
    type: string
  utcDateCreated:
    $ref: '#/components/schemas/UtcDateTime'
  utcDateModified:
    $ref: '#/components/schemas/UtcDateTime'
    readOnly: true
type: object

    """


@mcp.resource("schema://Branch")
def get_Branch_schema() -> str:
    """
    Get the Branch schema definition
    """
    return """
    description: Branch places the note into the tree, it represents the relationship
  between a parent note and child note
properties:
  branchId:
    $ref: '#/components/schemas/EntityId'
  isExpanded:
    type: boolean
  noteId:
    $ref: '#/components/schemas/EntityId'
    description: identifies the child note
    readOnly: true
  notePosition:
    format: int32
    type: integer
  parentNoteId:
    $ref: '#/components/schemas/EntityId'
    description: identifies the parent note
    readOnly: true
  prefix:
    type: string
  utcDateModified:
    $ref: '#/components/schemas/UtcDateTime'
    readOnly: true
type: object

    """


@mcp.resource("schema://NoteWithBranch")
def get_NoteWithBranch_schema() -> str:
    """
    Get the NoteWithBranch schema definition
    """
    return """
    properties:
  branch:
    $ref: '#/components/schemas/Branch'
  note:
    $ref: '#/components/schemas/Note'
type: object

    """


@mcp.resource("schema://Attachment")
def get_Attachment_schema() -> str:
    """
    Get the Attachment schema definition
    """
    return """
    description: Attachment is owned by a note, has title and content
properties:
  attachmentId:
    $ref: '#/components/schemas/EntityId'
    readOnly: true
  blobId:
    description: ID of the blob object which effectively serves as a content hash
    type: string
  contentLength:
    format: int32
    type: integer
  dateModified:
    $ref: '#/components/schemas/LocalDateTime'
    readOnly: true
  mime:
    type: string
  ownerId:
    $ref: '#/components/schemas/EntityId'
    description: identifies the owner of the attachment, is either noteId or revisionId
  position:
    format: int32
    type: integer
  role:
    type: string
  title:
    type: string
  utcDateModified:
    $ref: '#/components/schemas/UtcDateTime'
    readOnly: true
  utcDateScheduledForErasureSince:
    $ref: '#/components/schemas/UtcDateTime'
    readOnly: true
type: object

    """


@mcp.resource("schema://CreateAttachment")
def get_CreateAttachment_schema() -> str:
    """
    Get the CreateAttachment schema definition
    """
    return """
    properties:
  content:
    type: string
  mime:
    type: string
  ownerId:
    $ref: '#/components/schemas/EntityId'
    description: identifies the owner of the attachment, is either noteId or revisionId
  position:
    format: int32
    type: integer
  role:
    type: string
  title:
    type: string
type: object

    """


@mcp.resource("schema://Attribute")
def get_Attribute_schema() -> str:
    """
    Get the Attribute schema definition
    """
    return """
    description: Attribute (Label, Relation) is a key-value record attached to a note.
properties:
  attributeId:
    $ref: '#/components/schemas/EntityId'
  isInheritable:
    type: boolean
  name:
    example: shareCss
    pattern: ^[^\s]+
    type: string
  noteId:
    $ref: '#/components/schemas/EntityId'
    description: identifies the child note
    readOnly: true
  position:
    format: int32
    type: integer
  type:
    enum:
    - label
    - relation
    type: string
  utcDateModified:
    $ref: '#/components/schemas/UtcDateTime'
    readOnly: true
  value:
    type: string
type: object

    """


@mcp.resource("schema://AttributeList")
def get_AttributeList_schema() -> str:
    """
    Get the AttributeList schema definition
    """
    return """
    items:
  $ref: '#/components/schemas/Attribute'
type: array

    """


@mcp.resource("schema://SearchResponse")
def get_SearchResponse_schema() -> str:
    """
    Get the SearchResponse schema definition
    """
    return """
    properties:
  debugInfo:
    description: debugging info on parsing the search query enabled with &debug=true
      parameter
    type: object
  results:
    items:
      $ref: '#/components/schemas/Note'
    type: array
required:
- results
type: object

    """


@mcp.resource("schema://EntityId")
def get_EntityId_schema() -> str:
    """
    Get the EntityId schema definition
    """
    return """
    example: evnnmvHTCgIn
pattern: '[a-zA-Z0-9_]{4,32}'
type: string

    """


@mcp.resource("schema://StringId")
def get_StringId_schema() -> str:
    """
    Get the StringId schema definition
    """
    return """
    example: my_ID
pattern: '[a-zA-Z0-9_]{1,32}'
type: string

    """


@mcp.resource("schema://EntityIdList")
def get_EntityIdList_schema() -> str:
    """
    Get the EntityIdList schema definition
    """
    return """
    items:
  $ref: '#/components/schemas/EntityId'
type: array

    """


@mcp.resource("schema://LocalDateTime")
def get_LocalDateTime_schema() -> str:
    """
    Get the LocalDateTime schema definition
    """
    return """
    example: 2021-12-31 20:18:11.930+0100
pattern: '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}[\+\-][0-9]{4}'
type: string

    """


@mcp.resource("schema://UtcDateTime")
def get_UtcDateTime_schema() -> str:
    """
    Get the UtcDateTime schema definition
    """
    return """
    example: 2021-12-31 19:18:11.930000+00:00
pattern: '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z'
type: string

    """


@mcp.resource("schema://AppInfo")
def get_AppInfo_schema() -> str:
    """
    Get the AppInfo schema definition
    """
    return """
    properties:
  appVersion:
    description: Trilium version
    example: 0.50.2
    type: string
  buildDate:
    description: build date
    example: 2022-02-09 22:52:36+01:00
    format: date-time
    type: string
  buildRevision:
    description: git build revision
    example: 23daaa2387a0655685377f0a541d154aeec2aae8
    type: string
  clipperProtocolVersion:
    description: version of the supported Trilium Web Clipper protocol
    example: 1.0
    type: string
  dataDirectory:
    description: data directory where Trilium stores files
    example: /home/user/data
    type: string
  dbVersion:
    description: DB version
    example: 194
    format: int32
    type: integer
  syncVersion:
    description: Sync protocol version
    example: 25
    format: int32
    type: integer
  utcDateTime:
    description: current UTC date time
    example: 2022-03-07 21:54:25.277000+00:00
    type: string
type: object

    """


@mcp.resource("schema://Error")
def get_Error_schema() -> str:
    """
    Get the Error schema definition
    """
    return """
    properties:
  code:
    description: stable string constant
    example: NOTE_IS_PROTECTED
    type: string
  message:
    description: Human readable error, potentially with more details,
    example: Note 'evnnmvHTCgIn' is protected and cannot be modified through ETAPI
    type: string
  status:
    description: HTTP status, identical to the one given in HTTP response
    example: 400
    format: int32
    type: integer
required:
- status
- code
- message
type: object

    """


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="MCP Server for ETAPI")
    parser.add_argument(
        "--transport", 
        choices=["sse", "io"], 
        default="sse",
        help="Transport type (sse or io)"
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    logger.info(f"Starting MCP server with {args.transport} transport")
    
    if args.transport == "sse":
        # Run with SSE transport (default host and port)
        mcp.run(transport="sse")
    else:
        # Run with stdio transport
        mcp.run(transport="stdio")