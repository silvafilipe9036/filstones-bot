import tweepy
import random
from datetime import datetime
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Autenticar no Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Lê manchetes do arquivo
with open("manchetes_classificadas_2025-07-12_12-37-35.txt", "r", encoding="utf-8") as f:
    linhas = f.readlines()

posts = []
frase = ""

# Pega só as manchetes relevantes
for linha in linhas:
    if linha.strip().startswith("🎯 Classificação:"):
        if any(x in linha for x in ["Comunismo", "Censura", "Liberdade", "Direita", "Economia"]):
            categoria = linha.strip().replace("🎯 Classificação: ", "")
            post = f"{frase.strip()}\n#{categoria.replace('/', '').replace(' ', '')} #BrasilLivre 🇧🇷"
            posts.append(post)
        frase = ""
    elif linha.strip() and linha[0].isdigit():
        frase = linha.split(".", 1)[1].strip()

# Postar 1 frase aleatória
if posts:
    tweet = random.choice(posts)

    if len(tweet) > 280:
        print("⚠️ Tweet muito longo, ignorado:")
        print(tweet)
    else:
        api.update_status(tweet)
        print("✅ Postado com sucesso:")
        print(tweet)
else:
    print("⚠️ Nenhuma manchete relevante encontrada.")
