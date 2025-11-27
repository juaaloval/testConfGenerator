from testconf_agent.oas_states import OverallState
from langgraph.constants import Send

def map_operations(state: OverallState):
    """
    Fans out execution: One branch per Operation.
    """
    print("--- [Main] Reading Spec and Fanning Out ---")
    # TODO: Read real spec
    # spec = state['oas_spec']
    
    # Extract operations (Simulated)
    # In reality: operations = extract_ops_from_spec(spec)
    oas_spec = {
        "info": {
            "title": "Yelp API",
            "version": "1.0.0",
            "description": "API used to search for locations"
        },
        "paths": {
            "/businesses/search": {
                "get": {
                    "operationId": "getBusinesses",
                    "summary": "Search for businesses",
                    "description": "Search for businesses",
                    "parameters": [
                        {"name": "location", "in": "query", "required": True, "schema": {"type": "string"},
                        "description": "Location to search for businesses"},
                        {"name": "term", "in": "query", "required": False, "schema": {"type": "string"},
                        "description": "Term to search for businesses"},
                        {"name": "categories", "in": "query", "required": False, "schema": {"type": "string"},
                        "description": "Categories to search for businesses"}
                    ]
                },
                "post": {
                    "operationId": "postBusinesses",
                    "summary": "Create a new business",
                    "description": "Create a new business",
                    "parameters": [
                        {"name": "name", "in": "query", "required": True, "schema": {"type": "string"},
                        "description": "Name of the business"},
                        {"name": "address", "in": "query", "required": True, "schema": {"type": "string"},
                        "description": "Address of the business"},
                        {"name": "city", "in": "query", "required": True, "schema": {"type": "string"},
                        "description": "City of the business"}
                    ]
                }
            },
            "/locations": {
                "get": {
                    "operationId": "getLocations",
                    "summary": "Get locations",
                    "description": "Get locations",
                    "parameters": [
                        {"name": "location", "in": "query", "required": True, "schema": {"type": "string"},
                        "description": "Location to search for locations"}
                    ]
                }
            }
        }
    }

    # Generate the Send objects
    # This creates a unique 'OperationState' for each branch
    return [
        Send("process_operation_batch", {"op_id": op["id"], "parameters": op["parameters"]})
        for op in operations
    ]