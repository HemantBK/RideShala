"""Quick test to verify LLM providers are working."""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
load_dotenv(Path(__file__).parent / ".env")

print(f"GROQ_API_KEY set: {bool(os.getenv('GROQ_API_KEY'))}")
print(f"HF_TOKEN set: {bool(os.getenv('HF_TOKEN'))}")
print()

async def test_groq():
    print("--- Testing Groq ---")
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
        )
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "What is the seat height of Royal Enfield Meteor 350? Reply in one line."}],
            max_tokens=100,
            temperature=0.3,
        )
        print(f"SUCCESS: {response.choices[0].message.content}")
    except Exception as e:
        print(f"FAILED: {e}")

async def test_huggingface():
    print("\n--- Testing HuggingFace ---")
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.getenv("HF_TOKEN"),
        )
        response = await client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[{"role": "user", "content": "What is the best commuter bike in India? Reply in one line."}],
            max_tokens=100,
            temperature=0.3,
        )
        print(f"SUCCESS: {response.choices[0].message.content}")
    except Exception as e:
        print(f"FAILED: {e}")

async def main():
    await test_groq()
    await test_huggingface()

asyncio.run(main())
