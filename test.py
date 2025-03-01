import os
import pytube
import whisper
from transformers import pipeline

def baixar_audio(youtube_url):
    """Baixa o áudio de um vídeo do YouTube e salva como MP3."""
    yt = pytube.YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    output_path = audio_stream.download(filename="audio.mp4")
    return output_path

def transcrever_audio(audio_path):
    """Transcreve o áudio usando Whisper."""
    model = whisper.load_model("base")  # Pode usar 'small' ou 'medium' se quiser mais precisão
    result = model.transcribe(audio_path)
    return result["text"]

def analisar_texto(texto):
    """Analisa o texto usando um modelo de NLP da Hugging Face (zero custo)."""
    classifier = pipeline("sentiment-analysis")
    analise = classifier(texto)
    return analise

def main():
    url = input("Digite a URL do vídeo do YouTube: ")
    
    print("Baixando áudio...")
    audio_path = baixar_audio(url)
    
    print("Transcrevendo áudio para texto...")
    texto = transcrever_audio(audio_path)
    
    print("Texto transcrito:\n", texto)

    print("Analisando sentimento do texto...")
    resultado_analise = analisar_texto(texto)
    
    print("Resultado da análise:", resultado_analise)

    # Removendo o arquivo de áudio para não ocupar espaço
    os.remove(audio_path)

if __name__ == "__main__":
    main()
