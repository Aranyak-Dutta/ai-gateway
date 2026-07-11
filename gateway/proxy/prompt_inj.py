from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    model="protectai/deberta-v3-base-prompt-injection-v2",
    token= os.environ.get("HF_API_TOKEN")
    
)
def check_prompt(messages) -> bool:

    #checks for prompt injection
    for message in messages:
        if message.get("role") == "user":
            user_content = message.get("content", "")
        
    if not user_content:
        return False, 0.0
        

    try:
        response = client.text_classification(user_content)
        top_prediction = response[0]

        is_suspicious = top_prediction.label == "INJECTION"

        return is_suspicious

    except Exception as e:
        print(f"API Error: {e}")
        return False, 0.0

# Test it out