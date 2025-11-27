from langchain_core.prompts import PromptTemplate

VALUE_GENERATION_PROMPT = PromptTemplate(
    input_variables=["name", "description", "schema_type", "enum", "context"],
    template="""
You are an expert software tester specializing in REST APIs. Your task is to generate a list of meaningful and diverse test values for a specific API parameter.

Parameter Details:
- Name: {name}
- Description: {description}
- Type: {schema_type}
- Enum Values: {enum}
- Context (Operation Summary): {context}

Instructions:
1. Analyze the parameter description and type.
2. Generate a list of 5-10 values that cover different scenarios (valid, boundary, edge cases if applicable, but prioritize valid values that make sense for the context).
3. If the parameter is an enum, select a few representative values.
4. If the parameter is a search term or free text, provide realistic examples based on the description.
5. Return ONLY a JSON list of values. Do not include any other text or explanations.

Example Output:
["value1", "value2", 123, true]

Generated Values:
"""
)
