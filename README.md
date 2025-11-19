# Industrial Control Philosophy AI (100% Free & Local)

Reverse-engineers how your plant actually works from InfluxDB / TimescaleDB data.

Features
- Automatically discovers rules like "When Level > 80% → Pump P-101 starts"
- Generates beautiful control narratives & pseudo-ladder logic
- Runs completely offline with Ollama + Llama 3.1 70B or Qwen2.5-72B
- Streamlit chat interface: ask "How is valve XV-201 controlled?"

## One-time setup (15 minutes)
```bash
# 1. Install Ollama (if not already)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:72b-instruct-q5_K_M    # or llama3.1:70b

# 2. Python environment
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 3. Edit config.yaml with your DB credentials and tag names
