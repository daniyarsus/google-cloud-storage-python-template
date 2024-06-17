import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
credentials_path = 'example.json'  # change to your :^
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

client = storage.Client()
bucket_name = 'storage-name'  # change to your bucket-name :)
bucket = client.bucket(bucket_name)


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    logging.debug(f"Uploading file: {file.filename}")
    logging.debug(f"Using credentials from: {credentials_path}")

    blob = bucket.blob(file.filename)
    try:
        blob.upload_from_file(file.file, content_type=file.content_type)
        logging.debug(f"File uploaded successfully: {file.filename}")
        return {"filename": file.filename, "url": f"https://storage.googleapis.com/{bucket_name}/{file.filename}"}
    except Exception as e:
        logging.error(f"Failed to upload file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@app.get("/download/{filename}")
async def download(filename: str):
    logging.debug(f"Downloading file: {filename}")
    try:
        blob = bucket.blob(filename)
        if not blob.exists():
            raise HTTPException(status_code=404, detail="File not found")

        def file_stream():
            with blob.open("rb") as f:
                yield from f

        content_type = blob.content_type if blob.content_type else "application/octet-stream"
        return StreamingResponse(file_stream(), media_type=content_type,
                                 headers={"Content-Disposition": f"inline; filename={filename}"})
    except Exception as e:
        logging.error(f"Failed to download file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to download file: {str(e)}")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', reload=True)
