from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
logger = logging.getLogger(__name__)

model_id = "google/gemma-2b-it"
logger.info(f"Loading tokenizer for {model_id}...")
tokenizer = AutoTokenizer.from_pretrained(model_id)

logger.info(f"Loading model for {model_id}...")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    dtype=torch.float32, # Force float32 for CPU safety
)

logger.info("Creating pipeline...")
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=50,
)

logger.info("Generating test...")
result = pipe("Say hello")
logger.info(f"Result: {result}")
