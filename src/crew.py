from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource

from tools.scraping_tools import serper_tool, scrape_website_tool


@CrewBase
class ThesisMatcherCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    resume_pdf = PDFKnowledgeSource(
        file_paths=["Saleh_Resume_Thesis_FI.pdf"],
        chunk_size=800,
        chunk_overlap=100
    )

    @agent
    def job_searcher(self):
        return Agent(
            config=self.agents_config["job_searcher"],
            tools=[serper_tool, scrape_website_tool],
            verbose=True
        )

    @agent
    def job_parser(self):
        return Agent(
            config=self.agents_config["job_parser"],
            verbose=True
        )

    @agent
    def resume_parser(self):
        return Agent(
            config=self.agents_config["resume_parser"],
            knowledge_sources=[self.resume_pdf],
            verbose=True
        )

    @agent
    def matcher(self):
        return Agent(
            config=self.agents_config["matcher"],
            verbose=True
        )

    @task
    def search_jobs_task(self):
        return Task(config=self.tasks_config["search_jobs_task"])

    @task
    def parse_jobs_task(self):
        return Task(config=self.tasks_config["parse_jobs_task"])

    @task
    def parse_resume_task(self):
        return Task(config=self.tasks_config["parse_resume_task"])

    @task
    def match_jobs_task(self):
        return Task(config=self.tasks_config["match_jobs_task"])

    def crew(self):
        return Crew(
            agents=[
                self.job_searcher(),
                self.job_parser(),
                self.resume_parser(),
                self.matcher(),
            ],
            tasks=[
                self.search_jobs_task(),
                self.parse_jobs_task(),
                self.parse_resume_task(),
                self.match_jobs_task(),
            ],
            process=Process.sequential,
            verbose=True
        )
