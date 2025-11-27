import yaml
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class ParameterInfo(BaseModel):
    name: str
    in_: str  # 'query', 'path', 'header', 'cookie'
    description: Optional[str] = None
    schema_type: Optional[str] = None
    enum: Optional[List[Any]] = None
    required: bool = False

class OperationInfo(BaseModel):
    operation_id: str
    path: str
    method: str
    summary: Optional[str] = None
    description: Optional[str] = None
    parameters: List[ParameterInfo] = []

class OASParser:
    @staticmethod
    def parse(file_path: str) -> Dict[str, OperationInfo]:
        """
        Parses an OAS file and returns a dictionary mapping operation IDs to OperationInfo objects.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        operations = {}
        paths = data.get('paths', {})

        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() not in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
                    continue
                
                operation_id = details.get('operationId')
                if not operation_id:
                    continue

                params = []
                # Handle path-level parameters
                path_params = methods.get('parameters', [])
                # Handle operation-level parameters
                op_params = details.get('parameters', [])
                
                all_params = path_params + op_params

                for p in all_params:
                    # Resolve $ref if necessary (simplified for now, assuming no refs for params in this example)
                    # In a full implementation, we'd need to handle $ref resolution.
                    
                    schema = p.get('schema', {})
                    param_info = ParameterInfo(
                        name=p['name'],
                        in_=p['in'],
                        description=p.get('description'),
                        schema_type=schema.get('type'),
                        enum=schema.get('enum'),
                        required=p.get('required', False)
                    )
                    params.append(param_info)

                operations[operation_id] = OperationInfo(
                    operation_id=operation_id,
                    path=path,
                    method=method,
                    summary=details.get('summary'),
                    description=details.get('description'),
                    parameters=params
                )
        
        return operations
