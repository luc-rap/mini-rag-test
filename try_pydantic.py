from pydantic import BaseModel, Field, ValidationError

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    
ok = AskRequest(question=123)
print("Validation successful:", ok)
print("Question:", ok.question)