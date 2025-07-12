import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Dicionários de palavras-chave por categoria
categorias = {
    "Liberdade/Patriotismo": ["liberdade", "patriota", "brasil", "soberania", "verde e amarelo"],
    "Esquerda/Comunismo": ["comunismo", "pt", "esquerda", "lula", "bolivarianismo", "stf", "censura"],
    "Direita/Conservadorismo": ["direita", "bolsonaro", "valores", "família", "conservador", "deus"],
    "Justiça/Censura": ["censura", "prisão", "stf", "moraes", "toffoli", "xandão", "liberdade de expressão"],
    "Economia/Crise": ["inflação", "economia", "juros", "desemprego", "crise", "corrupção", "impostos"]
}

def classificar_manchete(texto):
    resultado = []
    for categoria, palavras in categorias.items():
        for palavra in palavras:
            if palavra.lower() in texto.lower():
                resultado.append(categoria)
                break
    return resultado or ["Indefinido"]

def coletar_manchetes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    manchetes = []

    for h2 in soup.find_all('h2'):
        texto = h2.get_text(strip=True)
        if len(texto) > 30:
            tags = classificar_manchete(texto)
            manchetes.append((texto, tags))

    return manchetes

# Roda o sistema
url = "https://www.gazetadopovo.com.br/"
manchetes = coletar_manchetes(url)

# Salvar em arquivo
agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nome_arquivo = f"manchetes_classificadas_{agora}.txt"

with open(nome_arquivo, "w", encoding="utf-8") as f:
    f.write("🧠 Análise de Manchetes:\n\n")
    for i, (texto, tags) in enumerate(manchetes, 1):
        f.write(f"{i}. {texto}\n")
        f.write(f"   🎯 Classificação: {', '.join(tags)}\n\n")

print(f"\n✅ Manchetes classificadas salvas em: {nome_arquivo}")


