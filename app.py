# app.py
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q")
    resultados = []

    if query:
        # Limpa espaços em branco extras nas pontas da pesquisa
        query = query.strip()
        
        # URL da API oficial da Wikipédia em Português
        url = "https://pt.wikipedia.org/w/api.php"
        
        # Parâmetros necessários para realizar a busca interna
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "utf8": 1,
            "srlimit": 5  # Quantidade de resultados retornados
        }
        
        # Cabeçalho obrigatório para evitar bloqueios de robôs desconhecidos (User-Agent)
        headers = {
            "User-Agent": "WikiBuscaApp/1.0 (usuario@exemplo.com)"
        }
        
        try:
            # Faz a requisição HTTP para os servidores da Wikipédia
            resposta = requests.get(url, params=params, headers=headers).json()
            itens_busca = resposta.get("query", {}).get("search", [])
            
            for item in itens_busca:
                # Remove as tags HTML de destaque que a API devolve por padrão
                snippet_limpo = (
                    item['snippet']
                    .replace('<span class="searchmatch">', '')
                    .replace('</span>', '')
                    .replace('&quot;', '"')
                )
                
                # Monta o link amigável para o artigo oficial
                link_artigo = f"https://pt.wikipedia.org/wiki/{item['title'].replace(' ', '_')}"
                
                resultados.append({
                    "titulo": item["title"],
                    "resumo": snippet_limpo + "...",
                    "link": link_artigo
                })
                
        except Exception as e:
            print(f"Erro de conexão com o servidor da Wikipédia: {e}")

    return render_template("index.html", resultados=resultados, busca_anterior=query)

if __name__ == "__main__":
    # Roda o servidor local em modo de desenvolvimento
    app.run(debug=True)
    
    if __name__ == "__main__":
    app.run(host="0.0.0.5000", port=5000)