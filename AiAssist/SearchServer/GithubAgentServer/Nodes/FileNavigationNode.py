from langgraph.types import interrupt


class FileNavigationNode:

    def __init__(self, navigation_tool):
        self.navigation_tool = navigation_tool

    def __call__(self, state):

        current_path = state.get("current_path", "")

        result = self.navigation_tool.get_path(current_path)

        if not result["success"]:
            return {
                "error": result["error"]
            }

        # FILE
        if result["type"] == "file":

            return {
                "selected_path": result["path"],
                "file_content": result["content"],
                "selection_type": "file"
            }

        # DIRECTORY
        items = result["items"]

        selected = interrupt({
            "message": f"Select a file or folder from {current_path or 'repository root'}",
            "path": current_path,
            "items": items
        })

        return {
            "current_path": selected["path"],
            "selection_type": selected["type"]
        }