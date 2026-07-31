from .quiz_state import QuizState
from langgraph.graph import END
def QuizPlannerRouter(state:QuizState):

    plan = state['execution_plan']

    if not plan:
        return END

    return plan[0]