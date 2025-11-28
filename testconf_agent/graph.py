from langgraph.constants import START, END
from langgraph.graph import StateGraph
from testconf_agent.nodes import process_operation_parameters, generate_extended_test_configuration_node

from testconf_agent.states import OverallState
from testconf_agent.edges import map_operations

def get_testconf_agent_graph():

    builder = StateGraph(OverallState)

    # Add the worker node
    builder.add_node("process_operation_parameters", process_operation_parameters)
    builder.add_node("generate_extended_test_configuration", generate_extended_test_configuration_node)

    # Add the conditional edge (The Map)
    builder.add_conditional_edges(START, map_operations, ["process_operation_parameters"])

    # Add the return edge
    builder.add_edge("process_operation_parameters", "generate_extended_test_configuration")
    builder.add_edge("generate_extended_test_configuration", END)

    graph = builder.compile()
    return graph
