from flask import Flask, jsonify
import dropbox
import os
from dotenv import load_dotenv

# Učitavanje iz .env fajla
load_dotenv()

DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

app = Flask(__name__)

@app.route("/")
def index():
    return "Dropbox API test radi."

@app.route("/debug-root")
def list_root():
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        result = dbx.files_list_folder(path="")  # root App Folder

        files = []
        for entry in result.entries:
            files.append({
                "name": entry.name,
                "path_lower": entry.path_lower,
                "type": type(entry).__name__
            })

        return jsonify({"root": files})

    except dropbox.exceptions.ApiError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
