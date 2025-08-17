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

# Carrega o JSON original
with open("Tabela_NCM_Vigente_20250816.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    ncms = data.get("Nomenclaturas", [])

@app.post("/diagnostico-fiscal")
async def diagnostico_fiscal(request: Request):
    body = await request.json()
    descricao_produto = body.get("descricao", "").lower()

    # Busca por NCMs cuja descrição contenha palavras do produto
    sugestoes = []
    for item in ncms:
        descricao_ncm = item.get("Descricao", "").lower()
        if any(palavra in descricao_ncm for palavra in descricao_produto.split()):
            sugestoes.append({
                "ncm": item.get("Codigo"),
                "descricao_ncm": item.get("Descricao"),
                "justificativa": f"Correspondência com termo '{descricao_produto}'",
                "risco_fiscal": "Indefinido",
                "tributos": {
                    "ipi": 0,
                    "pis": 1.65,
                    "cofins": 7.6,
                    "icms": 18,
                    "fcp": 2,
                    "iss": 0
                }
            })

    # Se não encontrar nada, retorna genérico
    if not sugestoes:
        sugestoes = [{
            "ncm": ncms[0].get("Codigo"),
            "descricao_ncm": ncms[0].get("Descricao"),
            "justificativa": "Sem correspondência clara, retornando primeiro NCM",
            "risco_fiscal": "Indefinido",
            "tributos": {
                "ipi": 0,
                "pis": 1.65,
                "cofins": 7.6,
                "icms": 18,
                "fcp": 2,
                "iss": 0
            }
        }]

    return {"sugestoes_ncm": sugestoes}