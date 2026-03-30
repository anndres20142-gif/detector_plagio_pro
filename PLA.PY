from fastapi import FastAPI, UploadFile, File, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# carpeta css/js/imagenes
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/analyze/")
async def analizar(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    return {
        "similitud": 45,
        "riesgo": "MEDIO"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
