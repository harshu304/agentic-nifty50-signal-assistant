from agent.nodes import llm_decision_node

def run_agent(state):
    state = llm_decision_node(state)
    return state