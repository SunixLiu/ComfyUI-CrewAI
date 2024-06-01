from crewai import Crew,Agent,Task, Process
from crewai_tools import (
    ScrapeWebsiteTool, 
    SerperDevTool, 
    FileReadTool,
    PDFSearchTool,
    MDXSearchTool,
    CSVSearchTool
    )
import os
from langchain_openai import ChatOpenAI

os.environ["SERPER_API_KEY"] = "88dd154f3a7fbb3bd72f1f98df676deb94ceaedb"
os.environ["OPENAI_BASE_URL"]="https://api.groq.com/openai/v1"
os.environ["OPENAI_API_KEY"] = "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"


class CrewNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "agents": ("AGENTLIST",),
                "tasks":("TASKLIST",),
            },
            "optional": {
                "verbose":("BOOLEAN", {"default": False}),
                "manager_llm": ("LLM",),
                "function_calling_llm": ("LLM",),
                # "inputs":("CREW_INPUTS"),
            }
        }
 
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("RESULT",)
 
    FUNCTION = "execute"
 
    #OUTPUT_NODE = False
 
    CATEGORY = "Crewai"
  
    def execute(self,agents,tasks, verbose,manager_llm=None,function_calling_llm=None):
        crew = Crew(agents=agents,tasks=tasks, 
                    verbose=verbose, 
                    manager_llm=manager_llm if manager_llm is not None else None,
                    function_calling_llm=function_calling_llm if function_calling_llm is not None else None
                    )
        print("Before crew kickoff ....")
        # if inputs is not None:
        #     crew.set_inputs(inputs)
        #     crew.kickoff(inputs=inputs)
        # else:
        crew.kickoff()
        print("After crew kickoff ....")
        # return (crew.get_results(),)
        # # crew.get_results()
        result = crew.kickoff()
        # print("After in crew function....")
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
                "function_calling_llm": ("LLM",),
                "tools":("TOOLLIST",),
                "max_iter": ("INT", {"default": 25,"min": 0, "max": 100, "step": 1}),
                "max_rpm": ("INT", {"default": None,"min": 0, "max": 100, "step": 1}),
                "max_execution_time": ("INT", {"default": None,"min": 0, "max": 1000, "step": 1}),
                "verbose": ("BOOLEAN", {"default": False}),
                "allow_delegation": ("BOOLEAN", {"default": True}),
                "step_callback": ("FUNCTION", {"default": None}),
                "cache": ("BOOLEAN", {"default": True}),
            }
        }
 
    RETURN_TYPES = ("AGENT",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_one_agent"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai"
 
    def set_one_agent(self,
                      role,
                      goal, 
                      backstory,
                      llm=None,
                      function_calling_llm=None,
                      tools=[],
                      max_iter=25,
                      max_rpm=None,
                      max_execution_time=None,
                      verbose=False,
                      allow_delegation=True,
                      step_callback=None,
                      cache=True
                      ):
        llm = llm if llm is not None else None
        function_calling_llm = function_calling_llm if function_calling_llm is not None else None
        tools = tools if len(tools)>0 else []
        max_rpm = max_rpm if max_rpm >0 else None
        max_execution_time = max_execution_time if max_execution_time>0 else None

        agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            llm=llm,
            function_calling_llm=function_calling_llm,
            tools=tools,
            max_iter=max_iter,
            max_rpm=max_rpm,
            max_execution_time=max_execution_time,
            verbose=verbose,
            allow_delegation=allow_delegation,
            step_callback=step_callback,
            cache=cache
                      )
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
                "tools": ("TOOLLIST",),
                "async_execution":("BOOLEAN", {"default": False}),
                "context":("TASKLIST",),
                "output_file":("STRING", {"default": "output.md"}),
                "callback":("FUNCTION", {"default": None}),
                "human_feedback":("BOOLEAN", {"default": False}),
                
            }
        }
 
    RETURN_TYPES = ("TASK",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_task"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai"
 
    def set_task(self,
                 description, 
                 agent,
                 expected_output,
                 async_execution,
                 tools=[],
                 context=[],
                 output_file="output.md",
                 callback=None,
                 human_feedback=False
                 ):
        
        tools = tools if len(tools)>0 else []
        context = context if len(context)>0 else []
        callback = callback if callback is not None else None

        task = Task(
            description=description,
            agent=agent,
            expected_output=expected_output,
            async_execution=async_execution,
            tools=tools,
            context=context,
            output_file=output_file,
            callback=callback,
            human_feedback=human_feedback
            )
        print("Excuting in task function....")
        return (task,)
    
class LLMNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base_url": ("STRING", {"default": "https://api.groq.com/openai/v1"}),
                "api_key": ("STRING", {"default": "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"}),
             },
            "optional":{
                "model": ("STRING", {"default": "llama3-70b-8192"}),
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

class AgentListNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "agent_01": ("AGENT",),
            },
            "optional": {
                "agent_02": ("AGENT",),
                "agent_03": ("AGENT",),
                "agent_04": ("AGENT",),
            }
        }
    RETURN_TYPES = ("AGENTLIST",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_agents"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai"
    
    def set_agents(self, agent_01, agent_02=None, agent_03=None, agent_04=None):
        print("within agentlist function...")
        agentList =[]
        # print("agent 01: ",agent_01)
        agentList.append(agent_01)
        if agent_02 is not None:
            agentList.append(agent_02)
        if agent_03 is not None:
            agentList.append(agent_03)
        if agent_04 is not None:
            agentList.append(agent_04)
        # print(agentList[0])    
        # print("Len of agentList: ",len(agentList))
        return (agentList,) 

class TaskListNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "task_01": ("TASK",),
            },
            "optional": {
                "task_02": ("TASK",),
                "task_03": ("TASK",),
                "task_04": ("TASK",),
            }
        }
    RETURN_TYPES = ("TASKLIST",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_tasks"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai"
    
    def set_tasks(self, task_01, task_02=None, task_03=None, task_04=None):
        print("within task list function...")
        taskList =[]
        taskList.append(task_01)
        if task_02 is not None:
            taskList.append(task_02)
        if task_03 is not None:
            taskList.append(task_03)  
        if task_04 is not None:
            taskList.append(task_04)
        # print("Len of task List: ",len(taskList))
        return (taskList,) 

class ToolsListNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "tool_01": ("TOOL",),
            },
            "optional": {
                "tool_02": ("TOOL",),
                "tool_03": ("TOOL",),
                "tool_04": ("TOOL",),
            }
        }
    RETURN_TYPES = ("TOOLLIST",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_tools"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai/tools"
    
    def set_tools(self, tool_01, tool_02=None, tool_03=None,tool_04=None):
        print("within tool list function...")
        toolList =[]
        toolList.append(tool_01)
        if tool_02 is not None:
            toolList.append(tool_02)
        if tool_03 is not None:
            toolList.append(tool_03)  
        if tool_04 is not None:
            toolList.append(tool_04)
        # print("Len of task List: ",len(toolList))
        return (toolList,)

class ContextListNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "context_01": ("TASK",),
            },
            "optional": {
                "context_02": ("TASK",),
                "context_03": ("TASK",),
                "context_04": ("TASK",),
            }
        }
    RETURN_TYPES = ("TASKLIST",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_contexts"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai"
    
    def set_contexts(self, context_01, context_02=None, context_03=None,context_04=None):
        print("within context list function...")
        contextList =[]
        contextList.append(context_01)
        if context_02 is not None:
            contextList.append(context_02)
        if context_03 is not None:
            contextList.append(context_03)  
        if context_04 is not None:
            contextList.append(context_04)
        # print("Len of task List: ",len(toolList))
        return (contextList,)
    
class SWTNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": ("STRING", {"default": "https://www.aia.com"}),                
             },
        }
 
    RETURN_TYPES = ("TOOL",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_swt"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai/tools"
 
    def set_swt(self,url):
        swt = ScrapeWebsiteTool(website_url=url)
        return (swt,)

#SerperDevTool    
class SDTNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            # "required": {
            #     "search_url": ("STRING", {"default": "https://www.aia.com"}),                
            #  },
        }
 
    RETURN_TYPES = ("TOOL",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_sdt"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai/tools"
 
    def set_sdt(self):
        sdt = SerperDevTool()
        return (sdt,)

#MDXSearchTool    
class MDXSTNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING",{"default": "/file_path"}),                
             },
        }
 
    RETURN_TYPES = ("TOOL",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_mdxst"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai/tools"
 
    def set_mdxst(self,file_path):
        mdxst = MDXSearchTool(mdx=file_path)
        return (mdxst,)
    
#FileReadTool    
class FRTNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING",{"default": "/file_path"}),                
             },
        }
 
    RETURN_TYPES = ("TOOL",)
    RETURN_NAMES = ()
 
    FUNCTION = "set_frt"
 
    OUTPUT_NODE = True
 
    CATEGORY = "Crewai/tools"
 
    def set_frt(self,file_path):
        frt = FileReadTool(file_path=file_path)
        return (frt,)
    
# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Crew": CrewNode,
    "Agent": AgentNode,
    "Task": TaskNode,
    "LLM": LLMNode,
    "AgentList": AgentListNode,
    "TaskList": TaskListNode,
    "ToolsList": ToolsListNode,
    "SWT": SWTNode,
    "SDT": SDTNode,
    "FRT": FRTNode,
    "MDXST": MDXSTNode,
    "ContextList": ContextListNode,
    # "PDFSearchTool": PDFSearchToolNode,
    # "Tool1": Tool1_Node,
}
 
# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "CrewtNode": "Node of Crew",
    "AgentNode": "Node of Agent",
    "TaskNode": "Node of Task",
    "LLMNode": "Node of LLM",
    "AgentListNode": "Node of AgentList",
    "TaskListNode": "Node of TaskList",
    "ToolsListNode": "Node of ToolsList",
    "SWTNode": "Node of SWT", 
    "SDTNode": "Node of SDT",
    "FRTNode": "Node of FRT",
    "MDSXSTNode": "Node of MDXST",
    "ContextListNode": "Node of ContextList",
    # "PDFSearchToolNode": "Node of PDFSearchTool",
    # "Tool1_Node": "Node of Tool1 Node",
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
