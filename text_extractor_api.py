import os
from io import BytesIO
from fastapi import FastAPI, Header, UploadFile, File
from fastapi.routing import APIRouter
from fastapi.responses import StreamingResponse
from text_extractor import TextExtractor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import uvicorn
from urllib.parse import quote

app = FastAPI(docs_url="/docs")

pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))


def create_pdf(text: str) -> BytesIO:
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    p.setFont('DejaVu', 12)
    lines = text.split('\n')
    y_position = height - 50
    for line in lines:
        if y_position < 50:
            p.showPage()
            p.setFont('DejaVu', 12)
            y_position = height - 50
        p.drawString(100, y_position, line)
        y_position -= 15
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


@app.post("/extract_text")
async def extract_text(
    file: UploadFile = File(...),
    get_dict: bool = Header(
        False, description="Return a dictionary with the extracted text (XML, JSON)"),
    get_image_blocks: bool = Header(
        False, description="Return a list of blocks with the extracted text (Image files)"),
):
    """
    Suported files:
    ALL_POSSIBLE_EXTENSIONS = ["pdf", "docx", "doc", "pptx", "xlsx", "xls", "txt", "json", "xml", "jpg", "png", "djvu"] 

    """
    contents = await file.read()

    if not os.path.exists("./tmp"):
        os.makedirs("./tmp")

    temp_file_path = f"./tmp/{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(contents)

    extractor = TextExtractor(temp_file_path)

    try:
        extracted_text = extractor.extract_text(
            get_dict=get_dict, get_image_blocks=get_image_blocks)
        pdf_buffer = create_pdf(extracted_text)
        encoded_filename = quote(f"{file.filename}.pdf")
        return StreamingResponse(pdf_buffer, media_type='application/pdf', headers={"Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"})
    except Exception as e:
        raise e
    finally:
        os.remove(temp_file_path)

if __name__ == '__main__':
    uvicorn.run("text_extractor_api:app",
                host="localhost", port=8000, workers=3)


# import os
# from fastapi import FastAPI, Header, UploadFile, File
# from fastapi.routing import APIRouter
# from text_extractor import TextExtractor
# import uvicorn

# app = FastAPI()

# @app.post("/extract_text")
# async def extract_text(
#     file: UploadFile = File(...),
#     get_dict: bool = Header(False, description="Return a dictionary with the extracted text (XML, JSON)"),
#     get_image_blocks: bool = Header(False, description="Return a list of blocks with the extracted text (Image files)"),
#     ):
#     """
#     Suported files:
#     ALL_POSSIBLE_EXTENSIONS = ["pdf", "docx", "doc", "txt", "json", "xml", "jpg", "png", "jpeg", "tiff"]

#     """
#     contents = await file.read()

#     if not os.path.exists("./tmp"):
#         os.makedirs("./tmp")

#     temp_file_path = f"./tmp/{file.filename}"
#     with open(temp_file_path, "wb") as temp_file:
#         temp_file.write(contents)

#     extractor = TextExtractor(temp_file_path)

#     try:
#         return extractor.extract_text(get_dict=get_dict, get_image_blocks=get_image_blocks)
#     except Exception as e:
#         raise e
#     finally:
#         os.remove(temp_file_path)

# if __name__ == '__main__':
#     uvicorn.run("text_extractor_api:app", host="localhost", port=8000, workers=3)



