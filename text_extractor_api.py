import os
from fastapi import FastAPI, Header, UploadFile, File
from fastapi.routing import APIRouter
from text_extractor import TextExtractor
import uvicorn

app = FastAPI()

@app.post("/extract_text")
async def extract_text(
    file: UploadFile = File(...),
    get_dict: bool = Header(False, description="Return a dictionary with the extracted text (XML, JSON)"),
    get_image_blocks: bool = Header(False, description="Return a list of blocks with the extracted text (Image files)"),
    ):
    """
    Suported files:
    ALL_POSSIBLE_EXTENSIONS = ["pdf", "docx", "doc", "txt", "json", "xml", "jpg", "png", "jpeg", "tiff"]

    """
    contents = await file.read()

    if not os.path.exists("./tmp"):
        os.makedirs("./tmp")

    temp_file_path = f"./tmp/{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(contents)

    extractor = TextExtractor(temp_file_path)

    try:
        return extractor.extract_text(get_dict=get_dict, get_image_blocks=get_image_blocks)
    except Exception as e:
        raise e
    finally:
        os.remove(temp_file_path)

if __name__ == '__main__':
    uvicorn.run("text_extractor_api:app", host="localhost", port=8000, workers=3)



