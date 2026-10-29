# Estado atual da API de orçamento

Revisão: 13/10/2026. Git inicial limpo. A etapa comprovada é a leitura estática dos contratos, cálculo e rotas; nenhum teste ou serviço foi executado.

## Arquitetura observada

[app/main.py](../app/main.py) cria FastAPI, `GET /health`, `POST /quote`, página inicial e assets estáticos. A rota de cotação recebe `QuoteRequest` e retorna `calculate_quote`. [app/models.py](../app/models.py) define entrada, detalhamento e resposta; [app/pricing.py](../app/pricing.py) concentra o cálculo. O README apresenta a proposta como demo sanitizada, sem uso de dados privados; nenhum dado de cliente ou banco foi lido.

## Regras observadas

O contrato exige custos/preços de filamento e impressora, peso e tempo positivos; energia, manutenção, trabalho e embalagem não negativos; perda entre 0 e 100; taxa de marketplace entre 0 inclusive e 100 exclusivo; quantidade mínima um. A resposta declara moeda `BRL`.

`calculate_quote` soma material, energia, depreciação, manutenção, trabalho e embalagem; aplica reserva de falha e margem de lucro, divide por `1 - taxa/100` quando existe taxa e multiplica pela quantidade. `round_money` arredonda os campos a duas casas. Fonte: [contratos](../app/models.py) e [cálculo](../app/pricing.py). Essas são regras implementadas observadas, sem certificação financeira ou aprovação por teste nesta tarefa.

## Operação

[README](../README.md) é a fonte editável para `python -m pip install -r requirements.txt`, `python -m uvicorn app.main:app --reload`, requisição `POST /quote` e `pytest`. [requirements.txt](../requirements.txt) declara FastAPI, Uvicorn, Pydantic, pytest e httpx. Todos: **não executado nesta tarefa**. Workflow e [testes](../tests/test_pricing.py) existem; sucesso de CI não foi consultado.

## Plano e lacunas

Não foi identificado roadmap aprovado nem registro de decisões a reproduzir. Sugestões para tarefa futura: (1) verificar suíte existente; (2) confirmar casos extremos de arredondamento/taxa com exemplos sintéticos; (3) revisar correspondência do formulário ao contrato. Não foi executada alteração de aplicação.

[Índice](INDEX.md).
