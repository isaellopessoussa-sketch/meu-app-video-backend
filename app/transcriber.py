import whisper

def gerar_legendas(caminho_video):
    """
    Usa a inteligência artificial Whisper para ouvir o vídeo,
    extrair o texto e descobrir o segundo exato em que cada palavra foi dita.
    """
    # Carrega o modelo de IA. O 'base' é leve e funciona bem para testes.
    modelo = whisper.load_model("base")
    
    # Processa o vídeo e pede os tempos detalhados por palavra
    print("A IA está ouvindo o vídeo...")
    resultado = modelo.transcribe(caminho_video, word_timestamps=True)
    
    palavras_detalhadas = []
    
    # Organiza o resultado para sabermos o início, fim e o texto de cada fala
    for segmento in resultado["segments"]:
        for palavra in segmento["words"]:
            palavras_detalhadas.append({
                "texto": palavra["word"].strip(),
                "inicio": palavra["start"],
                "fim": palavra["end"]
            })
            
    return palavras_detalhadas
