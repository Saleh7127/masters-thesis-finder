# Master's Thesis Position Finder

A simple Multi Agent Systems(MAS) built with CrewAI that helps to find master's thesis positions by matching the resume with available positions in specified countries and fields.

## Overview

This tool automates the process of finding master's thesis positions by:
1. **Searching** for relevant thesis positions using Google Search (via Serper API)
2. **Scraping** job posting websites for detailed descriptions
3. **Analyzing** your resume (PDF) to extract skills, experience, and interests
4. **Matching** positions with your profile using AI-powered matching
5. **Ranking** and presenting the top matches with fit scores

## Features

- 🔍 Automated job search for master's thesis positions
- 📄 Resume parsing and analysis (PDF format)
- 🤖 AI-powered matching algorithm with fit scores (0-100)
- 📊 Export results as JSON and CSV
- 🌍 Search in any country
- 🎯 Filter by field of interest (e.g., Machine Learning, AI Engineer, Computer Vision)
- ⚡ Configurable number of top matches

## Requirements

- OpenAI API key
- Serper API key
- Resume PDF file

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Saleh7127/masters-thesis-finder.git
cd masters-thesis-finder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env` (or create a new `.env` file)
   - Add your API keys:
```bash
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

4. Place your resume PDF in the `knowledge/` directory:
   - The default expected file is `knowledge/Saleh_Resume_Thesis_FI.pdf`
   - To use a different resume, update the filename in `src/crew.py`

## Getting API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key

### Serper API Key
1. Go to https://serper.dev/
2. Sign up for an account
3. Get your API key from the dashboard
4. Add it to your `.env` file

## Usage

```bash
python src/main.py \
  --field "Computer Vision" \
  --country "Sweden" \
  --top-k 10 \
  --output-dir results
```

### Command Line Arguments

- `--field` (required): Field of interest (e.g., "Machine Learning", "AI Engineer", "Data Science")
- `--country` (optional): Country to search in (default: "Finland")
- `--top-k` (optional): Number of top matches to return (default: 5)
- `--output-dir` (optional): Directory to save results (default: "output")

### Examples

```bash
# Search for AI Engineer positions in Germany
python src/main.py --field "AI Engineer" --country "Germany"

# Get top 10 matches for Data Science positions in Finland
python src/main.py --field "Data Science" --top-k 10

# Save results to custom directory
python src/main.py --field "Machine Learning" --output-dir my_results
```

## Output Format

Results are saved in two formats:

### JSON Format
```json
[
  {
    "rank": 1,
    "title": "Master's Thesis Position in Machine Learning",
    "company_or_institution": "University of Helsinki",
    "url": "https://example.com/thesis-position",
    "location": "Helsinki, Finland",
    "fit_score": 85,
    "match_summary": "Strong alignment with your ML background...",
    "required_skills_match": ["Python", "TensorFlow", "Research"],
    "preferred_skills_match": ["PyTorch", "NLP"]
  },
  ...
]
```

### CSV Format
Results are also exported as CSV with all fields as columns, making it easy to analyze in Excel or other tools.

Output files are named with timestamp:
- `matches_Machine_Learning_Finland_20241115_143022.json`
- `matches_Machine_Learning_Finland_20241115_143022.csv`

## Project Structure

```
masters-thesis-finder/
├── knowledge/                     # Resume PDF files (CrewAI knowledge source)
│   └── Saleh_Resume_Thesis_FI.pdf
├── output/                        # Generated results (JSON & CSV)
├── src/
│   ├── config/
│   │   ├── agents.yaml           # Agent configurations
│   │   └── tasks.yaml            # Task definitions
│   ├── tools/
│   │   ├── scraping_tools.py     # Serper and scraping tools
│   │   └── __init__.py
│   ├── crew.py                   # CrewAI crew definition
│   └── main.py                   # Main entry point
├── .env                          # Environment variables (not in git, see .env.example)
├── .gitignore
├── requirements.txt
└── README.md
```

## How It Works

The application uses CrewAI with multiple specialized agents:

1. **Job Searcher Agent**: Uses Serper API to search Google for thesis positions and scrapes job posting websites
2. **Job Parser Agent**: Extracts structured information from job postings (skills, requirements, etc.)
3. **Resume Parser Agent**: Analyzes your resume PDF to extract skills, experience, education, and interests
4. **Matcher Agent**: Computes fit scores by comparing job requirements with your profile

## Configuration

### Agents Configuration (`src/config/agents.yaml`)
Customize agent behavior, goals, and backstories.

### Tasks Configuration (`src/config/tasks.yaml`)
Modify task descriptions and expected outputs.

### Resume Path
Place your resume PDF in the `knowledge/` directory and update the filename in `src/crew.py`:
```python
resume_pdf = PDFKnowledgeSource(
    file_paths=["Your_Resume.pdf"],  # Update this - file must be in knowledge/ directory
    chunk_size=800,
    chunk_overlap=100
)
```

## Troubleshooting

### API Key Issues
- Ensure `.env` file exists and contains valid API keys
- Check that keys have sufficient credits/quota

### Resume Not Found
- Ensure filename in `knowledge/` matches the filename in `src/crew.py`
- Check file permissions are readable

### No Results Found
- Try different search terms
- Verify Serper API is working
- Review agent output for error messages

### JSON Parsing Errors
- The matcher agent might not be outputting valid JSON
- Check the raw output in console for debugging
- Ensure agents have clear instructions in `tasks.yaml`

## Limitations

- Requires active API keys with sufficient credits
- Search results depend on Serper API availability
- PDF parsing quality depends on resume format
- Matching accuracy depends on LLM quality and task descriptions

Note: This is a learn-and-experiment project.