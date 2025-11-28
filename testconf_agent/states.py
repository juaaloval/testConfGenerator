from typing import TypedDict, List, Annotated, Union
import operator


# This custom function mimics "operator.add" but for dictionaries
def merge_dicts(existing: dict, new_data: dict) -> dict:
    # Python 3.9+ syntax to merge dictionaries
    # This creates a new dict with keys from both, 
    # taking values from new_data if there is a conflict.
    return existing | new_data


# Global State: Tracks the Spec and the Aggregated Report
class OverallState(TypedDict):
    oas_spec: dict
    # This reducer ensures results from parallel branches are merged, not overwritten
    # Equivalent to test values
    final_report: Annotated[dict, merge_dicts]

# Operation State: The input payload for a single Operation worker
class OperationState(TypedDict):
    api_name: str
    api_description: str
    op_id: str
    parameters: List[dict]
    # TODO: Add operation description/summary