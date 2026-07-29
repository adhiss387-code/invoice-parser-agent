# =====================================================================
# PROJECT 1: AI Invoice Auditor - Part 3 (The LLM-Based Parser Agent)
# This script uses Google Gemini API to parse ANY invoice format.
#
# SETUP INSTRUCTIONS:
# 1. Install the SDK:  pip install google-genai
# 2. Get a free Gemini API key from: Google AI Studio (https://aistudio.google.com)
# 3. Set the key in your terminal before running:
#    Windows CMD:  set GEMINI_API_KEY=your_key_here
#    Windows PowerShell:  $env:GEMINI_API_KEY="your_key_here"
# =====================================================================

import os
import csv
import json

# Try to import the Google GenAI SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("WARNING: 'google-genai' library not installed. Please run: pip install google-genai")
    genai = None

def parse_with_llm(file_path):
    # Load .env file manually if it exists in the directory
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as env_f:
            for line in env_f:
                if "=" in line and not line.strip().startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

    # Check if API Key is configured
    if "GEMINI_API_KEY" not in os.environ:
        print("\nERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please set your API key in PowerShell using:")
        print("  $env:GEMINI_API_KEY=\"your_api_key_from_google_ai_studio\"")
        return

    # Check if SDK is installed
    if genai is None:
        return

    print(f"Reading invoice content from: {file_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print("Sending invoice text to Gemini AI for intelligent extraction...")
    
    # Initialize the client (automatically reads GEMINI_API_KEY from environment)
    client = genai.Client()

    # Define the prompt asking for structured JSON output
    prompt = f"""
    Analyze the following invoice text. Extract these fields:
    1. Vendor Name
    2. Invoice Number
    3. Invoice Date
    4. Total Amount Due (as a number, e.g. 1711.00)

    Format your output strictly as a JSON object with keys:
    "vendor_name", "invoice_number", "invoice_date", "total_due".
    Do not include any markdown formatting or extra text.
    
    Invoice Text:
    {content}
    """

    try:
        # Call the Gemini 3.5 Flash Lite model (less demand, more stable)
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=prompt,
        )
        
        # Parse the JSON response
        raw_text = response.text.strip()
        
        # Clean any accidental markdown codeblock formatting in response
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        
        data = json.loads(raw_text.strip())
        
        vendor_name = data.get("vendor_name", "Unknown")
        invoice_number = data.get("invoice_number", "Unknown")
        invoice_date = data.get("invoice_date", "Unknown")
        total_due = data.get("total_due", 0.0)
        
        print("\n--- AI Extracted Data ---")
        print(f"Vendor: {vendor_name}")
        print(f"Invoice Number: {invoice_number}")
        print(f"Date: {invoice_date}")
        print(f"Total Due: ${total_due}")
        
        # Save to CSV
        csv_file = "invoice_ledger.csv"
        file_exists = os.path.exists(csv_file)

        with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Vendor Name", "Invoice Number", "Invoice Date", "Total Amount Due"])
            writer.writerow([vendor_name, invoice_number, invoice_date, total_due])

        print(f"\nSuccess! AI results saved to '{csv_file}'")
        
    except Exception as e:
        print(f"An error occurred during API call or JSON parsing: {e}")

if __name__ == "__main__":
    print("--- PARSING INVOICE 1 (Standard Layout) ---")
    parse_with_llm("sample_invoice.txt")
    
    print("\n--- PARSING INVOICE 2 (Alternative Layout) ---")
    parse_with_llm("sample_invoice_2.txt")
