# Text Extractor API

This API provides a single endpoint for extracting text from various types of files.

## Endpoint

### POST /extract_text

This endpoint accepts a file and extracts text from it.

#### Parameters

- `file` (file, required): The file from which to extract text. The file must be one of the following types: pdf, docx, doc, txt, json, xml, jpg, png, jpeg, tiff.
- `get_dict` (boolean, optional, default=false): If true, the API will return a dictionary with the extracted text (for XML and JSON files).
- `get_image_blocks` (boolean, optional, default=false): If true, the API will return a list of blocks with the extracted text (for image files).

#### Response

The response is a string of the extracted text, or a dictionary or list of blocks if `get_dict` or `get_image_blocks` is true, respectively.

## Running the API

To run the API, execute the following command:

```bash
uvicorn text_extractor_api:app --host localhost --port 8000 --workers 3
```

## Docker Deployment

You can also run the API inside a Docker container. Here's how you can build and run the Docker container:

## Building the Docker Image

First, you need to build the Docker image. You can do this with the `docker build` command. In the directory containing the `Dockerfile`, run the following command:

```bash
docker build -t text_extractor_api .
```
```bash
docker run -p 8000:8000 text_extractor_api
```
