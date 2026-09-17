# 🛡️ AI-Powered IaC Security Analyzer

A modular, privacy-first Command Line Interface (CLI) tool that leverages local Large Language Models (LLMs) to perform semantic security static analysis on Infrastructure as Code (Terraform).

Built with **Domain-Driven Design (DDD)** principles and strict data contracts, this tool bridges the gap between traditional regex-based scanners (like Checkov) and contextual AI understanding, ensuring **Zero Data Leakage** by running inference entirely on-premises.

## ✨ Key Features

- **Context-Aware Analysis:** Understands intent and architecture, catching logical flaws that regex misses.
- **Custom Policy Injection (RAG):** Enforce internal company security rules dynamically via text files.
- **Recursive Directory Scanning:** Analyzes entire infrastructure repositories seamlessly with fault tolerance.
- **CI/CD Ready:** Multi-format exports (Console, JSON, Markdown). Strictly separates UI logs (`stderr`) from pure data pipes (`stdout`).
- **Zero Data Leakage:** Powered by local models. Your proprietary IaC topology never leaves your machine.

## 🏗️ Architecture & Tech Stack

- **Core Engine:** Python 3.10+
- **Local AI Inference:** [Ollama](https://ollama.com/) (Llama 3.1)
- **Data Validation & Contracts:** Pydantic (preventing LLM hallucinations)
- **LLM Output Structuring:** Instructor
- **CLI & UX:** Typer + Rich
- **HCL Parsing:** python-hcl2

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running on your system.

Pull the required local model:
```bash
ollama run llama3.1

```

### 2. Installation

Clone the repository and set up the environment:

```bash
git clone [https://github.com/tu-usuario/iac-sec-analyzer.git](https://github.com/tu-usuario/iac-sec-analyzer.git)
cd iac-sec-analyzer
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
make install

```

### 3. Usage

The CLI supports advanced routing and multi-format outputs.

**Scan a single file or an entire directory:**

```bash
python run.py analyze ./infra/

```

**Inject custom company policies (RAG):**

```bash
python run.py analyze ./infra/ --policy rules.txt

```

**Export pure JSON for CI/CD pipelines (Output Piping):**

```bash
# UI logs are sent to stderr, ensuring report.json contains strictly valid JSON
python run.py analyze ./infra/ --format json > report.json

```

**Generate a Markdown report for Pull Requests:**

```bash
python run.py analyze ./infra/ --format markdown

```

## 📂 Project Structure (src-layout)

```text
.
├── src/
│   └── iac_sec/
│       ├── analyzer/   # AI engine, prompt engineering (RAG), and LLM factory
│       ├── core/       # Singleton configuration and environment state
│       ├── models/     # Pydantic schemas (Strict data contracts & validation)
│       ├── parser/     # HCL to dictionary translation
│       ├── reporter/   # Strategy pattern for output formats (Console, JSON, MD)
│       └── cli.py      # Typer CLI entrypoint and routing
├── infra/              # Target directory containing .tf files for testing
├── rules.txt           # Example of custom company security policies
├── tests/              # Pytest automated test suite
├── Makefile            # Task runner for standardized commands
└── run.py              # Local execution wrapper

```

## 🧪 Testing

The project uses `pytest` for unit testing, adhering to the Arrange-Act-Assert (AAA) pattern.

```bash
make test

```