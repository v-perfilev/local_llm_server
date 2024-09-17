# Local LLM Server

A Flask server deploying the Llama-2 chat model with optional quantization.

## How To

1. Clone the repository:

```bash
git clone https://github.com/v-perfilev/local_llm_server.git
```

2. Install the required packages:

```bash
pip install torch torchvision transformers bitsandbytes flast
```

3. Obtain Hugging Face access token and get access to the model:
- https://huggingface.co/settings/tokens
- https://huggingface.co/meta-llama/Llama-2-7b-chat-hf

4. Set your access token to config.py
```python
HF_ACCESS_TOKEN = "FILL_IT_WITH_YOUR_OWN_ACCESS_TOKEN"
```

5. Run the server!
```bash
python server.py
```
