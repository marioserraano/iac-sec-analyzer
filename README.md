# 🛡️ AI-Powered IaC Security Analyzer

A modular, privacy-first Command Line Interface (CLI) tool that leverages local Large Language Models (LLMs) to perform semantic security static analysis on Infrastructure as Code (Terraform).

Built with **Domain-Driven Design (DDD)** principles and strict data contracts, this tool bridges the gap between traditional regex-based scanners (like Checkov) and contextual AI understanding, ensuring **Zero Data Leakage** by running inference entirely on-premises.

## 🏗️ Architecture & Tech Stack

- **Core Engine:** Python 3.13
- **Local AI Inference:** [Ollama](https://ollama.com/) (Llama 3.1)
- **Data Validation & Contracts:** Pydantic
- **LLM Output Structuring:** Instructor
- **CLI & UX:** Typer + Rich
- **HCL Parsing:** python-hcl2

### Why Local LLMs?
Infrastructure code contains highly sensitive topology data and secrets. Sending this data to third-party APIs (like OpenAI or Anthropic) violates strict compliance requirements (SOC2, HIPAA). This tool uses local models to guarantee that your proprietary IaC never leaves your machine.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running on your system.

Pull the required local model:
```bash
ollama run llama3.1

```

### 2. Installation

Clone the repository and use the included `Makefile` to set up the environment:

```bash
git clone [https://github.com/tu-usuario/iac-sec-analyzer.git](https://github.com/tu-usuario/iac-sec-analyzer.git)
cd iac-sec-analyzer
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
make install

```

### 3. Usage

Run the analyzer against a Terraform file:

```bash
make run
# Under the hood, this executes: python run.py vulnerable.tf

```

## 📂 Project Structure (src-layout)

```text
.
├── src/
│   └── iac_sec/
│       ├── analyzer/   # AI engine, prompt engineering, and LLM factory
│       ├── core/       # Singleton configuration and environment state
│       ├── models/     # Pydantic schemas acting as strict data contracts
│       ├── parser/     # HCL to dictionary translation
│       ├── reporter/   # Rich terminal UI and data visualization
│       └── cli.py      # Typer CLI entrypoint
├── tests/              # Pytest automated test suite
├── vulnerable.tf       # Example fixture with intentional misconfigurations
├── Makefile            # Task runner for standardized commands
└── run.py              # Local execution wrapper

```

## 🧪 Testing

The project uses `pytest` for unit testing, adhering to the Arrange-Act-Assert (AAA) pattern.

```bash
make test

```