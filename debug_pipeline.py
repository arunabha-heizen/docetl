import os
import sys
import json
from app.core.parser import Parser
from app.core.analyzer import Analyzer
from dotenv import load_dotenv

# Load env vars
load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python debug_pipeline.py <path_to_document>")
        # Create a dummy file for demonstration if no arg provided
        print("No file provided. Creating 'sample_consent.txt' for demonstration...")
        with open("sample_consent.txt", "w") as f:
            f.write("BOARD CONSENT\n\nThe Board of Directors of Acme Corp hereby consents to increase the authorized shares to 10,000,000.\n\nSigned: John Doe, Director\nDate: 2023-10-27")
        file_path = "sample_consent.txt"
    else:
        file_path = sys.argv[1]

    print(f"--- Processing: {file_path} ---")

    # 1. Docling Parsing
    print("\n[1] Running Docling Parser...")
    try:
        parser = Parser()
        markdown_content = parser.parse_file(file_path)
        print("--- Docling Output (Markdown) ---")
        print(markdown_content)
        print("---------------------------------")
    except Exception as e:
        print(f"Docling failed: {e}")
        return

    # 2. DocETL Analysis
    print("\n[2] Running DocETL Analyzer (Extraction)...")
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Skipping DocETL Analysis: ANTHROPIC_API_KEY not found in .env")
        print("To test DocETL, set the API key in .env")
        return

    try:
        analyzer = Analyzer()
        # We need a workflow type for the analyzer to know what to extract.
        # We'll default to a generic one or ask the user.
        # For debugging, we'll use a common one.
        workflow_type = "INCREASE_AUTHORIZED_SHARES" 
        print(f"Using Workflow Type: {workflow_type}")
        
        analysis_result = analyzer.analyze(markdown_content, workflow_type)
        print("--- DocETL Output (JSON Extraction) ---")
        print(json.dumps(analysis_result, indent=2))
        print("---------------------------------------")
    except Exception as e:
        print(f"DocETL Analysis failed: {e}")

if __name__ == "__main__":
    main()
