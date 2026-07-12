#using gpt-4o-mini
#using gemini 2.5 flash


PRICING = {
    "openai": {"input": 0.15, "output": 0.60},  
    "gemini": {"input": 0.0, "output": 0.0},    
}


def calculate_cost(prompt_tokens, completion_tokens, provider_name):
    rates = PRICING.get(provider_name, {"input": 0, "output": 0})
    input_cost = (prompt_tokens / 1_000_000) * rates["input"]
    output_cost = (completion_tokens / 1_000_000) * rates["output"]
    return round(input_cost + output_cost, 6)