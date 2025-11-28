from testconf_agent.graph import get_testconf_agent_graph

graph = get_testconf_agent_graph()


# TODO: Test max_concurrency with RESTCountries or similar
# graph.invoke(
#     {"oas_path": "./examples/oas_yelp.yaml"}, 
#     config={"max_concurrency": 1}
# )