# Projeto: Desenvolvimento e Análise de Segurança (CRUD com OWASP Top 10)

Este projeto implementa uma API básica em Python (Flask) para gestão de dados (CRUD) com foco na aplicação e teste de controles de segurança, conforme exigido pela seção 3 da especificação do projeto.

---

## Requisitos de Segurança e Mitigações

O projeto foi desenvolvido para mitigar as duas principais vulnerabilidades do OWASP Top 10.

### A01: Broken Access Control (Controle de Acesso Quebrado) - MITIGADO ✅

**Requisito:** Garantir que um usuário autenticado não consiga acessar dados ou funcionalidades de outros usuários sem permissão.

**Implementação:**
1.  Todo novo item criado é associado ao ID do usuário autenticado (`user_id`).
2.  Nas rotas de **Read (por ID)**, **Update** e **Delete** (`GET`, `PUT`, `DELETE /items/<id>`), o código realiza uma verificação de propriedade: `if item.user_id != current_user.id`, o acesso é negado (HTTP 403 Forbidden).

**Prova:** Testes demonstraram que, após o login do `User B`, as tentativas de `GET` ou `DELETE` no Item 1 (pertencente ao `User A`) falham com status **403 Forbidden**.

### A02: Cryptographic Failures (Falhas Criptográficas) - MITIGADO ✅

**Requisito:** Garantir que dados sensíveis (senhas) não sejam salvos em texto simples.

**Implementação:**
1.  Utilização da biblioteca **`Flask-Bcrypt`**, que implementa o algoritmo de hashing **Bcrypt** (um algoritmo moderno e resistente a ataques de força bruta).
2.  As senhas são salvas no banco de dados como um *hash* irreversível, e a verificação no login é feita comparando o hash.

**Prova:** O login bem-sucedido após o registro prova que o processo de *hashing* e verificação segura de senha está ativo.

---

## Funções CRUD Implementadas

A API fornece as quatro operações fundamentais para a gestão de itens. Todas as rotas CRUD exigem autenticação (`@login_required`).

| Operação | Método HTTP | Endpoint | Descrição | Segurança |
| :---: | :---: | :--- | :--- | :--- |
| **Create** | `POST` | `/register` | Cria um novo usuário (A02). | Pública |
| **Read All** | `GET` | `/items` | Lista **apenas** os itens do usuário logado. | **A01** |
| **Read One** | `GET` | `/items/<id>` | Busca um item pelo ID, verificando a propriedade. | **A01** |
| **Create** | `POST` | `/items` | Cria um novo item, associando-o ao `user_id` logado. | **A01** |
| **Update** | `PUT` | `/items/<id>` | Atualiza um item, verificando a propriedade. | **A01** |
| **Delete** | `DELETE` | `/items/<id>` | Deleta um item, verificando a propriedade. | **A01** |

---

## Configuração e Execução do Projeto

### Pré-requisitos
* Python 3.x
* Git
* Ambiente virtual (`venv`)

### Instalação

1.  Clone o repositório:
    ```bash
    git clone [SUA URL DO REPOSITÓRIO]
    cd [pasta do projeto]
    ```
2.  Crie e ative o ambiente virtual:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Comando para Windows PowerShell/CMD
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

### Como Rodar a Aplicação

Inicie o servidor Flask (o banco de dados `database.db` será criado automaticamente):

```bash
python app.py