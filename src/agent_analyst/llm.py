from typing import List, Optional, Union, Dict, Any
from google import genai
from google.genai import types
import logging
import os
import time
from src.shared.config import config

logger = logging.getLogger(__name__)

# Type for generation config
GenerationConfig = Union[types.GenerateContentConfig, Dict[str, Any]]

class LLMClient:
    def __init__(self) -> None:
        if not config.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY is missing!")
            raise ValueError("GEMINI_API_KEY is not set.")
        
        # Initialize the new GenAI client
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        
        # 試行モデルの優先リスト
        # 注: gemini-2.0-flash 系は無料枠が廃止(quota=0)され429になるため、
        # 現行で無料枠のある 2.5 系へ更新。最後に latest エイリアスでフォールバック。
        self.models_to_try: List[str] = [
            'gemini-2.5-flash',
            'gemini-2.5-flash-lite',
            'gemini-flash-latest'
        ]

    def generate_content(self, prompt: str, generation_config: Optional[GenerationConfig] = None) -> str:
        """
        Generates content using Gemini with exponential backoff and model fallback.
        Uses the new google-genai SDK.
        """
        for model_name in self.models_to_try:
            logger.info(f"Attempting generation with model: {model_name}")
            
            # Retry loop for a specific model
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Execute generation
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=generation_config
                    )
                    
                    if response and response.text:
                        return response.text
                        
                except Exception as e:
                    error_msg = str(e)
                    wait_time = 2 ** (attempt + 2) # Start at 4s, then 8s, 16s
                    
                    # Log the error details
                    logger.warning(f"Gemini API Error ({model_name} - Attempt {attempt+1}): {error_msg}")

                    # Detect 429 Rate Limit (Quota Exceeded)
                    if any(x in error_msg for x in ["429", "RESOURCE_EXHAUSTED", "quota"]):
                        logger.warning(f"Rate Limit hit for {model_name}. Attempting next model if available...")
                        time.sleep(2) 
                        break # Break retry loop to try next model
                    
                    # Detect 404 Model Not Found
                    if "404" in error_msg and "NOT_FOUND" in error_msg:
                        logger.warning(f"Model {model_name} not found. Switching to next model...")
                        break

                    # Detect Server Errors (5xx)
                    if any(x in error_msg for x in ["500", "503", "504"]):
                         logger.warning(f"Server Error ({model_name}). Retrying in {wait_time}s...")
                         time.sleep(wait_time)
                         continue

                    # For other unknown errors, wait and retry
                    time.sleep(wait_time)
            
        logger.error("All Gemini models and retries failed.")
        return ""

    def load_prompt(self, prompt_name: str) -> str:
        """
        Loads a prompt file from the prompts directory.
        Arguments:
            prompt_name: The filename (e.g. 'article_generation.txt')
        """
        filepath = os.path.join(config.PROMPTS_DIR, prompt_name)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {filepath}")
            return ""
        except Exception as e:
            logger.error(f"Failed to read prompt file {filepath}: {e}")
            return ""

# Singleton instance
llm_client = LLMClient()
