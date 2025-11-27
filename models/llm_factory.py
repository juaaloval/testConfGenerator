from typing import Any, Dict
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import logging

logger = logging.getLogger(__name__)

class LLMFactory:
    @staticmethod
    def create_llm(llm_config: Dict[str, Any]):
        """
        Creates a LangChain LLM instance based on the configuration.
        """
        model_id = llm_config.get('model_id', 'google/gemma-2b-it')
        temperature = llm_config.get('temperature', 0.7)
        max_new_tokens = llm_config.get('max_new_tokens', 512)
        device = llm_config.get('device', 'auto')

        logger.info(f"Loading model: {model_id} on {device}...")
        
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map=device,
            torch_dtype=torch.float16 if device != "cpu" else torch.float32,
        )

        logger.info("Creating transformers pipeline...")
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=True if temperature > 0 else False,
            repetition_penalty=1.1
        )

        logger.info("Wrapping in LangChain HuggingFacePipeline...")
        llm = HuggingFacePipeline(pipeline=pipe)
        logger.info("LLM initialized.")
        return llm
