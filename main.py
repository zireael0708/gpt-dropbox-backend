import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import dropbox

load_dotenv()

DROPBOX_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
DROPBOX_FOLDER = "/Operations"  # koristi kad budeš siguran u naziv

app = FastAPI()
dbx = dropbox.Dropbox(DROPBOX_TOKEN)


@app.get("/")
def root():
    return {"status": "OK", "message": "Dropbox GPT API radi."}


@app.get("/files")
def list_files():
    try:
        files = dbx.files_list_folder(DROPBOX_FOLDER)
        return {"files": [entry.name for entry in files.entries]}
    except dropbox.exceptions.ApiError as e:
        raise HTTPException(status_code=500, detail=f"Dropbox error: {e}")


@app.get("/read")
def read_file(name: str):
    path = f"{DROPBOX_FOLDER}/{name}"
    try:
        metadata, res = dbx.files_download(path)
        content = res.content.decode("utf-8", errors="ignore")
        return {"filename": name, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška prilikom čitanja: {e}")


@app.get("/check-folder/{folder_name}")
def check_folder(folder_name: str):
    path = f"/{folder_name}"
    try:
        metadata = dbx.files_get_metadata(path)
        return {"exists": True, "path": metadata.path_display}
    except dropbox.exceptions.ApiError:
        return {"exists": False, "path": path}

@app.get("/debug-root")
def debug_root():
    try:
        files = dbx.files_list_folder(path="")
        return {"root": [entry.name for entry in files.entries]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Greška: {e}")
