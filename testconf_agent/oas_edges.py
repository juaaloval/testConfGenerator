from testconf_agent.oas_states import OverallState
from langgraph.constants import Send

def map_operations(state: OverallState):
    """
    Fans out execution: One branch per Operation.
    """
    print("--- [Main] Reading Spec and Fanning Out ---")
    # spec = state['oas_spec']
    
    # Extract operations (Simulated)
    # In reality: operations = extract_ops_from_spec(spec)
    operations = [
        {
            "id": "GET_users", 
            "parameters": [
                {"name": "limit", "type": "int"}, 
                {"name": "page", "type": "int"},
                {"name": "sort", "type": "string"}
            ]
        },
        {
            "id": "POST_user", 
            "parameters": [
                {"name": "email", "type": "string"},
                {"name": "username", "type": "string"}
            ]
        }
    ]
    
    # Generate the Send objects
    # This creates a unique 'OperationState' for each branch
    return [
        Send("process_operation_batch", {"op_id": op["id"], "parameters": op["parameters"]})
        for op in operations
    ]