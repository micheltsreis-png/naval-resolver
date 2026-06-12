import os
import base64
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from anthropic import Anthropic

app = FastAPI(title="Resolvedor Colégio Naval")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
    max_age=600,
)

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """Você é um professor especialista em resolver questões do Colégio Naval e concursos militares brasileiros.

Ao receber uma questão:
1. Identifique a matéria (Matemática, Física, Química, Português, História, etc.)
2. Leia o enunciado com atenção
3. Resolva passo a passo de forma clara e didática
4. Destaque a resposta final

Use linguagem simples e acessível para um estudante do ensino médio.
Se for questão de múltipla escolha, indique qual alternativa está correta e explique por que as outras estão erradas.
Se houver fórmulas, explique o que cada variável representa."""


def chamar_claude(mensagens):
    resposta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=mensagens,
    )
    return resposta.content[0].text


@app.get("/")
async def health():
    return {"status": "ok", "app": "Resolvedor Naval"}


class TextoRequest(BaseModel):
    texto: str


@app.post("/resolver")
async def resolver_texto(req: TextoRequest):
    """Resolve questão enviada como texto (JSON)."""
    if not req.texto.strip():
        raise HTTPException(status_code=400, detail="Texto vazio.")
    try:
        resolucao = chamar_claude([{"role": "user", "content": req.texto.strip()}])
        return {"resolucao": resolucao}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/resolver-imagem")
async def resolver_imagem(
    texto: str = Form(default=""),
    imagem: UploadFile = File(...),
):
    """Resolve questão enviada como imagem (multipart)."""
    try:
        conteudo = await imagem.read()
        imagem_b64 = base64.standard_b64encode(conteudo).decode("utf-8")
        media_type = imagem.content_type or "image/jpeg"

        content = []
        if texto.strip():
            content.append({"type": "text", "text": texto})
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": imagem_b64},
        })
        content.append({"type": "text", "text": "Resolva esta questão passo a passo."})

        resolucao = chamar_claude([{"role": "user", "content": content}])
        return {"resolucao": resolucao}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
