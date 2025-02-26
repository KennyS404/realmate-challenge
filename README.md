
# Realmate Challenge
Este projeto foi criado para cumprir o desafio da Realmate, que consiste em desenvolver uma API que recebe eventos
(webhooks) de um sistema de atendimentos via WhatsApp, registrando conversas e mensagens em um banco de
dados SQLite, e expondo um endpoint para consultas. De forma opcional, foi criado tambem um front-end simples em
HTML/JS que lista as conversas e mensagens.
## Tecnologias
- Python 3.8+
- Django
- Django Rest Framework
- Poetry (Gerenciador de dependencias)
- SQLite (Banco de dados)
## 1. Funcionalidades
1. **Receber Webhooks em `POST /webhook/`**
 - Tipos de evento:
 - `NEW_CONVERSATION` - Cria uma nova conversa (estado inicial `OPEN`).
 - `NEW_MESSAGE` - Cria uma mensagem (SENT ou RECEIVED) numa conversa aberta.
 - `CLOSE_CONVERSATION` - Fecha a conversa (`state = CLOSED`).
2. **Listar conversas**
 - `GET /conversations/` retorna a lista de todas as conversas, com seus detalhes e mensagens.
3. **Consultar detalhes de uma conversa**
 - `GET /conversations/<uuid:conversation_id>/` retorna o estado da conversa e todas as mensagens associadas.
4. **Front-end opcional (Bonus)**
 - `GET /front/` retorna um HTML simples que, via JavaScript, consome o endpoint `/conversations/` e exibe todas as
conversas, seus estados e mensagens numa listagem.
## 3. Instalacao
### 3.1. Pre-requisitos
- Python 3.8+
- Poetry instalado (via `pip install poetry` ou seguindo a documentacao oficial)
### 3.2. Passos
1. **Clone ou faca o download do repositorio:**
 ```bash
 git clone https://github.com/SEU-USUARIO/realmate-challenge.git
 cd realmate-challenge
 ```
2. **Instale as dependencias com Poetry:**
Realmate Challenge - README
 ```bash
 poetry install
 ```
3. **Entre no shell virtual do Poetry (opcional, mas recomendado):**
 ```bash
 poetry shell
 ```
4. **Aplique as migracoes para criar o banco SQLite:**
 ```bash
 python manage.py migrate
 ```
5. **Execute o servidor de desenvolvimento:**
 ```bash
 python manage.py runserver
 ```
 A aplicacao estara disponivel em `http://127.0.0.1:8000`.
## 4. Testando a API
### 4.1. POST `/webhook/`
Exemplo (nova conversa):
```bash
curl -X POST http://127.0.0.1:8000/webhook/ -H "Content-Type: application/json" -d '{
 "type": "NEW_CONVERSATION",
 "timestamp": "2025-02-21T10:20:41.349308",
 "data": {
 "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
 }
 }'
```
### 4.2. GET `/conversations/`
```bash
curl -X GET http://127.0.0.1:8000/conversations/
```
### 4.3. GET `/conversations/<uuid>/`
```bash
Realmate Challenge - README
curl -X GET http://127.0.0.1:8000/conversations/6a41b347-8d80-4ce9-84ba-7af66f369f6a/
```
## 5. Testando o Front-end (Bonus)
Acesse `http://127.0.0.1:8000/front/` no navegador.
## 6. Regras de Negocio
- Conversa comeca em estado `OPEN`.
- Se a conversa esta `CLOSED`, nao pode receber novas mensagens.
- A mensagem precisa referenciar uma conversa existente.
## 7. Contribuicao e Fork
Para enviar o desafio, faca fork deste repositorio e altere conforme seu desenvolvimento.
## 8. Licenca
(opcional)