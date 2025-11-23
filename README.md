# API Flask com JWT, Swagger e CI/CD

Pequena API Flask com autenticao JWT, Swagger UI, pipeline CI no GitHub Actions, deploy no Render via webhook e suporte a Docker/Docker Compose.

## Endpoints
- `GET /` health check retornando `{"message": "API is running"}`.
- `GET /items` retorna lista fixa de itens.
- `GET /login` gera um JWT de exemplo.
- `POST /protected` rota protegida por JWT.
- Swagger UI em `/swagger` consumindo `static/swagger.json`.

## Requisitos locais
- Python 3.11+
- `pip install -r requirements.txt`
- Opcional: `pip install pytest` (se nao estiver no ambiente)

## Como rodar a API
```bash
python app.py
# API ouvindo na porta 1313
```

## Testes (pytest)
```bash
python -m pytest -q
```
Fixtures de teste geram client Flask e tokens JWT; cobertura inclui home, login, itens, rota protegida com/sem token e metodo nao permitido em /login.

## Docker
Build e run direto:
```bash
docker build -t flask-api .
docker run -p 1313:1313 flask-api
```

## Docker Compose
```bash
docker-compose up --build
# Porta 1313 exposta no host
```

## CI (GitHub Actions)
Workflow em `.github/workflows/ci.yml`:
- Roda pytest em Python 3.11 em `push`/`pull_request` para `main`.
- Se os testes passam, aciona deploy no Render via webhook `RENDER_DEPLOY_HOOK` (secret).

## Deploy no Render
O job `deploy_to_render` envia um POST para o webhook configurado no Render. Gere o Deploy Hook no painel do Render e salve como secret `RENDER_DEPLOY_HOOK` no repositrio.

## Estrutura
- `app.py`: API Flask com JWT e Swagger.
- `static/swagger.json`: definicao OpenAPI usada pelo Swagger UI.
- `tests/`: testes pytest e `conftest.py` para resolver importacoes.
- `Dockerfile` e `docker-compose.yml`: conteinerizacao local/DEV.
- `.github/workflows/ci.yml`: pipeline CI/CD.