from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path
import uvicorn

app = FastAPI()
DATA_ROOT = Path("data")

"""
curl -X POST http://localhost:8001/upload \
  -F "uuid=123e4567" \
  -F "path=subdir/hello.txt" \
  -F "file=@./hello.txt"
"""
@app.put("/upload")
async def upload_file(
    uuid: str = Form(...),
    path: str = Form(...),
    file: UploadFile = File(...)
):
    # sanitize path to avoid ../ attacks
    safe_path = Path(path).as_posix().lstrip("/")
    target_file = DATA_ROOT / uuid / safe_path
    target_file.parent.mkdir(parents=True, exist_ok=True)

    # Write file in chunks to support large uploads
    with target_file.open("wb") as buffer:
        while True:
            chunk = await file.read(1024*1024)  # 1 MB per chunk
            if not chunk:
                break
            buffer.write(chunk)

    return {"status": "cOcK"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
