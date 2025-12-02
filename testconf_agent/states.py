from typing import TypedDict, List


# Global State: Tracks the Spec and the Aggregated Report
class OverallState(TypedDict):
    oas_path: str
    oas_spec: dict

# Operation State: The input payload for a single Operation worker
class OperationState(TypedDict):
    api_name: str
    api_description: str
    op_id: str
    parameters: List[dict]
    # TODO: Add operation description/summary