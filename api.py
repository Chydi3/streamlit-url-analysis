from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a request model
class URLRequest(BaseModel):
    url: str

@app.get("/")
def home():
    return {"message": "API is running successfully!"}

@app.post("/analyze")
def analyze_url(data: URLRequest):
    return {"url": data.url, "status": "Processed"}
