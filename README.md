# EVM Wallet Generator

## Overview

The **EVM Wallet Generator** is a Python-based tool for generating and managing Ethereum Virtual Machine (EVM) wallets. It supports both CLI and GUI modes for seed phrase generation, address derivation, and wallet export in various formats.

## Features

- Generate BIP-39-compliant seed phrases (12 or 24 words).

- Derive Ethereum addresses and private keys using the BIP-44 standard.

- Export wallet details in CSV, JSON, or TXT formats.

- Include or exclude private keys in the output.

- Interactive GUI for ease of use.

- CLI mode for advanced workflows and automation.

## Prerequisites

### Python Version

- This project is tested on Python 3.12.7 due to compatibility issues with dependencies on Python 3.13. Ensure you have Python 3.12.7 installed from the official Python website.

### C++ Build Tools

- Some libraries require C++ build tools to compile extensions. Install the Microsoft C++ Build Tools if not already installed:

  - Visit Microsoft C++ Build Tools.

  - Install the tools and ensure the environment path is updated.

## Installation

### Clone the Repository

```bash
# Clone the repository
git clone https://github.com/siggven/EVM-Wallet-Generator.git
cd EVM-Wallet-Manager
```

## Set Up Environment

1. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the Application

- GUI Mode:
  ```bash
  python gui.py
  ```
- CLI Mode:
  ```bash
  python main.py --help
  ```

## Usage

### GUI Mode

1. Run the GUI:

   python gui.py

2. Use the user-friendly interface to:

- Generate seed phrases.

- Derive addresses and private keys.

- Save outputs in CSV or JSON format.

### CLI Mode

```bash
python main.py [OPTIONS]
```

Example:

```bash
python main.py --file seed_phrases.txt --num-addresses 5 --output-format csv --output-file wallets.csv
```

**Key CLI Options:**

- `--generate`: Generate a new seed phrase.

- `--num-words`: Number of words for the seed phrase (12, 15, 18, 21, or 24).

- `--file`: File containing seed phrases to process.

- `--num-addresses`: Number of addresses to derive per seed phrase.

- `--output-format`: Output format (`csv`, `json`, or `txt`).

- `--output-file`: Path to save the output file.

- `--exclude-private-keys`: Exclude private keys from the output.

- `--interactive`: Run in interactive mode for step-by-step input.

## Security Notice

- Seed phrases and private keys are highly sensitive information.

  - Keep output files secure.
  - Do not share private keys or seed phrases.

- Consider excluding private keys (`--exclude-private-keys`) if not required.
