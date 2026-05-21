import shutil
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
# Importamos as duas ferramentas: o cortador e o transcritor!
from app.core_editor import cortar_silencios
from app.transcriber import gerar_legendas

app = FastAPI(title="Auto Video Editor API")

UPLOAD_DIR = "videos_originais"
OUTPUT_DIR = "videos_editados"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/editar-video/")
async def receber_e_editar_video(file: UploadFile = File(...)):
    """
    Recebe o vídeo do app, corta os silêncios automaticamente,
    gera as legendas temporizadas com IA e devolve tudo estruturado.
    """
    caminho_original = os.path.join(UPLOAD_DIR, file.filename)
    caminho_final = os.path.join(OUTPUT_DIR, f"editado_{file.filename}")
    
    # 1. Salva o vídeo enviado pelo telemóvel
    with open(caminho_original, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 2. Executa o corte automático de silêncios
        print("A cortar silêncios do vídeo...")
        cortar_silencios(caminho_original, caminho_final)
        
        # 3. Passa o vídeo editado na IA para gerar as legendas no tempo correto
        print("A gerar legendas com o Whisper...")
        legendas = gerar_legendas(caminho_final)
        
        # 4. Cria o link para baixar o vídeo
        # Nota: Numa aplicação real, o vídeo seria guardado numa nuvem (como AWS S3 ou Firebase)
        url_video_editado = f"/videos_editados/editado_{file.filename}"
        
        # Retorna a resposta completa: o link do vídeo e a lista de legendas para o Front-end desenhar no ecrã
        return JSONResponse(content={
            "mensagem": "Vídeo processado com sucesso!",
            "url_video": url_video_editado,
            "legendas": legendas
        })
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": f"Falha ao processar: {str(e)}"})
