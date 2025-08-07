"""
chatgpt.py

Defines a simple GPT-2–based text-generation assistant using HuggingFace Transformers.
"""

# pylint: disable=import-error
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, set_seed
import torch

MODEL_ID = "gpt2"
TOKENIZER = AutoTokenizer.from_pretrained(MODEL_ID)
TOKENIZER.pad_token = TOKENIZER.eos_token  # use EOS as pad

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL = AutoModelForCausalLM.from_pretrained(MODEL_ID).to(DEVICE)

GENERATOR = pipeline(
    "text-generation",
    model=MODEL,
    tokenizer=TOKENIZER,
    device=0 if DEVICE == "cuda" else -1,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.1,
    max_new_tokens=100,
    pad_token_id=TOKENIZER.pad_token_id,
)

set_seed(42)


def ask_gpt2(question: str) -> str:
    """
    Generate a completion for the given user question using GPT-2.

    Args:
        question: The user's input string.

    Returns:
        The model's response text.
    """
    prompt = f"You are a helpful assistant.\nUser: {question}\nAssistant:"
    output = GENERATOR(prompt)[0]["generated_text"]
    # split off the prompt so only the assistant’s reply remains
    return output.split("Assistant:")[-1].strip()
