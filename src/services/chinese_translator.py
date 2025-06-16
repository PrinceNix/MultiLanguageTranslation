# src/services/chinese_translator.py
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from src.utils.logger import setup_logger
import time

logger = setup_logger("chinese_translator")

class ChineseTranslator:
    """
    Chinese translation service using Helsinki-NLP OPUS-MT models.
    Supports English ↔ Chinese (Simplified) translation.
    """
    
    # Model mappings for Chinese translation
    MODELS = {
        "en_to_zh": "Helsinki-NLP/opus-mt-en-zh",
        "zh_to_en": "Helsinki-NLP/opus-mt-zh-en"
    }
    
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "zh": "Chinese (Simplified)"
    }
    
    VALID_PAIRS = [
        ("en", "zh"),  # English → Chinese
        ("zh", "en"),  # Chinese → English
    ]
    
    def __init__(self):
        self.device = self._get_device()
        
        # Model and tokenizer cache (same pattern as existing UnifiedTranslator)
        self.cached_models = {}
        self.cached_tokenizers = {}
        
        logger.info(f"Chinese Translator initialized on device: {self.device}")
        logger.info(f"Supported languages: {list(self.SUPPORTED_LANGUAGES.keys())}")
    
    def _get_device(self) -> str:
        """Detect and return the best available device (same as existing system)."""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def _get_model_key(self, src_lang: str, tgt_lang: str) -> str:
        """Determine which model to use based on language pair."""
        if src_lang == "en" and tgt_lang == "zh":
            return "en_to_zh"
        elif src_lang == "zh" and tgt_lang == "en":
            return "zh_to_en"
        else:
            raise ValueError(f"Unsupported language pair: {src_lang} → {tgt_lang}")
    
    def _load_model(self, model_key: str):
        """Load and cache model and tokenizer (same pattern as existing system)."""
        if model_key in self.cached_models:
            logger.info(f"Using cached Chinese model: {model_key}")
            return self.cached_models[model_key], self.cached_tokenizers[model_key]
        
        model_name = self.MODELS[model_key]
        logger.info(f"Loading Chinese model: {model_name}")
        
        start_time = time.time()
        try:
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            
            # Load model with appropriate dtype (same as existing system)
            dtype = torch.float16 if self.device != "cpu" else torch.float32
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                torch_dtype=dtype
            ).to(self.device)
            
            model.eval()
            
            # Cache the models
            self.cached_models[model_key] = model
            self.cached_tokenizers[model_key] = tokenizer
            
            load_time = time.time() - start_time
            logger.info(f"Chinese model {model_key} loaded successfully in {load_time:.2f}s")
            
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"Failed to load Chinese model {model_name}: {str(e)}")
            raise
    
    def is_supported_pair(self, src_lang: str, tgt_lang: str) -> bool:
        """Check if language pair is supported."""
        return (src_lang, tgt_lang) in self.VALID_PAIRS
    
    def get_supported_languages(self):
        """Get supported languages (consistent with existing system interface)."""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def get_available_targets(self, src_lang: str):
        """Get available target languages for a given source language."""
        available = []
        for src, tgt in self.VALID_PAIRS:
            if src == src_lang:
                available.append(tgt)
        return available
    
    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """
        Translate text between English and Chinese.
        
        Args:
            text: Text to translate
            src_lang: Source language code ("en" or "zh")
            tgt_lang: Target language code ("en" or "zh")
            
        Returns:
            Translated text
        """
        # Validation (same pattern as existing system)
        if not self.is_supported_pair(src_lang, tgt_lang):
            available_targets = self.get_available_targets(src_lang)
            src_name = self.SUPPORTED_LANGUAGES.get(src_lang, src_lang)
            available_names = [self.SUPPORTED_LANGUAGES.get(t, t) for t in available_targets]
            
            raise ValueError(
                f"❌ Unsupported language pair: {src_name} → {self.SUPPORTED_LANGUAGES.get(tgt_lang, tgt_lang)}\n"
                f"✅ Supported from {src_name}: {', '.join(available_names)}"
            )
        
        if src_lang == tgt_lang:
            return text
        
        if not text.strip():
            return text
        
        try:
            start_time = time.time()
            logger.info(f"Translating Chinese: '{text}' from {src_lang} to {tgt_lang}")
            
            # Get appropriate model
            model_key = self._get_model_key(src_lang, tgt_lang)
            model, tokenizer = self._load_model(model_key)
            
            # Tokenize (no special preprocessing needed for OPUS-MT)
            inputs = tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            ).to(self.device)
            
            # Generate translation (same parameters as existing system)
            with torch.no_grad():
                generated_ids = model.generate(
                    **inputs,
                    max_length=512,
                    num_beams=4,
                    length_penalty=0.8,
                    early_stopping=True,
                    no_repeat_ngram_size=2
                )
            
            # Decode (no special postprocessing needed)
            translated_text = tokenizer.decode(
                generated_ids[0], 
                skip_special_tokens=True
            )
            
            translation_time = time.time() - start_time
            logger.info(f"Chinese translation completed in {translation_time:.2f}s: '{translated_text}'")
            
            return translated_text.strip()
            
        except Exception as e:
            logger.error(f"Chinese translation failed: {str(e)}")
            raise
    
    def get_model_info(self):
        """Get information about loaded Chinese models (consistent with existing system)."""
        return {
            "device": self.device,
            "loaded_models": list(self.cached_models.keys()),
            "supported_languages": self.SUPPORTED_LANGUAGES,
            "valid_pairs": self.VALID_PAIRS,
            "model_mappings": self.MODELS
        }