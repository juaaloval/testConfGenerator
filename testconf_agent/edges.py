from testconf_agent.states import OverallState
from langgraph.constants import Send
import yaml
import jsonref

def map_operations(state: OverallState):
    """
    Fans out execution: One branch per Operation.
    """
    print("--- [Main] Reading Spec and Fanning Out ---")

    oas_spec = load_oas_spec(state['oas_path'])

    # Generate the Send objects
    # This creates a unique 'OperationState' for each branch
    # General data
    api_name = oas_spec.get("info", {}).get("title")
    api_description = oas_spec.get("info", {}).get("description")
    
    # Operations
    operations = []
    for path, methods in oas_spec['paths'].items():
        for method, op in methods.items():
            operations.append({
                "id": op.get("operationId"), 
                "summary": op.get("summary"),
                "description": op.get("description"),
                "path": path,
                "method": method,
                "parameters": op.get("parameters", []),
                "request_body": op.get("requestBody", {}).get("content", {}).get("application/json", None)
            })
    
    return [
        Send("process_operation_parameters",
            {
                "api_name": api_name,
                "api_description": api_description,
                "method": op["method"],
                "path": op["path"],
                "op_id": op["id"],
                "summary": op["summary"],
                "description": op["description"],                
                "parameters": op["parameters"],
                "request_body": op["request_body"]
            }
        )
        for op in operations
    ]


def load_oas_spec(oas_path: str):
    """
    Load OAS spec from file and resolve $refs.
    """
    # Load the raw yaml file
    with open(oas_path, "r") as f:
        raw_obj = yaml.safe_load(f)
    
    # Resolve $refs
    return jsonref.replace_refs(raw_obj)
