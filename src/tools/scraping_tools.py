from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os
from pathlib import Path
from dotenv import load_dotenv

_project_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(_project_root / ".env")

if not os.getenv("SERPER_API_KEY"):
    raise ValueError("SERPER_API_KEY not found in environment variables. Please set it in your .env file.")

serper_tool = SerperDevTool()
scrape_website_tool = ScrapeWebsiteTool()
