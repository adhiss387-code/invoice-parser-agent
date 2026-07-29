# =====================================================================
# PROJECT 1: AI Invoice Auditor - Part 4 (The Chatbot Auditor)
# This script reads your Excel/CSV ledger and lets you query it in plain English!
# =====================================================================

import os

# Load API Key from .env file
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as env_f:
        for line in env_f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ[k.strip()] = v.strip().strip("'\"")

try:
    from google import genai
except ImportError:
    print("ERROR: google-genai package is not installed. Run: pip install google-genai")
    exit()

def run_chatbot():
    csv_file = "invoice_ledger.csv"
    
    if not os.path.exists(csv_file):
        print(f"ERROR: Ledger file '{csv_file}' not found. Please run llm_agent.py first to create it.")
        return

    # Read the ledger content so we can feed it to the AI
    with open(csv_file, "r", encoding="utf-8") as f:
        ledger_data = f.read()

    print("\n==================================================")
    print("      💼 AI LEDGER AUDITOR CHATBOT ACTIVE 💼     ")
    print(" Ask any question about your invoices (e.g., 'How much")
    print(" did we spend in total?' or 'List all invoice numbers')")
    print(" Type 'exit' to quit.")
    print("==================================================\n")

    client = genai.Client()

    while True:
        question = input("Ask a question about the ledger: ").strip()
        if not question:
            continue
        if question.lower() == 'exit':
            print("Exiting chatbot. Great job auditing today!")
            break

        # System prompt instructing Gemini how to act as a financial auditor
        prompt = f"""
        You are a corporate accounting auditor. You are reviewing the following invoice ledger data:

        --- LEDGER START ---
        {ledger_data}
        --- LEDGER END ---

        Answer the user's question accurately using only the data provided in the ledger. 
        If the answer involves numbers, format it clearly as currency (e.g., $1,500.00).
        Be professional and concise.

        User Question: {question}
        """

        print("\nThinking...")
        try:
            response = client.models.generate_content(
                model='gemini-3.5-flash-lite',
                contents=prompt
            )
            print(f"\n🤖 Auditor Response:\n{response.text.strip()}")
            print("-" * 50 + "\n")
        except Exception as e:
            print(f"Error communicating with AI: {e}\n")

if __name__ == "__main__":
    run_chatbot()
