from testconf_agent.oas_states import OperationState

def process_operation_batch(state: OperationState):
    """
    This node receives ONE operation, but processes ALL its parameters 
    sequentially inside a standard Python loop.
    """
    op_id = state['op_id']
    params = state['parameters']
    
    print(f"--- [Node Start] Batch processing {op_id} ({len(params)} params) ---")
    
    # Local accumulation of results for this specific operation
    batch_results = []
    
    # Iterate over params
    for param in params:
        p_name = param['name']
        p_type = param['type']
        
        # Simulate Local LLM work
        # response = local_llm.invoke(f"Analyze {p_name}...")
        print(f"    ... Checking param '{p_name}' locally")
        
        # Format the result
        result_str = f"[{op_id}] Parameter '{p_name}' ({p_type}): VALID"
        batch_results.append(result_str)
        
    print(f"--- [Node End] Finished {op_id} ---")
    
    # RETURN ONLY THE RESULTS
    # We return a dict matching OverallState to merge into 'final_report'.
    # We do NOT return 'op_id' or 'parameters' to avoid global state write conflicts.
    return {"final_report": batch_results}