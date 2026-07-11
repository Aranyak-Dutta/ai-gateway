from huggingface_hub import InferenceClient
import os
"""
    using Meta Prompt guard model
"""


jailbreak_client = InferenceClient(
    model="meta-llama/Prompt-Guard-86M",
    token=os.environ.get("HF_API_TOKEN")
)


def check_jailbreak(messages):

    for message in messages:
        if message.get("role") == "user":
            user_content = message.get("content", "")

    if not user_content:
        return False

    try:
        response = jailbreak_client.text_classification(user_content)
        top_prediction = response[0]

    
        is_suspicious = top_prediction.label == "JAILBREAK"

        return is_suspicious

    except Exception as e:
        print(f"Jailbreak scan API Error: {e}")
        return False