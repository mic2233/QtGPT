# chatgpt.py
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, set_seed
import torch

model_id = "openai-community/gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_id)

device = (
    "cuda" if torch.cuda.is_available() else
    "mps"  if torch.backends.mps.is_available() else
    "cpu"
)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if device != "cpu" else torch.float32,
    device_map={"": device}
)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
set_seed(42)

def ask_gpt2(question: str, max_new: int = 120) -> str:
    prompt = f"### Question:\n{question}\n### Answer:"
    out = generator(
        prompt,
        max_new_tokens=max_new,
        pad_token_id=tokenizer.eos_token_id
    )[0]["generated_text"]
    return out.split("### Answer:")[-1].strip()

