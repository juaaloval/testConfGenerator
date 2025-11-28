from testconf_agent.states import OperationState
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Union
from langchain_core.messages import SystemMessage, HumanMessage


# Requires environment variable OPENAI_API_KEY
# TODO: Replace with Ollama in the future
# TODO: Convert into configurable parameters
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)

# Pydantic Schema for the JSON Output containing the list of test values for an API parameter
class ParameterValuesSchema(BaseModel):
    """
    Structure for the generated list of test values for an API parameter.
    """
    test_values: List[Union[str, int, float, bool]] = Field(
        description="A list of diverse, meaningful, and edge-case test values for the API parameter. The datatype of the values must match the datatype of the parameter."
    )


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

        # Skip parameter if the name is None
        if not p_name:
            continue
        
        # TODO: Improve prompts
        # TODO: Add parameters such as number of values to generate
        # TODO: Manage parameter values if None
        messages  = [
            SystemMessage(content="You are an expert software tester specializing in REST APIs. Your task is to generate a list of meaningful and diverse test values for a specific API parameter, " +
            "the values must be as diverse as possible."),
            # TODO: Improve prompt
            # TODO: At least include API and operation data
            # TODO: Add operation description/summary
            HumanMessage(content=f"""
            API name: {state.get('api_name')}
            API description: {state.get('api_description')}
            Operation id: {state['op_id']}
            Parameter Details:
            {param}
            """)
        ]

        # Configure the LLM to return a JSON object
        structured_llm = llm.with_structured_output(ParameterValuesSchema)

        # Get list of values from the LLM in JSON format
        try:
            model_response = structured_llm.invoke(messages)
        except Exception as e:
            # If the LLM fails to generate a valid JSON object, skip this parameter
            print(f"Error getting parameter values: {e}")
            continue

        batch_results.append({
            p_name: model_response.test_values
        })
    
    # RETURN ONLY THE RESULTS
    # Adds the results to the OverallState
    # We return a dict matching OverallState to merge into 'final_report'.
    # We do NOT return 'op_id' or 'parameters' to avoid global state write conflicts.
    return {"final_report": batch_results}


# TODO: Generate extended test configuration (real)
def generate_extended_test_configuration_node(state):
    # For now, simply export the parameter values to a JSON file
    with open("test_configuration.json", "w") as f:
        json.dump(state["parameter_values"], f, indent=4)
    return {}
    