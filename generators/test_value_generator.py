import json
from typing import Dict, Any, List
from langchain_core.language_models import LLM
from parsers.oas_parser import OperationInfo, ParameterInfo
from generators.prompts import VALUE_GENERATION_PROMPT

class TestValueGenerator:
    def __init__(self, llm: LLM):
        self.llm = llm

    def generate(self, oas_data: Dict[str, OperationInfo], testconf_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Iterates through the TestConf operations and updates parameters with LLM-generated values.
        """
        operations = testconf_data.get('testConfiguration', {}).get('operations', [])
        
        for op in operations:
            op_id = op.get('operationId')
            if not op_id or op_id not in oas_data:
                continue
            
            oas_op = oas_data[op_id]
            test_params = op.get('testParameters', [])
            
            for param in test_params:
                param_name = param.get('name')
                
                # Find corresponding OAS parameter info
                oas_param = next((p for p in oas_op.parameters if p.name == param_name), None)
                
                if oas_param:
                    print(f"Generating values for {op_id} -> {param_name}...")
                    new_values = self._generate_values_for_param(oas_param, oas_op.summary)
                    
                    if new_values:
                        # Update the generator to RandomInputValue with the new values
                        param['generators'] = [{
                            'type': 'RandomInputValue',
                            'genParameters': [{
                                'name': 'values',
                                'values': new_values,
                                'objectValues': None
                            }],
                            'valid': True
                        }]
        
        return testconf_data

    def _generate_values_for_param(self, param: ParameterInfo, context: str) -> List[Any]:
        """
        Invokes the LLM to generate values for a single parameter.
        """
        prompt = VALUE_GENERATION_PROMPT.format(
            name=param.name,
            description=param.description or "No description provided.",
            schema_type=param.schema_type,
            enum=param.enum or "None",
            context=context or "None"
        )
        
        try:
            response = self.llm.invoke(prompt)
            # Basic cleanup to ensure we get a list
            response_text = response.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:-3]
            elif response_text.startswith("```"):
                response_text = response_text[3:-3]
            
            values = json.loads(response_text)
            if isinstance(values, list):
                return values
            else:
                print(f"Warning: LLM did not return a list for {param.name}. Response: {response_text}")
                return []
        except Exception as e:
            print(f"Error generating values for {param.name}: {e}")
            return []
