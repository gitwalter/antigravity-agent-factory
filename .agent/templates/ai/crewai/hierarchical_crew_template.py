"""
CrewAI Hierarchical Crew Template

This template demonstrates a hierarchical crew structure with a manager agent
coordinating worker agents to accomplish complex tasks.

Usage:
    crew = HierarchicalCrewTemplate()
    result = crew.run("Research and write a report on AI agent frameworks")
"""

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_openai import ChatOpenAI
from typing import List, Optional


class HierarchicalCrewTemplate:
    """
    Hierarchical crew with manager and worker agents.
    
    Structure:
    - Manager: Coordinates tasks and delegates to workers
    - Workers: Execute specific tasks based on their roles
    """
    
    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """
        Initialize the hierarchical crew.
        
        Args:
            llm: Language model to use (defaults to GPT-4o)
        """
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0.7)
        
        # Create agents
        self.researcher = self._create_researcher()
        self.analyst = self._create_analyst()
        self.writer = self._create_writer()
        self.manager = self._create_manager()
        
        # Create crew
        self.crew = self._create_crew()
    
    def _create_researcher(self) -> Agent:
        """Create the researcher agent."""
        return Agent(
            role="Senior Researcher",
            goal="Conduct thorough research and gather comprehensive information",
            backstory="""You are an experienced researcher with a keen eye for detail.
            You excel at finding relevant information from multiple sources and
            synthesizing it into clear, actionable insights.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self._search_tool()]
        )
    
    def _create_analyst(self) -> Agent:
        """Create the analyst agent."""
        return Agent(
            role="Data Analyst",
            goal="Analyze information and extract meaningful patterns and insights",
            backstory="""You are a skilled data analyst who excels at identifying
            trends, patterns, and key insights from complex information. You have
            a talent for turning raw data into actionable recommendations.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _create_writer(self) -> Agent:
        """Create the writer agent."""
        return Agent(
            role="Technical Writer",
            goal="Create clear, comprehensive, and engaging written content",
            backstory="""You are an expert technical writer who can transform
            complex information into clear, accessible content. You have a talent
            for structuring information logically and writing in an engaging style.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _create_manager(self) -> Agent:
        """Create the manager agent."""
        return Agent(
            role="Project Manager",
            goal="Coordinate the team and ensure high-quality deliverables",
            backstory="""You are an experienced project manager who excels at
            coordinating teams, delegating tasks, and ensuring projects are
            completed on time and to a high standard.""",
            verbose=True,
            allow_delegation=True,
            llm=self.llm
        )
    
    @tool("Search Tool")
    def _search_tool(query: str) -> str:
        """Search for information on the internet."""
        # Implement actual search functionality
        return f"Search results for: {query}"
    
    def _create_crew(self) -> Crew:
        """Create the hierarchical crew."""
        return Crew(
            agents=[self.manager, self.researcher, self.analyst, self.writer],
            process=Process.hierarchical,
            manager_llm=self.llm,
            verbose=True
        )
    
    def run(self, objective: str) -> str:
        """
        Run the crew on an objective.
        
        Args:
            objective: The high-level objective to accomplish
            
        Returns:
            The final output from the crew
        """
        # Create tasks dynamically based on objective
        research_task = Task(
            description=f"Research the following topic thoroughly: {objective}",
            expected_output="Comprehensive research findings with sources",
            agent=self.researcher
        )
        
        analysis_task = Task(
            description="Analyze the research findings and extract key insights",
            expected_output="Detailed analysis with actionable insights",
            agent=self.analyst,
            context=[research_task]
        )
        
        writing_task = Task(
            description="Create a comprehensive report based on the research and analysis",
            expected_output="Well-structured report with clear sections and conclusions",
            agent=self.writer,
            context=[research_task, analysis_task]
        )
        
        # Add tasks to crew
        self.crew.tasks = [research_task, analysis_task, writing_task]
        
        # Execute
        result = self.crew.kickoff()
        
        return result


# Example usage
if __name__ == "__main__":
    crew = HierarchicalCrewTemplate()
    
    result = crew.run(
        "AI agent frameworks in 2026: Compare LangChain, CrewAI, and AutoGen"
    )
    
    print(f"\n{'='*80}\nFinal Result:\n{'='*80}\n{result}")
