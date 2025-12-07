import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

'''use load_dotenv to get python environment'''
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError("API key not found. Please add an API key to your environment.")

'''use argparse to get user prompt'''
parser = argparse.ArgumentParser(description="ai_agent")
parser.add_argument("prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

'''store messages'''
messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

'''client object authenitcates api key, manages sending request over the internet to google, handles receiving the data'''
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages
        )
usage = response.usage_metadata
if usage is None:
    raise RuntimeError("API request failed to execute.")

if args.verbose:
    print("--- User Prompt --")
    print(f"User prompt: {args.prompt}")

    print("\n--- Token Usage ---")
    print(f"Prompt tokens: {usage.prompt_token_count}")
    print(f"Response tokens: {usage.candidates_token_count}")
    print(f"Total Tokens: {usage.total_token_count}")

print("\n--- Response Text ---")
print(response.text)


