from src.generator import generate_response
from src.utils import logger


while True:
    question = input("Enter your question (What do beetles eat?) (or 'exit' to quit): ")
    if question.lower() == "exit":
        break
    
    response = generate_response(question)
    logger.info(f"Response: {response}")
