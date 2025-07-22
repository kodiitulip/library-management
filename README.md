# 📚 Library Management

Um sistema simples de gerenciamento de biblioteca criado para a
disciplina de Estrutura de Dados, utilizando Python e uma
interface de linha de comando (CLI) simples.

## ✨ Entidades Principais

- `Book` (Livro) ✅
- `Member` (Usuário) 🚧
- `Library` (Biblioteca) ✅

## ✨ Funcionalidades Principais

- Adicionar / Remover livros ✅
- Buscar livros ✅
- Emprestar / Devolver livros
- Listar livros disponíveis ✅
- Rastrear livros emprestados por membro

## 💻 Instalação e Execução

Você pode executar este projeto usando [**UV**](https://docs.astral.sh/uv)
(recomendado pela velocidade) ou o bom e velho `pip`.

### 🚀 Usando UV

1. Instale o [UV](https://docs.astral.sh/uv)
2. Clone este repositório:

   ```bash
   git clone https://github.com/kodiitulip/library-management.git
   cd library-management
   ```

3. Execute o app:

   ```bash
   uv run library --help
   ```

### 🐍 Usando pip

1. Clone este repositório:

   ```bash
   git clone https://github.com/kodiitulip/library-management.git
   cd library-management
   ```

2. *(Opcional, mas recomendado)* Crie e ative um ambiente virtual:

   - **Mac/Linux**

     ```bash
     python -m venv .venv
     source .venv/bin/activate
     ```

   - **Windows**

     ```bat
     python -m venv .venv
     .venv\Scripts\activate.bat
     ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute o app:

   ```bash
   python -m library_management
   # se estiver usando um ambiente virtual ativado
   # é possível que o seguinte comando funcione:
   library
   ```

## Usando a CLI

A aplicação é uma CLI construída com a biblioteca [Typer](https://typer.tiangolo.com/)
e em todos os comandos existe a opção `--help`, que irá imprimir os comandos e
opções disponíveis e seus formatos.

Portanto comece com:

```bash
uv run library --help
# output:
# Usage: library [OPTIONS] COMMAND [ARGS]...
#
# Ferramenta de comando para gerenciar uma biblioteca
#
# Options
# --install-completion          Install completion for the current shell.
# --show-completion             Show completion for the current shell, to copy
#                               it or customize the installation.
# --help                        Show this message and exit.
# Commands
# book   Comandos relacionados a gerenciamendo de livros
# user   Comandos para lidar com usuários
```

Caso não saiba como usar um commando:

```bash
uv run library book --help
#---#
uv run library user --help
```

Subcomandos para `book`:

```bash
library book donate   Adiciona um livro a lista da Bilioteca
library book remove   Remove um livro da lista de livros disponíveis
library book list     Lista todos os livros disponíveis na Biblioteca
library book find     Encontra um livro pelo titúlo ou pelo autor
```

Subcomandos para user:

```bash
library user list     Lista usuários cadastrados
library user add      Registra um novo usuário
library user borrow   Pegar um livro emprestado
library user return   Devolver um livro emprestado
library user track    Lista os livros emprestados pelo usuário logado
library user login    Entrar na conta de usuário
library user logout   Sair da conta atual
```

## 🧠 Notas

- Utilizamos uma Arvore de Busca Binária para armazenar os livros.
Isso permite uma busca veloz e organizada alfabeticamente
- Utilizamos um arquivo json gerado na pasta `gendata/` para
armazenar o estado da biblioteca entre comandos da interface
- Utilizamos a biblioteca [Typer](https://typer.tiangolo.com/) para
termos uma interface de linha de comando limpa e funcional
além da biblioteca [Rich](https://rich.readthedocs.io/en/stable/introduction.html)
para ter maior controle do output pro console


### Contribuições

- Kodie:
  - Iniciou o git repo e os primeiros passos usando a biblioteca Typer
  - Implementou a árvore de busca binária para armazenar os dados
  - Implementou salvamento em arquivo `json`
- Eduarda:
  - Implementou funções de usuário e acoplou com as funções existentes
    da aplicação
  - Implementou salvamento em `json` para usuários
  - Implementou função básica de "login"

## 📜 Licença

[MIT](./LICENSE)
