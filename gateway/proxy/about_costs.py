'''I am using gpt-4o-mini 
'''
COST_PER_1M = 0.15    # dollars per 1 million input tokens
COST_PER_1M = 0.60   # dollars per 1 million output tokens

def calculate_cost(prompt_tokens, completion_tokens):
    input_cost = (prompt_tokens / 1_000_000) * COST_PER_1M
    output_cost = (completion_tokens / 1_000_000) * COST_PER_1M
    return round(input_cost + output_cost, 6)