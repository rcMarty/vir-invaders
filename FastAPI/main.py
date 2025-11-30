from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path
import uvicorn

app = FastAPI()

DATA_ROOT = Path("data")

"""
curl -X POST http://localhost:8001/upload   -F "uuid=123e4567"   -F "path=subdir/hello.txt"   -F "file=@./hello.txt"
"""
@app.post("/upload")
async def upload_file(
    uuid: str = Form(...),
    path: str = Form(...),
    file: UploadFile = File(...)
):
    safe_path = Path(path).as_posix().lstrip("/")
    target_dir = DATA_ROOT / uuid / safe_path
    target_dir.parent.mkdir(parents=True, exist_ok=True)

    target_file = target_dir

    with target_file.open("wb") as buffer:
        buffer.write(await file.read())

    return {
        "status": "ok",
        "saved_to": str(target_file)
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)