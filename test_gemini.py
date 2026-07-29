# =====================================================================
# Diagnostic script to list all available models for your API key
# =====================================================================

import os

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY environment variable is missing!")
    exit()

try:
    from google import genai
except ImportError:
    print("ERROR: google-genai package is not installed. Run: pip install google-genai")
    exit()

client = genai.Client()

print("Fetching available models for your API key...")
try:
    model_list = client.models.list()
    print("\n--- Available Models ---")
    
    # Let's inspect the first model to see what attributes it has
    first_model = None
    for m in model_list:
        first_model = m
        break
    
    if first_model:
        # Print attributes of the Model object to debug
        print(f"DEBUG: Model object type is {type(first_model)}")
        print(f"DEBUG: Available attributes are: {dir(first_model)}\n")
    
    # Just print the model names directly
    for m in model_list:
        # Check model name and print it
        name = getattr(m, "name", "NoName")
        # Extract model ID (e.g. 'gemini-2.5-flash')
        model_id = name.split('/')[-1] if '/' in name else name
        print(f"- {name} (Use: {model_id})")

except Exception as e:
    print(f"Error listing models: {e}")
