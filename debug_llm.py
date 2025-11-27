from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

model_id = "google/gemma-2b-it"
print(f"Loading tokenizer for {model_id}...")
tokenizer = AutoTokenizer.from_pretrained(model_id)

print(f"Loading model for {model_id}...")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    dtype=torch.float32, # Force float32 for CPU safety
)

print("Creating pipeline...")
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=50,
)

print("Generating test...")
result = pipe("Say hello")
print(f"Result: {result}")
