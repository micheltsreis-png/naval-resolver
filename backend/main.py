import os
import base64
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from anthropic import Anthropic

app = FastAPI(title="Resolvedor Colégio Naval")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
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


@app.post("/resolver")
async def resolver(
    texto: str = Form(default=""),
    imagem: UploadFile = File(default=None),
):
    mensagens = []

    if imagem:
        conteudo_imagem = await imagem.read()
        imagem_b64 = base64.standard_b64encode(conteudo_imagem).decode("utf-8")
        media_type = imagem.content_type or "image/jpeg"

        content = []
        if texto.strip():
            content.append({"type": "text", "text": texto})
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": media_type, "data": imagem_b64},
        })
        content.append({"type": "text", "text": "Resolva esta questão passo a passo."})
        mensagens.append({"role": "user", "content": content})
    else:
        mensagens.append({"role": "user", "content": texto})

    resposta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=mensagens,
    )

    return {"resolucao": resposta.content[0].text}
