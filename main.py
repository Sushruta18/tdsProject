from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import base64
from PIL import Image
from io import BytesIO
import pytesseract
from qa_pipeline import answer_question
import os
import uvicorn

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    image: str | None = None

@app.post("/api/")
async def get_answer(data: QuestionRequest):
    image_text = ""
    if data.image:
        try:
            image_data = base64.b64decode(data.image)
            image = Image.open(BytesIO(image_data))
            image_text = pytesseract.image_to_string(image)
        except Exception:
            return JSONResponse(status_code=400, content={"error": "Invalid image"})
    
    answer, links = answer_question(data.question, image_text)
    return {"answer": answer, "links": links}

# Run app when executed directly (required for Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
