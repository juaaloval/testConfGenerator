from testconf_agent.states import OverallState
from langgraph.constants import Send
import yaml

def map_operations(state: OverallState):
    """
    Fans out execution: One branch per Operation.
    """
    print("--- [Main] Reading Spec and Fanning Out ---")

    # TODO: Surround with try/except
    with open(state['oas_path'], 'r', encoding='utf-8') as f:
            oas_spec = yaml.safe_load(f)

    # Generate the Send objects
    # This creates a unique 'OperationState' for each branch
    # General data
    # TODO: Improve spec analysis (use another library, body objects, etc.)
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
                "parameters": op["parameters"]
            }
        )
        for op in operations
    ]