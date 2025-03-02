import yt_dlp
import whisper

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
    """Transcreve o áudio usando Whisper."""
    modelo = whisper.load_model("small", device="cpu")  # Pode usar "tiny", "base", "small", "medium", "large"
    resultado = modelo.transcribe(arquivo_mp3)
    return resultado["text"]

# --- EXECUÇÃO ---
url = input("Digite a URL do vídeo do YouTube: ")
arquivo_mp3 = baixar_audio(url)
print(f"Áudio baixado: {arquivo_mp3}")

print("\nTranscrevendo...")
texto = transcrever_audio(arquivo_mp3)

print("\n📜 Transcrição:")
print(texto)

# Salvar a transcrição em um arquivo
with open("transcricao.txt", "w", encoding="utf-8") as f:
    f.write(texto)
print("\n✅ Transcrição salva em 'transcricao.txt'")
