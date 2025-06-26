# 📚 Library Management

A simple mock library management system built for a Data Structures course,
using Python and a clean CLI interface.

## ✨ Core Entities

- `Book`
- `Member` (User)
- `Library`

## ✨ Core Functionality

- Add / Remove Books
- Search Books
- Borrow / Return Books
- Show Available Books
- Track Borrowed Books per Member

## 💻 Installation and Running

You can run this project either with [**UV**](https://docs.astral.sh/uv)
(recommended for speed) or using standard `pip`.

### 🚀 Using UV

1. Install [UV](https://docs.astral.sh/uv)
2. Clone this repo:

   ```bash
   git clone https://github.com/kodiitulip/library-management.git
   cd library-management
   ```

3. Run the app:

   ```bash
   uv run library --help
   ```

### 🐍 Using pip

1. Clone this repo:

   ```bash
   git clone https://github.com/kodiitulip/library-management.git
   cd library-management
   ```

2. *(Optional but recommended)* Create and activate a virtual environment:

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

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   python -m library
   # ^ if fail try:
   python src/library_management/
   ```

## 🧠 Notes

- Uses basic data structures (dicts, lists, queues, stacks) under the hood to
model system behavior.

## 📜 License

[MIT](./LICENSE) — do whatever, just don't blame me if your bookshelf
catches fire. 🔥
