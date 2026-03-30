from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber
import io
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def extraer_texto(file_bytes):
    texto = ""

    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                texto += page.extract_text() or ""
    except:
        texto = file_bytes.decode(errors="ignore")

    return texto

def calcular_similitud(texto1, texto2):
    vectorizador = TfidfVectorizer()
    matriz = vectorizador.fit_transform([texto1, texto2])

    similitud = cosine_similarity(matriz[0], matriz[1])[0][0]

    return round(similitud * 100, 2)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/analyze/")
async def analizar(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    texto1 = extraer_texto(await file1.read())
    texto2 = extraer_texto(await file2.read())

    porcentaje = calcular_similitud(texto1, texto2)

    riesgo = "BAJO"

    if porcentaje >= 70:
        riesgo = "ALTO"
    elif porcentaje >= 40:
        riesgo = "MEDIO"

    return {
        "similitud": porcentaje,
        "riesgo": riesgo,
        "muestra": texto1[:1200]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
