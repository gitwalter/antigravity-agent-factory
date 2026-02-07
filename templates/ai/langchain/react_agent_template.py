"""
LangChain ReAct Agent Template

This template demonstrates a ReAct (Reasoning + Acting) agent using LangChain.
The agent interleaves thought, action, and observation in a loop to solve tasks.

Usage:
    agent = ReActAgentTemplate(tools=[search_tool, calculator_tool])
    result = agent.run("What is the population of Tokyo multiplied by 2?")
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from typing import List, Optional


class ReActAgentTemplate:
    """
    ReAct agent that combines reasoning and acting.
    
    The agent follows this pattern:
    1. Thought: Reason about what to do next
    2. Action: Select and execute a tool
    3. Observation: Observe the result
    4. Repeat until task is complete
    """
    
    def __init__(
        self,
        tools: List[Tool],
        llm: Optional[ChatOpenAI] = None,
        verbose: bool = True
    ):
        """
        Initialize the ReAct agent.
        
        Args:
            tools: List of tools available to the agent
            llm: Language model to use (defaults to GPT-4o)
            verbose: Whether to print intermediate steps
        """
        self.tools = tools
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0)
        self.verbose = verbose
        
        # Create the ReAct prompt
        self.prompt = self._create_prompt()
        
        # Create the agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        # Create the executor
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=self.verbose,
            handle_parsing_errors=True,
            max_iterations=10
        )
    
    def _create_prompt(self) -> PromptTemplate:
        """Create the ReAct prompt template."""
        template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
        
        return PromptTemplate.from_template(template)
    
    def run(self, query: str) -> str:
        """
        Run the agent on a query.
        
        Args:
            query: The question or task for the agent
            
        Returns:
            The agent's final answer
        """
        result = self.executor.invoke({"input": query})
        return result["output"]
    
    async def arun(self, query: str) -> str:
        """
        Run the agent asynchronously.
        
        Args:
            query: The question or task for the agent
            
        Returns:
            The agent's final answer
        """
        result = await self.executor.ainvoke({"input": query})
        return result["output"]


# Example usage
if __name__ == "__main__":
    from langchain.tools import DuckDuckGoSearchRun
    from langchain_community.utilities import WikipediaAPIWrapper
    from langchain.agents import Tool
    
    # Define tools
    search = DuckDuckGoSearchRun()
    wikipedia = WikipediaAPIWrapper()
    
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="Useful for searching the internet for current information"
        ),
        Tool(
            name="Wikipedia",
            func=wikipedia.run,
            description="Useful for looking up factual information on Wikipedia"
        ),
        Tool(
            name="Calculator",
            func=lambda x: str(eval(x)),
            description="Useful for mathematical calculations. Input should be a valid Python expression."
        )
    ]
    
    # Create and run agent
    agent = ReActAgentTemplate(tools=tools)
    
    result = agent.run(
        "What is the population of Tokyo according to the latest data, multiplied by 2?"
    )
    
    print(f"\nFinal Answer: {result}")
