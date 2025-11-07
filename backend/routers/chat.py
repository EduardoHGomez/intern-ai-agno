# from datetime import datetime
# from fastapi import APIRouter, HTTPException, Body
# from agents import RAGTeam
# import json

# router = APIRouter(prefix="/api", tags=["chat"])

# @router.get("/sessions/{session_id}/messages")
# async def get_session_messages(session_id: str):
#     """Gets all messages for a session including Exa search results"""
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print(f"[{timestamp}] GET /api/sessions/{session_id}/messages")

#     try:
#         messages = RAGTeam.get_messages_for_session(session_id=session_id)

#         formatted_messages = []
#         for msg in messages:
#             role = msg.role if hasattr(msg, 'role') else 'assistant'
#             content = msg.content if hasattr(msg, 'content') else str(msg)
            
#             # Extract tool calls/results if present
#             tool_data = None
#             if hasattr(msg, 'tool_calls') and msg.tool_calls:
#                 tool_data = {"tool_calls": []}
#                 for call in msg.tool_calls:
#                     # Handle both dict and object formats
#                     if isinstance(call, dict):
#                         tool_data["tool_calls"].append({
#                             "name": call.get("name"),
#                             "arguments": call.get("arguments"),
#                             "result": call.get("result")
#                         })
#                     else:
#                         tool_data["tool_calls"].append({
#                             "name": getattr(call, 'name', None),
#                             "arguments": getattr(call, 'arguments', None),
#                             "result": getattr(call, 'result', None)
#                         })

#             if role in ['user', 'assistant']:
#                 message_obj = {
#                     "role": role,
#                     "content": content
#                 }
#                 if tool_data:
#                     message_obj["tool_data"] = tool_data
                    
#                 formatted_messages.append(message_obj)

#         print(f"[{timestamp}] Retrieved {len(formatted_messages)} messages")
#         return {"messages": formatted_messages}

#     except Exception as e:
#         print(f"[{timestamp}] Error: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/chat")
# async def chat(payload: dict = Body(...)):
#     """
#     Chat endpoint with MCP/Exa integration
    
#     Payload:
#         - message: str (required)
#         - session_id: str (required, UUID v4)
        
#     Returns:
#         - session_id: str
#         - response: str (agent response)
#         - search_results: list (if Exa search was used)
#     """
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     try:
#         message = payload.get("message")
#         session_id = payload.get("session_id")
#         model = payload.get("model")

#         if not message:
#             raise HTTPException(status_code=400, detail="message is required")
#         if not session_id:
#             raise HTTPException(status_code=400, detail="session_id is required")

#         print(f"[{timestamp}] POST /api/chat - Session: {session_id}, Message: '{message[:100]}...'")

#         # Run the team agent
#         run_response = RAGTeam.run(message, session_id=session_id)

#         # Extract response text
#         text = (
#             getattr(run_response, "content", None) or 
#             getattr(run_response, "output_text", None) or 
#             str(run_response)
#         )

#         # Extract Exa search results and sources
#         search_results = []
#         sources = []
        
#         if hasattr(run_response, 'messages'):
#             for msg in run_response.messages:
#                 if hasattr(msg, 'tool_calls') and msg.tool_calls:
#                     for tool_call in msg.tool_calls:
#                         # Handle both dict and object formats
#                         if isinstance(tool_call, dict):
#                             tool_name = tool_call.get('name', '')
#                             tool_args = tool_call.get('arguments', {})
#                             tool_result = tool_call.get('result')
#                         else:
#                             tool_name = getattr(tool_call, 'name', '')
#                             tool_args = getattr(tool_call, 'arguments', {})
#                             tool_result = getattr(tool_call, 'result', None)
                        
#                         # Check if it's an Exa tool
#                         if tool_name in ['exa_search', 'exa_get_contents']:
#                             if tool_result:
#                                 search_results.append({
#                                     "tool": tool_name,
#                                     "arguments": tool_args,
#                                     "result": tool_result
#                                 })
                                
#                                 # Extract URLs/sources
#                                 if isinstance(tool_result, dict):
#                                     if 'results' in tool_result:
#                                         for r in tool_result['results']:
#                                             if isinstance(r, dict) and 'url' in r:
#                                                 sources.append(r['url'])
#                                 elif isinstance(tool_result, list):
#                                     for r in tool_result:
#                                         if isinstance(r, dict) and 'url' in r:
#                                             sources.append(r['url'])

#         response_data = {
#             "session_id": run_response.session_id,
#             "response": text
#         }
        
#         # Add search results if present
#         if search_results:
#             response_data["search_results"] = search_results
#         if sources:
#             response_data["sources"] = list(set(sources))  # Deduplicate

#         print(f"[{timestamp}] Response sent - Length: {len(text)}, Sources: {len(sources)}")
#         return response_data

#     except HTTPException:
#         raise
#     except Exception as e:
#         print(f"[{timestamp}] Error: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/search")
# async def direct_search(payload: dict = Body(...)):
#     """
#     Direct Exa search endpoint (bypasses agent)
    
#     Payload:
#         - query: str (required)
#         - num_results: int (optional, default 5)
#         - search_type: str (optional: auto/neural/keyword)
#         - include_content: bool (optional, default False)
#     """
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     try:
#         from agents.exa_agent import ExaAgent
        
#         query = payload.get("query")
#         if not query:
#             raise HTTPException(status_code=400, detail="query is required")
        
#         num_results = payload.get("num_results", 5)
#         search_type = payload.get("search_type", "auto")
#         include_content = payload.get("include_content", False)
        
#         print(f"[{timestamp}] POST /api/search - Query: '{query}', Results: {num_results}")
        
#         # Use the agent's tool directly
#         tool_call = f"Search for: {query}"
#         if include_content:
#             tool_call += " and get full content"
            
#         response = ExaAgent.run(tool_call)
        
#         return {
#             "query": query,
#             "results": response.content
#         }
        
#     except Exception as e:
#         print(f"[{timestamp}] Error in /api/search: {str(e)}")
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))

from datetime import datetime
from fastapi import APIRouter, HTTPException, Body
from agents import RAGTeam
from typing import Optional
import json


router = APIRouter(prefix="/api", tags=["chat"])

@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str, model: Optional[str] = 'gpt-4o'):
    """Gets all messages for a session including Exa search results"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] GET /api/sessions/{session_id}/messages")
    print("Model: ", model)

    try:
        messages = RAGTeam(model).get_messages_for_session(session_id=session_id)

        formatted_messages = []
        for msg in messages:
            role = msg.role if hasattr(msg, 'role') else 'assistant'
            content = msg.content if hasattr(msg, 'content') else str(msg)
            
            # Extract tool calls/results if present
            tool_data = None
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                tool_data = {"tool_calls": []}
                for call in msg.tool_calls:
                    # Handle both dict and object formats
                    if isinstance(call, dict):
                        tool_data["tool_calls"].append({
                            "name": call.get("name"),
                            "arguments": call.get("arguments"),
                            "result": call.get("result")
                        })
                    else:
                        tool_data["tool_calls"].append({
                            "name": getattr(call, 'name', None),
                            "arguments": getattr(call, 'arguments', None),
                            "result": getattr(call, 'result', None)
                        })

            if role in ['user', 'assistant']:
                message_obj = {
                    "role": role,
                    "content": content
                }
                if tool_data:
                    message_obj["tool_data"] = tool_data
                    
                formatted_messages.append(message_obj)

        print(f"[{timestamp}] Retrieved {len(formatted_messages)} messages")
        return {"messages": formatted_messages}

    except Exception as e:
        print(f"[{timestamp}] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat")
async def chat(payload: dict = Body(...)):
    """
    Chat endpoint with MCP/Exa integration
    
    Payload:
        - message: str (required)
        - session_id: str (required, UUID v4)
        
    Returns:
        - session_id: str
        - response: str (agent response)
        - search_results: list (if Exa search was used)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        message = payload.get("message")
        session_id = payload.get("session_id")
        model = payload.get("model", "gpt-4o")
        print("Model", model)

        if not message:
            raise HTTPException(status_code=400, detail="message is required")
        if not session_id:
            raise HTTPException(status_code=400, detail="session_id is required")

        print(f"[{timestamp}] POST /api/chat - Session: {session_id}, Message: '{message[:100]}...'")

        # Run the team agent
        run_response = RAGTeam(model).run(input=message, session_id=session_id)

        # Extract response text
        text = (
            getattr(run_response, "content", None) or 
            getattr(run_response, "output_text", None) or 
            str(run_response)
        )

        # Extract Exa search results and sources
        search_results = []
        sources = []
        
        if hasattr(run_response, 'messages'):
            for msg in run_response.messages:
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        # Handle both dict and object formats
                        if isinstance(tool_call, dict):
                            tool_name = tool_call.get('name', '')
                            tool_args = tool_call.get('arguments', {})
                            tool_result = tool_call.get('result')
                        else:
                            tool_name = getattr(tool_call, 'name', '')
                            tool_args = getattr(tool_call, 'arguments', {})
                            tool_result = getattr(tool_call, 'result', None)
                        
                        # Check if it's an Exa tool
                        if tool_name in ['exa_search', 'exa_get_contents']:
                            if tool_result:
                                search_results.append({
                                    "tool": tool_name,
                                    "arguments": tool_args,
                                    "result": tool_result
                                })
                                
                                # Extract URLs/sources
                                if isinstance(tool_result, dict):
                                    if 'results' in tool_result:
                                        for r in tool_result['results']:
                                            if isinstance(r, dict) and 'url' in r:
                                                sources.append(r['url'])
                                elif isinstance(tool_result, list):
                                    for r in tool_result:
                                        if isinstance(r, dict) and 'url' in r:
                                            sources.append(r['url'])

        response_data = {
            "session_id": run_response.session_id,
            "response": text
        }
        
        # Add search results if present
        if search_results:
            response_data["search_results"] = search_results
        if sources:
            response_data["sources"] = list(set(sources))  # Deduplicate

        print(f"[{timestamp}] Response sent - Length: {len(text)}, Sources: {len(sources)}")
        return response_data

    except HTTPException:
        raise
    except Exception as e:
        print(f"[{timestamp}] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search")
async def direct_search(payload: dict = Body(...)):
    """
    Direct Exa search endpoint (bypasses agent)
    
    Payload:
        - query: str (required)
        - num_results: int (optional, default 5)
        - search_type: str (optional: auto/neural/keyword)
        - include_content: bool (optional, default False)
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        from agents.exa_agent import ExaAgent
        
        query = payload.get("query")
        if not query:
            raise HTTPException(status_code=400, detail="query is required")
        
        num_results = payload.get("num_results", 5)
        search_type = payload.get("search_type", "auto")
        include_content = payload.get("include_content", False)
        
        print(f"[{timestamp}] POST /api/search - Query: '{query}', Results: {num_results}")
        
        # Use the agent's tool directly
        tool_call = f"Search for: {query}"
        if include_content:
            tool_call += " and get full content"
            
        response = ExaAgent.run(tool_call)
        
        return {
            "query": query,
            "results": response.content
        }
        
    except Exception as e:
        print(f"[{timestamp}] Error in /api/search: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))