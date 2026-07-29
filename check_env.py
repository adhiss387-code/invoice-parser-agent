# Check which libraries are installed
libs = ["google-genai", "google-generativeai", "openai", "langchain", "crewai"]
available = []

for lib in libs:
    try:
        __import__(lib.replace("-", "_"))
        available.append(lib)
    except ImportError:
        pass

print("Available LLM Libraries:", available)

# Let's check environment keys (safely checking existence, not printing the key itself)
import os
print("GEMINI_API_KEY exists:", "GEMINI_API_KEY" in os.environ)
print("OPENAI_API_KEY exists:", "OPENAI_API_KEY" in os.environ)
