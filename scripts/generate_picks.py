import json
import os
import subprocess
import re
from datetime import datetime

def get_investor_prompt(investor_file_path):
    with open(investor_file_path, 'r') as f:
        content = f.read()
    # Extract content between "## Action" and "## Output format"
    match = re.search(r'## Action\s*\n(.*?)\n## Output format', content, re.DOTALL)
    if match:
        # Clean up the extracted prompt: remove leading/trailing whitespace and newlines
        prompt = match.group(1).str ip()
        return prompt
    else:
        raise ValueError("Could not find '## Action' or '## Output format' sections in investor.md")

def call_gemini_cli(prompt):
    # Assuming gemini-cli is in the PATH
    command = ["gemini", "-y", "-m", "gemini-2.5-flash", "-p", prompt]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error calling gemini: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise

def generate_stock_picks():
    investor_file_path = os.path.join(os.path.dirname(__file__), '..', 'investor.md')
    prompt = get_investor_prompt(investor_file_path)

    # Call Gemini CLI
    gemini_output = call_gemini_cli(prompt)

    # Assuming gemini_output is directly the JSON string
    # Extract only the JSON part from the gemini_output
    json_match = re.search(r'\[.*?\]', gemini_output, re.DOTALL)
    if not json_match:
        raise ValueError("No JSON array found in Gemini CLI output.")
    json_string = json_match.group(0)

    try:
        stock_data = json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from gemini-cli output: {e}")
        print(f"Gemini CLI Output: {gemini_output}")
        raise # Re-raise the exception if JSON decoding fails


    output_dir = os.path.join(os.path.dirname(__file__), '..', 'web_app', 'public', 'data')
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'picked_stocks_{timestamp}.json'
    output_path = os.path.join(output_dir, filename)

    # Update index.json
    index_path = os.path.join(output_dir, 'index.json')
    historical_files = []
    if os.path.exists(index_path):
        with open(index_path, 'r') as f:
            try:
                historical_files = json.load(f)
            except json.JSONDecodeError:
                historical_files = [] # Handle empty or malformed JSON
    
    if filename not in historical_files:
        historical_files.append(filename)
    
    with open(index_path, 'w') as f:
        json.dump(historical_files, f, indent=4)

    with open(output_path, 'w') as f:
        json.dump(stock_data, f, indent=4)

    print(f"Stock data generated at {output_path}")

if __name__ == "__main__":
    generate_stock_picks()