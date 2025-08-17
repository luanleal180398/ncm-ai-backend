import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega o JSON com os NCMs
with open("Tabela_NCM_Vigente_20250816.json", "r", encoding="utf-8") as f:
    ncms = json.load(f)

@app.post("/diagnostico-fiscal")
async def diagnostico_fiscal(request: Request):
    body = await request.json()
    descricao = body.get("descricao", "").lower()

    # Busca por palavras-chave na descrição
    sugestoes = []
    for item in ncms:
        palavras = item.get("palavras_chave", [])
        if any(p in descricao for p in palavras):
            sugestoes.append(item)

    # Se não encontrar nada, retorna genérico
    if not sugestoes:
        sugestoes = [ncms[0]]

    return {"sugestoes_ncm": sugestoes}