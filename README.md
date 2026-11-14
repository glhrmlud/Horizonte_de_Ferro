# 🕵️ Detetive de Caelum

> Projeto desenvolvido para a disciplina de **Resolução de Problemas Matemáticos**, da Professora [MARIA ANGELA MOSCALEWSKI ROVEREDO DOS SANTOS](https://pucpr.instructure.com/courses/70852/users/2029), da **PUCPR**.

Jogo de investigação policial que roda no terminal. Na cidade vertical de Caelum, você navega por pastas e arquivos de texto (laudos, depoimentos, registros e perícias) para descobrir **quem** cometeu o crime, **com qual arma** e **em que local**.

## Sobre o projeto

Mais informações sobre a **história**, os **personagens** e a **parte lógica** do projeto podem ser encontradas na apresentação:

👉 [Apresentação do projeto no Canva](https://canva.link/lnp9fudfwqxy6s3)

## Requisitos

- [Python 3](https://www.python.org/downloads/) instalado (confira com `python --version` ou `py --version`)
- [Git](https://git-scm.com/downloads)

## Instalação

### 1. Clone o repositório

```bash
git clone <URL-DO-REPOSITORIO>
cd <NOME-DA-PASTA-DO-PROJETO>
```

### 2. Crie o ambiente virtual (venv)

**Windows**

```bash
py -m venv venv
```

**Linux / macOS**

```bash
python3 -m venv venv
```

### 3. Ative o ambiente virtual

**Windows (PowerShell)**

```powershell
venv\Scripts\Activate.ps1
```

**Windows (Prompt de Comando)**

```bat
venv\Scripts\activate.bat
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Quando o venv estiver ativo, o terminal mostra `(venv)` no início da linha.

> **PowerShell bloqueando o script?** Rode `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e tente ativar de novo.

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

## Como executar

Entre na pasta `src` e execute o `app.py`:

```bash
cd src
py app.py
```

> Em Linux/macOS, se o comando `py` não existir, use `python3 app.py`.

## Problemas comuns

| Problema | Solução |
| --- | --- |
| `py` não é reconhecido | Use `python app.py` (Windows) ou `python3 app.py` (Linux/macOS) |
| `ModuleNotFoundError` | O venv não está ativo ou as dependências não foram instaladas. Repita os passos 3 e 4 |
| `requirements.txt` não encontrado | Rode `pip install` a partir da raiz do projeto, antes de entrar em `src` |

## Para sair do venv

```bash
deactivate
```
