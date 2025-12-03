from testconf_agent.states import OperationState
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from typing import List, Union
from langchain_core.messages import SystemMessage, HumanMessage
import json
import pandas as pd
from langchain_core.output_parsers import JsonOutputParser
from testconf_agent.utils import ConfigLoader
from testconf_agent.prompts import PARAM_GENERATION_PROMPT, PARAM_SYSTEM_PROMPT, BODY_SYSTEM_PROMPT, BODY_GENERATION_PROMPT

# Load config info
config = ConfigLoader.load()

# Load LLM from config
llm = ChatOllama(
    model=config.get("llm").get("model_id"),
    temperature=config.get("llm").get("temperature"),
    device=config.get("llm").get("device"),
    max_tokens=config.get("llm").get("max_tokens")
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
    
    print(f"--- [Node Start] Batch processing {state['op_id']} ({len(state.get('parameters', []))} params) ---")
    
    # Local accumulation of results for this specific operation
    batch_results = []
    
    # Iterate over params
    for param in state.get('parameters', []):
        p_name = param['name']

        # Skip parameter if the name is None
        if not p_name:
            continue

        if param['in'] == 'body':
            generate_request_body(state, param.get('schema'))
        else:
            generate_param_value(state, param)

    request_body = state.get('request_body')
    if request_body:
        # Generate request body in JSON format
        generate_request_body(state, request_body.get('schema'))        


def get_test_values_filename(method, path, param_name, extension="csv"):
    """
    Returns a filename for the test values file. The value of the filename is <method>_<path>_<param_name>.csv,
    in lowercase and replacing '/' with '_'.
    """
    return f"{method}_{path}_{param_name}.{extension}".replace(" ", "_").replace("/", "_").replace("{", "_").replace("}", "_").lower()


def generate_param_value(state: OperationState, param: dict):
    messages = [
        SystemMessage(content=PARAM_SYSTEM_PROMPT.format(
            n_valid_values=config.get("generation").get("n_valid_values"),
            n_invalid_values=config.get("generation").get("n_invalid_values")
        )),
        HumanMessage(content=PARAM_GENERATION_PROMPT.format(
            api_name=state.get('api_name'), 
            api_description=state.get('api_description'), 
            operation_id=state.get('op_id'), 
            operation_summary=state.get('summary'), 
            operation_description=state.get('description'), 
            parameter_details=param)
        )
    ]

    # Configure the LLM to return a JSON object
    structured_llm = llm.with_structured_output(ParameterValuesSchema)
    
    # Get list of values from the LLM in JSON format
    try:
        # TODO: Add retry logic and timeout parameter
        model_response = structured_llm.invoke(messages)
        test_values = model_response.test_values
        print(model_response)
    except Exception as e:
        # If the LLM fails to generate a valid JSON object, skip this parameter
        # TODO: Add default values depending on the parameter datatype
        print(f"Error getting parameter values: {e}")
        test_values = []
    
    # Export to CSV
    pd.Series(test_values).to_csv(get_test_values_filename(state["method"], state["path"], param["name"]), index=False, header=False)


def generate_request_body(state: OperationState, schema: dict):
    messages = [
        SystemMessage(content=BODY_SYSTEM_PROMPT),
        
        HumanMessage(content=BODY_GENERATION_PROMPT.format(
            api_name=state.get('api_name'), 
            api_description=state.get('api_description'), 
            operation_id=state.get('op_id'), 
            operation_summary=state.get('summary'), 
            operation_description=state.get('description'), 
            schema=schema)
        )
    ]

    # Call LLM like in previous function, but generating a JSON file
    try:

        parser = JsonOutputParser()
        chain = llm | parser

        body_value = chain.invoke(messages)
        print("BODY VALUE:")
        print(body_value)
    except Exception as e:
        # If the LLM fails to generate a valid JSON object, skip this parameter
        # TODO: Add default values depending on the parameter datatype
        print(f"Error getting request body: {e}")
        body_value = {}

    # Export to JSON
    with open(get_test_values_filename(state["method"], state["path"], "body", "json"), "w") as f:
        json.dump(body_value, f)
