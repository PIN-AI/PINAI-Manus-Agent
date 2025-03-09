# PINAI-Manus-Agent

## Demo Video
Watch our demo video: [PINAI-Manus-Agent Demo](https://youtu.be/0lqii2_79sE)

## Installation Guide

1. Create a new conda environment:

```bash
conda create -n pinai_manus python=3.12
conda activate pinai_manus
```

2. Clone the repository:

```bash
git clone https://github.com/PIN-AI/PINAI-Manus-Agent.git
cd PINAI-Manus-Agent
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

PINAI-Manus-Agent requires configuration for the LLM API. Please follow these steps:

1. Create a `config.toml` file in the `config` directory (you can copy from the example):

```bash
cp config/config.example.toml config/config.toml
```

2. Edit `config/config.toml` to add your API key and custom settings:

```toml
# Global LLM configuration
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # Replace with your actual API key
max_tokens = 4096
temperature = 0.0

# Optional specific LLM model configuration
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # Replace with your actual API key
```

## Quick Start
Run PINAI-Manus-Agent with a single command:

```bash
python pinai_manus_agent.py
```

