from langgraph.constants import START, END
from langgraph.graph import StateGraph
from testconf_agent.TestConfGraphState import TestConfGraphState
from testconf_agent.nodes import (extract_parameter_data_node, 
                                 get_parameter_values_node, 
                                 generate_extended_test_configuration_node)

from testconf_agent.oas_states import OverallState
from testconf_agent.oas_nodes import process_operation_batch
from testconf_agent.oas_edges import map_operations

def get_testconf_agent_graph():

    builder = StateGraph(OverallState)

    # Add the worker node
    builder.add_node("process_operation_batch", process_operation_batch)

    # Add the conditional edge (The Map)
    builder.add_conditional_edges(START, map_operations, ["process_operation_batch"])

    # Add the return edge
    builder.add_edge("process_operation_batch", END)

    graph = builder.compile()
    return graph
    
    # Create graph
    # builder = StateGraph(TestConfGraphState)

    # # Add nodes
    # builder.add_node("extract_parameter_data", extract_parameter_data_node)
    # builder.add_node("get_parameter_values", get_parameter_values_node)
    # builder.add_node("generate_extended_test_configuration", generate_extended_test_configuration_node)

    # # Add edges
    # builder.add_edge(START, "extract_parameter_data")
    # builder.add_edge("extract_parameter_data", "get_parameter_values")
    # builder.add_edge("get_parameter_values", "generate_extended_test_configuration")
    # builder.add_edge("generate_extended_test_configuration", END)

    # # Compile and return graph
    # return builder.compile()
