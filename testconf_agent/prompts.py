from langchain_core.prompts import PromptTemplate

PARAM_SYSTEM_PROMPT = PromptTemplate(input_variables=["n_valid_values", "n_invalid_values"], template="""
You are an expert software tester specializing in REST APIs. Your task is to generate a list of meaningful and diverse test values for the specified API parameter, generate {n_valid_values} valid values and {n_invalid_values} invalid values.""")

PARAM_GENERATION_PROMPT = PromptTemplate(
    input_variables=["api_name", "api_description", "operation_id", "operation_summary", "operation_description", "parameter_details"], template="""
API name: {api_name}
API description: {api_description}
Operation id: {operation_id}
Operation summary: {operation_summary}
Operation description: {operation_description}
Parameter Details:
{parameter_details}
""")

BODY_SYSTEM_PROMPT = "You are an expert software tester specializing in REST APIs. Your task is to generate a valid JSON request body containing the properties specified in following schema."

BODY_GENERATION_PROMPT = PromptTemplate(input_variables=["api_name", "api_description", "operation_id", "operation_summary", "operation_description", "schema"], template="""
API name: {api_name}
API description: {api_description}
Operation id: {operation_id}
Operation summary: {operation_summary}
Operation description: {operation_description}
Schema:
{schema}
""")
