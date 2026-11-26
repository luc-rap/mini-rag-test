from ollama import AsyncClient

MODEL = "gemma4:e4b"

async def generate(prompt: str) -> str:
    response = await AsyncClient().generate(model=MODEL, prompt=prompt)
    # lets FastAPI serve other requests while the model is thinking
    return response['response']