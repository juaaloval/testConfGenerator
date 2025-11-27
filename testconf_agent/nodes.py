from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Requires environment variable OPENAI_API_KEY
# TODO: Replace with Ollama in the future
# TODO: Convert into configurable parameters
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.7)

def extract_parameter_data_node(state):
    # TODO: Extract parameter data from state
    return {"current_parameter": {
        "name": "location",
        "description": "Required if either latitude or longitude is not provided. This string indicates the geographic area to be used when searching for businesses. Examples: 'New York City', 'NYC', '350 5th Ave, New York, NY 10118'. Businesses returned in the response may not be strictly within the specified location.",
        "schema_type": "string"
    }}


def get_parameter_values_node(state):
    messages  = [
        SystemMessage(content="You are an expert software tester specializing in REST APIs. Your task is to generate a list of meaningful and diverse test values for a specific API parameter."),
        # TODO: Improve prompt
        # TODO: At least include API and operation data
        HumanMessage(content="""
        Parameter Details:
        {current_parameter}
        """)
    ]

    # TODO: Format response into a list of values
    model_response = llm.invoke(messages)
    return {"values": model_response}