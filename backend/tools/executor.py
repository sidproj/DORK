class ToolExecutor:
    
    def __init__(self,registry):
        self.registry = registry
    
    def execute(self,name:str,arguments:dict):
        tool = self.registry.get(name)
        
        print("Tool:",tool)
    
        if not tool:
            print("Tool not found!")
            return {
                "success": False,
                "tool": name,
                "result": None,
                "error": f"Unknown tool: {name}"
            }
    
        try:
            result = tool.execute(**arguments)
            
            print("result for tool: ",result)
            
            return {
                "success":True,
                "tool":name,
                "result":result,
                "error":None
            }
        except Exception as e:
            print(e)
            return {
                "success": False,
                "tool": name,
                "result": None,
                "error": str(e)
            }