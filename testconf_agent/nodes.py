from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Union
from langchain_core.messages import SystemMessage, HumanMessage
import json

# Requires environment variable OPENAI_API_KEY
# TODO: Replace with Ollama in the future
# TODO: Convert into configurable parameters
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)

def extract_parameter_data_node(state):
    # TODO: Extract parameter data from state
    # TODO: Initialize parameter values in a different node in the future
    return {"current_parameter": {
        "name": "location",
        "description": "Required if either latitude or longitude is not provided. This string indicates the geographic area to be used when searching for businesses. Examples: 'New York City', 'NYC', '350 5th Ave, New York, NY 10118'. Businesses returned in the response may not be strictly within the specified location.",
        "schema_type": "string"
    }, "parameter_values": {}}


# Pydantic Schema for the JSON Output containing the list of test values for an API parameter
class ParameterValuesSchema(BaseModel):
    """
    Structure for the generated list of test values for an API parameter.
    """
    test_values: List[Union[str, int, float, bool]] = Field(
        description="A list of diverse, meaningful, and edge-case test values for the API parameter. The datatype of the values must match the datatype of the parameter."
    )

def get_parameter_values_node(state):

    parameter_name = state["current_parameter"].get("name")

    # Perform this step only if the parameter name is not None
    if parameter_name:
        messages  = [
            SystemMessage(content="You are an expert software tester specializing in REST APIs. Your task is to generate a list of meaningful and diverse test values for a specific API parameter, " +
            "the values must be as diverse as possible."),
            # TODO: Improve prompt
            # TODO: At least include API and operation data
            HumanMessage(content=f"""
            Parameter Details:
            {state["current_parameter"]}
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
            return {}

        # Update parameter values
        parameter_values = state["parameter_values"]
        parameter_values[parameter_name] = model_response.test_values
        return {"parameter_values": parameter_values}


def generate_extended_test_configuration_node(state):
    # For now, simply export the parameter values to a JSON file
    with open("test_configuration.json", "w") as f:
        json.dump(state["parameter_values"], f, indent=4)
    return {}