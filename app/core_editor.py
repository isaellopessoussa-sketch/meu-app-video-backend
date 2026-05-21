from moviepy.editor import VideoFileClip, concatenate_videoclips

def cortar_silencios(caminho_video_original, caminho_video_final, limite_volume=0.03):
    """
    Abre o vídeo, analisa o volume do áudio a cada 100 milissegundos
    e junta apenas as partes onde alguém está falando.
    """
    video = VideoFileClip(caminho_video_original)
    audio = video.audio
    duracao = video.duration
    intervalo = 0.1  
    cortes_bons = []
    inicio_trecho = None
    
    # Analisa o volume passo a passo
    for i in range(int(duracao / intervalo)):
        tempo_atual = i * intervalo
        fim_intervalo = min(tempo_atual + intervalo, duracao)
        volume = audio.subclip(tempo_atual, fim_intervalo).max_volume()
        
        if volume > limite_volume:
            if inicio_trecho is None:
                inicio_trecho = tempo_atual
        else:
            if inicio_trecho is not None:
                cortes_bons.append((inicio_trecho, tempo_atual))
                inicio_trecho = None
                
    if inicio_trecho is not None:
        cortes_bons.append((inicio_trecho, duracao))

    # Se o vídeo inteiro for silêncio, não corta nada para evitar erros
    if not cortes_bons:
        cortes_bons = [(0, duracao)]

    # Junta os pedaços com som e gera o novo vídeo
    clips_finais = [video.subclip(start, end) for start, end in cortes_bons]
    video_editado = concatenate_videoclips(clips_finais)
    
    # Salva o resultado final
    video_editado.write_videofile(caminho_video_final, codec="libx264", audio_codec="aac")
    
    # Fecha os arquivos para não travar a memória do celular/servidor
    video.close()
    video_editado.close()
