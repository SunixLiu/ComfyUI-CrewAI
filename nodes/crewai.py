from crewai import Crew,Agent,Task
from langchain_openai import ChatOpenAI

class CrewNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "agent": ("AGENT",),
                "task":("TASK",),
            },
            "optional": {
                "verbose":("BOOLEAN", {"default": False}),
                "manager_llm": ("LLM",),
                "function_calling_llm": ("LLM",),
            }
        }
 
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("RESULT",)
 
    FUNCTION = "execute"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "Crewai"
  
    def execute(self,agent,task, verbose,manager_llm=None,function_calling_llm=None):
        # print("Agent: ",agent)
        # print("Task: ",task)
        crew = Crew(agents=[agent],tasks=[task], 
                    verbose=verbose, 
                    manager_llm=manager_llm if manager_llm is not None else None,
                    function_calling_llm=function_calling_llm if function_calling_llm is not None else None
                    )
        print("Before crew kickoff ....")
        result = crew.kickoff()
        print("After in crew function....")
        return (result,)
 
class AgentNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "role": ("STRING", {"multiline": True, "dynamicPrompts": False, "default": ""}),
                "goal": ("STRING", {"multiline": True, "dynamicPrompts": False, "default": ""}),
                "backstory": ("STRING", {"multiline": True, "dynamicPrompts": False, "default": ""}),                                                                       
            },
            "optional":{
                "llm": ("LLM",),
            }
        }
 
    RETURN_TYPES = ("AGENT",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_one_agent"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai"
 
    def set_one_agent(self,role,goal, backstory,llm=None):
        if llm is not None:
            agent = Agent(role=role,goal=goal,backstory=backstory,llm=llm)
        else:
            agent = Agent(role=role,goal=goal,backstory=backstory)
        print("Excuting in agent function....")
        return (agent,)
    
class TaskNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "description": ("STRING", {"multiline": True, "dynamicPrompts": False, "default": ""}),
                "agent":("AGENT",),
                "expected_output": ("STRING", {"multiline": True, "dynamicPrompts": False, "default": ""}),                                                                                      
            },
            "optional": {
                "async_execution":("BOOLEAN", {"default": False}),
                "llm": ("LLM",),
            }
        }
 
    RETURN_TYPES = ("TASK",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_task"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai"
 
    def set_task(self,description, agent,expected_output,async_execution,llm=None):
        task = Task(description=description,agent=agent,expected_output=expected_output,async_execution=async_execution,llm=llm if llm is not None else None)
        print("Excuting in task function....")
        return (task,)
    
class LLMNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base_url": ("STRING", {"default": "http://localhost:1234/v1"}),
                "api_key": ("STRING", {"default": "mykey"}),
             },
            "optional":{
                "model": ("STRING", {"default": "TheBloke/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"}),
            }
        }
 
    RETURN_TYPES = ("LLM",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_llm"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai"
 
    def set_llm(self,base_url,api_key,model):
        llm = ChatOpenAI(base_url=base_url,api_key=api_key,model=model)
        return (llm,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Crew": CrewNode,
    "Agent": AgentNode,
    "Task": TaskNode,
    "LLM": LLMNode,
}
 
# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "CrewtNode": "Node of Crew",
    "AgentNode": "Node of Agent",
    "TaskNode": "Node of Task",
    "LLMNode": "Node of LLM",
}
 

 
 
# # A dictionary that contains all nodes you want to export with their names
# # NOTE: names should be globally unique
# NODE_CLASS_MAPPINGS = {
#     "Agent": Agent
# }
 
# # A dictionary that contains the friendly/humanly readable titles for the nodes
# NODE_DISPLAY_NAME_MAPPINGS = {
#     "AgentNode": "Node of Agent"
# }

 
 
# # A dictionary that contains all nodes you want to export with their names
# # NOTE: names should be globally unique
# NODE_CLASS_MAPPINGS = {
#     "Task": Task
# }
 
# # A dictionary that contains the friendly/humanly readable titles for the nodes
# NODE_DISPLAY_NAME_MAPPINGS = {
#     "TaskNode": "Node of Task"
# }