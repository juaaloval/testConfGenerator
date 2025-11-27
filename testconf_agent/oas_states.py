from typing import TypedDict, List, Annotated, Union
import operator

# Global State: Tracks the Spec and the Aggregated Report
class OverallState(TypedDict):
    oas_spec: dict
    # This reducer ensures results from parallel branches are merged, not overwritten
    # Equivalent to test values
    final_report: Annotated[List[str], operator.add]

# Operation State: The input payload for a single Operation worker
class OperationState(TypedDict):
    api_name: str
    api_description: str
    op_id: str
    parameters: List[dict]