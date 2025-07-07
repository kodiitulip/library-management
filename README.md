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

## 🧠 Notas

- Utilizamos uma Arvore de Busca Binária para armazenar os livros.
Isso permite uma busca veloz e organizada alfabeticamente
- Utilizamos um arquivo json gerado na pasta `gendata/` para
armazenar o estado da biblioteca entre comandos da interface
- Utilizamos a biblioteca [Typer](https://typer.tiangolo.com/) para
termos uma interface de linha de comando limpa e funcional
além da biblioteca [Rich](https://rich.readthedocs.io/en/stable/introduction.html)
para ter maior controle do output pro console

## 📜 Licença

[MIT](./LICENSE)
