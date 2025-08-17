from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/diagnostico-fiscal")
async def diagnostico_fiscal(request: Request):
    body = await request.json()
    return {
        "sugestoes_ncm": [
            {
                "ncm": "3307.30.00",
                "descricao_ncm": "Sabonetes líquidos",
                "justificativa": "Produto de higiene pessoal infantil",
                "risco_fiscal": "Baixo",
                "tributos": {
                    "federal": {"ipi": 0, "pis": 1.65, "cofins": 7.6},
                    "estadual": {"SP": {"icms": 18, "fcp": 2}},
                    "municipal": {"iss": 0}
                }
            }
        ]
    }