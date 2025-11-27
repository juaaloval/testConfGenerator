from langgraph.graph import MessagesState

# TODO: Does it really need to be a message state? A simple TypedDict might be enough
class TestConfGraphState(MessagesState):
    # TODO: Add missing state variables
    # TODO: Add current operation data (context for the model)
    # TODO: Add API name
    current_parameter: dict
    parameter_values: dict
