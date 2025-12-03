from langchain_core.prompts import PromptTemplate

PARAM_SYSTEM_PROMPT = PromptTemplate(input_variables=["n_valid_values", "n_invalid_values"], template="""
You are an expert software tester specializing in REST APIs. Your task is to generate a list of meaningful and diverse test values for the specified API parameter, generate {n_valid_values} valid values and {n_invalid_values} invalid values.

### Valid Values
 
Valid values **MUST**:
 
- Strictly comply with **all** constraints defined in the OpenAPI schema for each parameter:
  - **Type**: `string`, `integer`, `number`, `boolean`, `array`, `object`
  - **Enum**: values must only come from the allowed set
  - **Numeric constraints**: `minimum`, `maximum`, `exclusiveMinimum`, `exclusiveMaximum`
  - **String constraints**: `minLength`, `maxLength`, `pattern`
  - **Array constraints**: `minItems`, `maxItems`, and `items` schema
- Respect constraints implied by the parameter **description**:
  - Formatting rules such as ISO 8601 dates, country codes, ZIP/postal codes, language codes, UUIDs, etc.
  - Identifier parameters should contain syntactically valid IDs whenever possible
- Avoid `null` values **unless** explicitly allowed in the schema (`nullable: true`)
 
---
 
### Invalid Values
 
Invalid values **MUST** intentionally violate** one or more** of the constraints listed above, such as:
 
- Using the wrong type (e.g., string instead of integer)
- Breaking numeric bounds, string length limits, or array size limits
- Producing values not defined in an enum
- Using malformed formats (e.g., incorrect date format, unknown country code)
- Generating unrealistic or inconsistent identifier values
""")

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
