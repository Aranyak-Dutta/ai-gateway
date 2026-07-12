import os
from openai import OpenAI
from google import genai

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def call_provider(provider_name, messages):
    """
    transferring the request to specified model
    """
    
    if provider_name == "openai":
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return {
            "reply": completion.choices[0].message.content,
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
        }
    

    elif provider_name == "gemini":
        user_text = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        response = gemini_client.models.generate_content(
            model="gemini-3.5-flash",
            contents=user_text
        )

        return {
            "reply": response.text,
            "prompt_tokens": response.usage_metadata.prompt_token_count,
            "completion_tokens": response.usage_metadata.candidates_token_count,
        }

    else:
        raise ValueError(f"Unknown provider: {provider_name}")