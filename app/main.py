import shutil
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from app.core_editor import cortar_silencios

app = FastAPI(title="Auto Video Editor API")

# Cria as pastas para salvar os vídeos temporariamente
UPLOAD_DIR = "videos_originais"
OUTPUT_DIR = "videos_editados"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/editar-video/")
async def receber_e_editar_video(file: UploadFile = File(...)):
    """
    Recebe o arquivo de vídeo do usuário, salva no servidor,
    chama o cortador de silêncio e devolve o vídeo pronto.
    """
    caminho_original = os.path.join(UPLOAD_DIR, file.filename)
    caminho_final = os.path.join(OUTPUT_DIR, f"editado_{file.filename}")
    
    # Salva o arquivo que veio do aplicativo
    with open(caminho_original, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # Executa a edição automática
        cortar_silencios(caminho_original, caminho_final)
        
        # Envia o arquivo editado de volta
        return FileResponse(caminho_final, media_type="video/mp4", filename=f"editado_{file.filename}")
    except Exception as e:
        return {"erro": f"Falha ao processar o vídeo: {str(e)}"}
