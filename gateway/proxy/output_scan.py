from huggingface_hub import InferenceClient
import os

toxicity_client = InferenceClient(
    model="unitary/toxic-bert",
    token=os.environ.get("HF_API_TOKEN")
)

def check_output(ai_response_text):
    """
    Returns (is_unsafe: bool, risk_score: float)
    Scans the AI's response for toxic/harmful content before it reaches the user.
    """
    if not ai_response_text:
        return False, 0.0

    try:
        response = toxicity_client.text_classification(ai_response_text)
        top_prediction = response[0]


        is_unsafe = top_prediction.label == "toxic" and top_prediction.score > 0.7
    

        return is_unsafe

    except Exception as e:
        print(f"Output scan API Error: {e}")
        return False, 0.0