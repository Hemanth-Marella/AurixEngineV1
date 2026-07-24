from ..LanggraphTools.LanggraphState import LanggraphState
from langgraph.graph import END

# this node is only for build and update the state 
# this node is actually a planner node which is source to graph conditional edges
def planner_node(state:LanggraphState):

    return state