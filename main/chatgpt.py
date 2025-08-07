# chatgpt.py
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, set_seed
import torch

model_id = "gpt2"  # or whatever GPT-2 variant you're using
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token_id  # ensure padding works

device = (
    "cuda" if torch.cuda.is_available() else
    "mps"  if torch.backends.mps.is_available() else
    "cpu"
)
model = AutoModelForCausalLM.from_pretrained(model_id).to(device)

# enable sampling + sensible defaults
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=0 if device=="cuda" else -1,
    # NEW PARAMS ↓
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.1,
    max_new_tokens=100,
    pad_token_id=tokenizer.eos_token_id
)

set_seed(42)

def ask_gpt2(question: str) -> str:
    # use a chat-like prefix
    prompt = (
        "You are a helpful assistant.\n"
        f"User: {question}\n"
        "Assistant:"
    )
    out = generator(prompt)[0]["generated_text"]
    # strip off the prefix
    return out.split("Assistant:")[-1].strip()

# Example
print(ask_gpt2("hi"))
