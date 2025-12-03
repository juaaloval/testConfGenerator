from langgraph.constants import START, END
from langgraph.graph import StateGraph
from testconf_agent.nodes import process_operation_parameters

from testconf_agent.states import OverallState
from testconf_agent.edges import map_operations


def get_testconf_agent_graph():

    builder = StateGraph(OverallState)

    # Add the worker node
    builder.add_node("process_operation_parameters", process_operation_parameters)

    # Add the conditional edge (The Map)
    builder.add_conditional_edges(START, map_operations, ["process_operation_parameters"])
    builder.add_edge("process_operation_parameters", END)

    graph = builder.compile()
    return graph
