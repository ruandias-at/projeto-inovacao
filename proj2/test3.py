import yt_dlp
import whisper
from collections import Counter
import re
from textblob import TextBlob

def baixar_audio(youtube_url):
    """Baixa o áudio do YouTube e retorna o nome do arquivo MP3."""
    opcoes = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        nome_arquivo = f"{info['title']}.mp3"
        return nome_arquivo

def transcrever_audio(arquivo_mp3):
    """Transcreve o áudio usando Whisper e salva em um arquivo de texto."""
    modelo = whisper.load_model("small", device="cpu")
    resultado = modelo.transcribe(arquivo_mp3)
    texto = resultado["text"]

    with open("transcricao.txt", "w", encoding="utf-8") as f:
        f.write(texto)

    print("\n✅ Transcrição salva em 'transcricao.txt'")
    return texto

def analisar_texto(texto):
    """Analisa o texto: contagem de palavras, palavras-chave e sentimento."""
    palavras = re.findall(r'\b\w+\b', texto.lower())  # Normaliza e separa palavras
    contagem_palavras = len(palavras)
    contagem_caracteres = len(texto)
    palavras_mais_comuns = Counter(palavras).most_common(10)  # Top 10 palavras mais usadas

    # Análise de sentimento (usando TextBlob)
    sentimento = TextBlob(texto).sentiment.polarity
    if sentimento > 0:
        sentimento_texto = "Positivo 😊"
    elif sentimento < 0:
        sentimento_texto = "Negativo 😡"
    else:
        sentimento_texto = "Neutro 😐"

    # Criar resumo (pegando as primeiras 3 frases)
    frases = re.split(r'(?<=[.!?]) +', texto)  # Divide por pontuação
    resumo = " ".join(frases[:3]) if len(frases) > 3 else texto

    print("\n📊 Análise do Texto:")
    print(f"🔹 Total de palavras: {contagem_palavras}")
    print(f"🔹 Total de caracteres: {contagem_caracteres}")
    print(f"🔹 Palavras mais comuns: {palavras_mais_comuns}")
    print(f"🔹 Sentimento do texto: {sentimento_texto}")
    print(f"🔹 Resumo: {resumo}")

    return {
        "total_palavras": contagem_palavras,
        "total_caracteres": contagem_caracteres,
        "palavras_mais_comuns": palavras_mais_comuns,
        "sentimento": sentimento_texto,
        "resumo": resumo
    }

# --- EXECUÇÃO ---
url = input("Digite a URL do vídeo do YouTube: ")
arquivo_mp3 = baixar_audio(url)
texto_transcrito = transcrever_audio(arquivo_mp3)
analisar_texto(texto_transcrito)
