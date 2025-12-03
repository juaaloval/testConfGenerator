from langchain_core.prompts import PromptTemplate

# TODO: Improve prompt
# TODO: At least include API and operation data
# TODO: Add operation description/summary

PARAM_SYSTEM_PROMPT = "You are an expert software tester specializing in REST APIs. Your task is to generate a list of meaningful and diverse test values for a specific API parameter, the values must be as diverse as possible."

# TODO: Improve prompts
# TODO: Add parameters such as number of values to generate
# TODO: Manage parameter values if None
# TODO: Test $refs
# TODO: Add operation description/summary
PARAM_GENERATION_PROMPT = PromptTemplate(
    input_variables=["api_name", "api_description", "operation_id", "parameter_details"], template="""
API name: {api_name}
API description: {api_description}
Operation id: {operation_id}
Parameter Details:
{parameter_details}
""")

BODY_SYSTEM_PROMPT = "You are an expert software tester specializing in REST APIs. Your task is to generate a valid JSON body containing the properties specified in following schema."

# TODO: Improve prompt
# TODO: At least include API and operation data
# TODO: Add operation description/summary
# Same as commented above
BODY_GENERATION_PROMPT = PromptTemplate(input_variables=["api_name", "api_description", "operation_id", "schema"], template="""
API name: {api_name}
API description: {api_description}
Operation id: {operation_id}
Schema:
{schema}
""")
