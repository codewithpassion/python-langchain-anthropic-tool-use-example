# python-langchain-anthropic-tool-use-example

This is a demonstration on how to use the Anthropic tool or function call API with Python and Langchain.

There is a very simple, user prompt and feedback loop to interact with Claude.

The single configured tool is just a mock implementation that returns a fixed string per location.

## Installation

```bash
pip install -r requirements.txt
cp .env.example .env
```

Then add your API keys to the `.env` file.

## Usage

```bash
python main.py
```
