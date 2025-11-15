import argparse
import sys
import json
import csv
import re
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv(project_root / ".env")

from src.crew import ThesisMatcherCrew

def extract_json_from_output(text):
    """Extract JSON array from text output."""
    json_match = re.search(r'\[.*\]', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            if isinstance(data, list):
                return data
            return [data]
        except json.JSONDecodeError:
            pass
    
    return []

def save_results(matches, output_dir, field, country):
    """Save results as JSON and CSV."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"matches_{field.replace(' ', '_')}_{country}_{timestamp}"
    
    json_path = output_dir / f"{base_filename}.json"
    csv_path = output_dir / f"{base_filename}.csv"
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(matches, f, indent=2, ensure_ascii=False)
    
    if matches:
        fieldnames = list(matches[0].keys())
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(matches)
    
    return json_path, csv_path

def main():
    parser = argparse.ArgumentParser(description='Find master thesis positions matching your resume')
    parser.add_argument('--country', type=str, default='Finland', help='Country to search in (default: Finland)')
    parser.add_argument('--field', type=str, default='Machine Learning', help='Field of interest (e.g., Machine Learning, AI Engineer)')
    parser.add_argument('--output-dir', type=str, default='output', help='Output directory for results (default: output)')
    parser.add_argument('--top-k', type=int, default=5, help='Number of top matches to return (default: 5)')
    
    args = parser.parse_args()
    
    crew_instance = ThesisMatcherCrew()
    crew = crew_instance.crew()

    inputs = {
        "field": args.field,
        "location": args.country,
        "top_k": args.top_k
    }

    print(f"\n🔍 Searching for master thesis positions in {args.country} related to '{args.field}'...\n")
    result = crew.kickoff(inputs=inputs)
    
    print("\n" + "="*80)
    print("PROCESSING RESULTS...")
    print("="*80)
    
    result_text = str(result)
    matches = extract_json_from_output(result_text)
    
    if not matches:
        print("\nWarning: Could not extract JSON from result. Raw output:")
        print(result_text[:500])
        matches = []
    
    if matches:
        json_path, csv_path = save_results(matches, args.output_dir, args.field, args.country)
        print(f"\nFound {len(matches)} matches!")
        print(f"📄 Results saved to:")
        print(f"   JSON: {json_path}")
        print(f"   CSV:  {csv_path}")
        
        print("\n" + "="*80)
        print("TOP MATCHES:")
        print("="*80)
        for match in matches:
            print(f"\n{match.get('rank', 'N/A')}. {match.get('title', 'N/A')}")
            print(f"   Company: {match.get('company_or_institution', 'N/A')}")
            print(f"   Fit Score: {match.get('fit_score', 'N/A')}/100")
            print(f"   URL: {match.get('url', 'N/A')}")
            if match.get('match_summary'):
                print(f"   Match: {match.get('match_summary', '')[:150]}...")
    else:
        print("\nNo matches found or could not parse results.")

if __name__ == "__main__":
    main()
