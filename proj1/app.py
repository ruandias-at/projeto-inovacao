from flask import Flask, render_template, request
import requests
from config import TMDB_API_KEY

app = Flask(__name__)

# Função para buscar filmes similares no TMDb
def buscar_recomendacoes(filme):
    url_busca = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={filme}&language=pt-BR"
    resposta = requests.get(url_busca).json()
    
    if resposta["results"]:
        filme_id = resposta["results"][0]["id"]
        url_recomendacoes = f"https://api.themoviedb.org/3/movie/{filme_id}/similar?api_key={TMDB_API_KEY}&language=pt-BR"
        recomendacoes = requests.get(url_recomendacoes).json()

        for item in recomendacoes["results"]:
            if item.get("poster_path"):
                item["poster_url"] = f"https://image.tmdb.org/t/p/w500{item['poster_path']}"
            else:
                item["poster_url"] = "https://via.placeholder.com/200x300?text=Sem+Imagem"

        return recomendacoes["results"]
    
    return []


# Rota principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        filme = request.form["filme"]
        recomendacoes = buscar_recomendacoes(filme)
        return render_template("resultado.html", filme=filme, recomendacoes=recomendacoes)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
