import json
import os
import subprocess
import re
import time
import threading
from datetime import datetime

def get_investor_prompt(investor_file_path):
    with open(investor_file_path, 'r') as f:
        content = f.read()
    # Extract content between "## Action" and "## Output format"
    match = re.search(r'## Action\s*\n(.*?)\n## Output format', content, re.DOTALL)
    if match:
        # Clean up the extracted prompt: remove leading/trailing whitespace and newlines
        prompt = match.group(1).strip()
        return prompt
    else:
        raise ValueError("Could not find '## Action' or '## Output format' sections in investor.md")

def call_gemini_cli(prompt, result_container):
    # Assuming gemini-cli is in the PATH
    command = ["gemini", "-y", "-m", "gemini-2.5-flash", "-p", prompt]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        result_container['output'] = result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error calling gemini: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        result_container['error'] = e

def spinner(stop_event, start_time):
    spinner_chars = ['-', '\\', '|', '/']
    while not stop_event.is_set():
        for char in spinner_chars:
            if stop_event.is_set():
                break
            elapsed_time = time.time() - start_time
            print(f'\rCalling Gemini to generate stock picks... {char} ({elapsed_time:.2f}s)', end='', flush=True)
            time.sleep(0.1)
    print('\r', ' ' * 60, '\r', end='', flush=True) # Clear the spinner line

def transform_stock_data(stock_data):
    transformed_data = []
    for stock in stock_data:
        # Prioritize 'name' and 'ticker' if present, otherwise use 'company_name' and 'stock_symbol'
        company_name = stock.get("name") or stock.get("company_name")
        stock_symbol = stock.get("ticker") or stock.get("stock_symbol")

        transformed_stock = {
            "stock_symbol": stock_symbol,
            "company_name": company_name,
            "current_value": stock.get("current_stock_value") or stock.get("current_value"),
            "analyst_estimated_price": stock.get("analyst_consensus_estimated_price") or stock.get("analyst_estimated_price"),
            "summary": stock.get("summary")
        }
        transformed_data.append(transformed_stock)
    return transformed_data

def generate_stock_picks():
    investor_file_path = os.path.join(os.path.dirname(__file__), '..', 'investor.md')
    print(f"Reading investor prompt from {investor_file_path}...")
    prompt = get_investor_prompt(investor_file_path)
    print("Prompt retrieved successfully.")

    # Call Gemini CLI with spinner
    result_container = {}
    stop_spinner = threading.Event()
    start_time = time.time()
    gemini_thread = threading.Thread(target=call_gemini_cli, args=(prompt, result_container))
    spinner_thread = threading.Thread(target=spinner, args=(stop_spinner, start_time))

    gemini_thread.start()
    spinner_thread.start()

    gemini_thread.join()
    stop_spinner.set()
    spinner_thread.join()

    if 'error' in result_container:
        raise result_container['error']

    gemini_output = result_container.get('output')
    if not gemini_output:
        raise ValueError("Failed to get output from Gemini CLI.")

    print("Successfully received response from Gemini.")

    # Assuming gemini_output is directly the JSON string
    # Extract only the JSON part from the gemini_output
    print("\nParsing JSON from Gemini output...")
    json_match = re.search(r'\[.*?\]', gemini_output, re.DOTALL)
    if not json_match:
        print(f"Gemini CLI Output: {gemini_output}")
        raise ValueError("No JSON array found in Gemini CLI output.")
    json_string = json_match.group(0)

    try:
        stock_data = json.loads(json_string)
        print("Successfully parsed JSON data.")
        stock_data = transform_stock_data(stock_data)
        print("Successfully transformed stock data to desired format.")
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
    print(f"\nUpdating index.json at {output_dir}...")
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
    print("index.json updated.")

    print(f"\nSaving stock picks to {output_path}...")
    with open(output_path, 'w') as f:
        json.dump(stock_data, f, indent=4)

    print(f"\nStock data generated at {output_path}")

if __name__ == "__main__":
    generate_stock_picks()
