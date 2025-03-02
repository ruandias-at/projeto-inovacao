import yt_dlp

#Função que vai baixar o áudio do vídeo do youtube em webm e em seguida converter para mp3
def baixar_audio(youtube_url):
    try:
        opcoes = {
            'format': 'bestaudio/best',  # Melhor qualidade de áudio disponível
            'outtmpl': '%(title)s.%(ext)s',  # Nome do arquivo = título do vídeo
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # Qualidade do MP3
            }],
        }

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([youtube_url])
            print("Download concluído!")

    except Exception as e:
        print(f"Erro ao baixar o áudio: {e}")

# Exemplo de uso:
url = input("Digite a URL do vídeo do YouTube: ")
baixar_audio(url)
