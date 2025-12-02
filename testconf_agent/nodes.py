from testconf_agent.states import OperationState
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import List, Union
from langchain_core.messages import SystemMessage, HumanMessage
import json
import pandas as pd


# Requires environment variable OPENAI_API_KEY
# TODO: Replace with Ollama in the future
# TODO: Convert into configurable parameters
# llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
llm = ChatOllama(
    # TODO: Model should be a configurable parameter
    model="llama3.2:3b",
    # model="gemma3:4b",
    # TODO: Temperature should be a configurable parameter, change on specific tasks
    temperature=0.7
)


# Pydantic Schema for the JSON Output containing the list of test values for an API parameter
class ParameterValuesSchema(BaseModel):
    """
    Structure for the generated list of test values for an API parameter.
    """
    test_values: List[Union[str, int, float, bool]] = Field(
        description="A list of diverse, meaningful, and edge-case test values for the API parameter. The datatype of the values must match the datatype of the parameter."
    )


def process_operation_parameters(state: OperationState):
    """
    This node receives ONE operation, but processes ALL its parameters 
    sequentially inside a standard Python loop.
    """
    op_id = state['op_id']
    path = state['path']
    method = state['method']
    params = state.get('parameters', [])
    
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
            Operation id: {state.get('op_id')}
            Parameter Details:
            {param}
            """)
        ]
        print(messages)

        # Configure the LLM to return a JSON object
        structured_llm = llm.with_structured_output(ParameterValuesSchema)

        # Get list of values from the LLM in JSON format
        try:
            model_response = structured_llm.invoke(messages)
            test_values = model_response.test_values
            print(model_response)
        except Exception as e:
            # If the LLM fails to generate a valid JSON object, skip this parameter
            # TODO: Add default values depending on the parameter datatype
            print(f"Error getting parameter values: {e}")
            test_values = []

        # Export to CSV
        pd.Series(test_values).to_csv(get_test_values_filename(method, path, param['name']), index=False, header=False)
    
    # RETURN ONLY THE RESULTS
    # Adds the results to the OverallState
    # We return a dict matching OverallState to merge into 'final_report'.
    # We do NOT return 'op_id' or 'parameters' to avoid global state write conflicts.
    # TODO: THIS SHOULD NOT RETURN ANYTHING, DELETE
    return {"final_report": {op_id: batch_results}}


def get_test_values_filename(method, path, param_name):
    """
    Returns a filename for the test values file. The value of the filename is <method>_<path>_<param_name>.csv,
    in lowercase and replacing '/' with '_'.
    """
    return f"{method}_{path}_{param_name}.csv".replace(" ", "_").replace("/", "_").replace("{", "_").replace("}", "_").lower()

# TODO: DELETE
def generate_extended_test_configuration_node(state):
    # For now, simply export the parameter values to a JSON file
    with open("test_configuration.json", "w") as f:
        json.dump(state["final_report"], f, indent=4)
    return {}
    