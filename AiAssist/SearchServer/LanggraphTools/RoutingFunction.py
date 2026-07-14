from langgraph.graph import END
from .LanggraphState import LanggraphState

# Decide where the graph should go next
def route(state: LanggraphState):

    plan =state["execution_plan"]
    print("plan is ",plan)

    if not plan:
        return END

    return plan[0]