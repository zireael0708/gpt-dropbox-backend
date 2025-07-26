from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import dropbox
from dropbox.exceptions import ApiError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# CORS konfiguracija
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tvoj Dropbox token (koristi "App Token" → "Generated access token")
DROPBOX_ACCESS_TOKEN = "tvoj_token_ovde"

# Inicijalizuj Dropbox klijent
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# -------------------------
# PROVERA FOLDERA
# -------------------------
@app.get("/check-folder/{folder_name}")
async def check_folder(folder_name: str):
    folder_path = f"/{folder_name}"
    try:
        metadata = dbx.files_get_metadata(folder_path)
        return {"exists": True, "path": metadata.path_display}
    except ApiError as e:
        if isinstance(e.error, dropbox.files.GetMetadataError) and e.error.is_path() and e.error.get_path().is_not_found():
            return {"exists": False, "path": folder_path}
        else:
            return JSONResponse(content={"detail": str(e)}, status_code=500)

# -------------------------
# LISTANJE FAJLOVA U FOLDERU
# -------------------------
@app.get("/folders")
async def list_folders():
    try:
        result = dbx.files_list_folder(path="")
        folders = [entry.name for entry in result.entries if isinstance(entry, dropbox.files.FolderMetadata)]
        return {"folders": folders}
    except Exception as e:
        return JSONResponse(content={"detail": f"Greška prilikom listanja foldera: {str(e)}"}, status_code=500)

# -------------------------
# LISTANJE SADRŽAJA U FOLDERU
# -------------------------
@app.get("/list-files/{folder_name}")
async def list_files(folder_name: str):
    try:
        result = dbx.files_list_folder(path=f"/{folder_name}")
        files = [entry.name for entry in result.entries if isinstance(entry, dropbox.files.FileMetadata)]
        return {"files": files}
    except Exception as e:
        return JSONResponse(content={"detail": f"Greška: {str(e)}"}, status_code=500)

# -------------------------
# KREIRAJ FOLDER
# -------------------------
@app.get("/create-folder/{folder_name}")
async def create_folder(folder_name: str):
    folder_path = f"/{folder_name}"
    try:
        dbx.files_create_folder_v2(folder_path)
        return {"created": True, "path": folder_path}
    except ApiError as e:
        if e.error.get_path().is_conflict():
            return {"created": False, "detail": "Folder već postoji"}
        return JSONResponse(content={"detail": str(e)}, status_code=500)

# -------------------------
# UPLOAD FAJLA U FOLDER
# -------------------------
@app.get("/upload-file/{folder_na_
