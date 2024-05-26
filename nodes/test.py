# from crewai import Crew,Agent,Task
# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(base_url= "http://127.0.0.1:1234/v1",api_key="whatever")

# agent = Agent(
#   role='Data Analyst',
#   goal='Extract actionable insights',
#   backstory="""You're a data analyst at a large company.
#   You're responsible for analyzing data and providing insights
#   to the business.
#   You're currently working on a project to analyze the
#   performance of our marketing campaigns.""",
# #   tools=[my_tool1, my_tool2],  # Optional, defaults to an empty list
#   llm=llm,  # Optional
# #   function_calling_llm=my_llm,  # Optional
# #   max_iter=15,  # Optional
# #   max_rpm=None, # Optional
#   verbose=True,  # Optional
#   allow_delegation=True,  # Optional
# #   step_callback=my_intermediate_step_callback,  # Optional
# #   cache=True  # Optional
# )

# task = Task(
#     description='Find and summarize the latest and most relevant news on AI',
#     agent=agent
# )

# crew = Crew(
#     agents = 
    
# )