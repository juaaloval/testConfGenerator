from langchain_core.prompts import PromptTemplate

PARAM_SYSTEM_PROMPT = PromptTemplate(input_variables=["n_valid_values", "n_invalid_values"], template="""
**Role:** REST API test expert
 
**Task:** Generate **{n_valid_values}** **valid** test values for the given API parameter.
 
**Rules**
1. All values **must** satisfy **all** OpenAPI schema constraints.
2. All values **must** follow any implied format in the parameter name or description
   _(e.g. ISO-8601 date, UUID, country code, ZIP code)_.
3. Each value **must** be unique.""")

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
