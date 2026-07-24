from .LanggraphState import LanggraphState
from langgraph.graph import END

def planner_route(state:LanggraphState):

    plan = state['execution_plan']

    print("plan is :",plan)

    if not plan:
        return END

    return plan[0]