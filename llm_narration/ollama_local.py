import ollama

def ask_ollama(prompt, model="qwen2.5:72b-instruct-q5_K_M"):
    response = ollama.generate(model=model, prompt=prompt, options={"temperature": 0.2})
    return response["response"]
