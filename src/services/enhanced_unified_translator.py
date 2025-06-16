# src/services/enhanced_unified_translator.py
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor
from src.services.chinese_translator import ChineseTranslator
from src.utils.logger import setup_logger
from typing import Dict, Tuple, List
import time

logger = setup_logger("enhanced_unified_translator")

class EnhancedUnifiedTranslator:
    """
    Enhanced unified translation system supporting:
    - English ↔ Hindi (IndicTrans2)
    - English ↔ Urdu (IndicTrans2)  
    - English ↔ Chinese (OPUS-MT)
    
    FIXED: Enhanced multi-step language selection
    """
    
    # Simplified supported languages (no duplicates)
    SUPPORTED_LANGUAGES = {
        "eng_Latn": "English",
        "hin_Deva": "Hindi", 
        "urd_Arab": "Urdu",
        "zh": "Chinese (Simplified)"
    }
    
    # Valid direct translation pairs
    VALID_PAIRS = [
        # IndicTrans2 pairs
        ("eng_Latn", "hin_Deva"),  # English → Hindi
        ("hin_Deva", "eng_Latn"),  # Hindi → English
        ("eng_Latn", "urd_Arab"),  # English → Urdu
        ("urd_Arab", "eng_Latn"),  # Urdu → English
        # OPUS-MT pairs
        ("eng_Latn", "zh"),  # English → Chinese
        ("zh", "eng_Latn"),  # Chinese → English
    ]
    
    # IndicTrans2 model mappings
    INDICTRANS_MODELS = {
        "en_to_indic": "ai4bharat/indictrans2-en-indic-dist-200M",
        "indic_to_en": "ai4bharat/indictrans2-indic-en-dist-200M"
    }
    
    def __init__(self):
        self.device = self._get_device()
        
        # IndicTrans2 setup
        self.ip = IndicProcessor(inference=True)
        self.cached_indictrans_models = {}
        self.cached_indictrans_tokenizers = {}
        
        # Chinese translator setup
        self.chinese_translator = ChineseTranslator()
        
        logger.info(f"Enhanced Unified Translator initialized on device: {self.device}")
        logger.info(f"Supported languages: {len(self.SUPPORTED_LANGUAGES)} languages")
    
    def _get_device(self) -> str:
        """Detect and return the best available device."""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def _is_chinese_pair(self, src_lang: str, tgt_lang: str) -> bool:
        """Check if this is a Chinese translation pair."""
        return "zh" in {src_lang, tgt_lang}
    
    def _is_indictrans_pair(self, src_lang: str, tgt_lang: str) -> bool:
        """Check if this is an IndicTrans2 pair."""
        indic_langs = {"eng_Latn", "hin_Deva", "urd_Arab"}
        return src_lang in indic_langs and tgt_lang in indic_langs
    
    def _get_indictrans_model_key(self, src_lang: str, tgt_lang: str) -> str:
        """Determine which IndicTrans2 model to use."""
        if src_lang == "eng_Latn":
            return "en_to_indic"
        else:
            return "indic_to_en"
    
    def _load_indictrans_model(self, model_key: str):
        """Load and cache IndicTrans2 model and tokenizer."""
        if model_key in self.cached_indictrans_models:
            logger.info(f"Using cached IndicTrans model: {model_key}")
            return self.cached_indictrans_models[model_key], self.cached_indictrans_tokenizers[model_key]
        
        model_name = self.INDICTRANS_MODELS[model_key]
        logger.info(f"Loading IndicTrans model: {model_name}")
        
        start_time = time.time()
        try:
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                model_name, 
                trust_remote_code=True
            )
            
            # Load model with appropriate dtype
            dtype = torch.float16 if self.device != "cpu" else torch.float32
            model = AutoModelForSeq2SeqLM.from_pretrained(
                model_name,
                trust_remote_code=True,
                torch_dtype=dtype
            ).to(self.device)
            
            model.eval()
            
            # Cache the models
            self.cached_indictrans_models[model_key] = model
            self.cached_indictrans_tokenizers[model_key] = tokenizer
            
            load_time = time.time() - start_time
            logger.info(f"IndicTrans model {model_key} loaded successfully in {load_time:.2f}s")
            
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"Failed to load IndicTrans model {model_name}: {str(e)}")
            raise
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Return all supported languages."""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def get_valid_pairs(self) -> List[Tuple[str, str]]:
        """Return all valid language pairs."""
        return self.VALID_PAIRS.copy()
    
    def is_supported_pair(self, src_lang: str, tgt_lang: str) -> bool:
        """Check if language pair is supported (direct translation)."""
        return (src_lang, tgt_lang) in self.VALID_PAIRS
    
    def is_multistep_supported(self, src_lang: str, tgt_lang: str) -> bool:
        """Check if multi-step translation is possible via English."""
        if self.is_supported_pair(src_lang, tgt_lang):
            return True  # Direct translation available
        
        # Check if both languages can go through English
        english_code = "eng_Latn"
        
        # Can source go to English and English go to target?
        can_src_to_eng = self.is_supported_pair(src_lang, english_code) or src_lang == english_code
        can_eng_to_tgt = self.is_supported_pair(english_code, tgt_lang) or tgt_lang == english_code
        
        return can_src_to_eng and can_eng_to_tgt
    
    def get_available_targets(self, src_lang: str, include_multistep: bool = False) -> List[str]:
        """
        Get available target languages for a given source language.
        
        Args:
            src_lang: Source language code
            include_multistep: If True, include targets available via multi-step translation
        """
        if include_multistep:
            # Return all languages that can be reached via direct or multi-step translation
            available = []
            for lang_code in self.SUPPORTED_LANGUAGES.keys():
                if lang_code != src_lang:  # Don't include same language
                    if self.is_multistep_supported(src_lang, lang_code):
                        available.append(lang_code)
            return available
        else:
            # Return only direct translation targets
            available = []
            for src, tgt in self.VALID_PAIRS:
                if src == src_lang:
                    available.append(tgt)
            return available
    
    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """
        Translate text between any supported languages.
        Automatically routes to the appropriate translation system.
        """
        # Validation
        if not self.is_supported_pair(src_lang, tgt_lang):
            available_targets = self.get_available_targets(src_lang, include_multistep=False)
            src_name = self.SUPPORTED_LANGUAGES.get(src_lang, src_lang)
            available_names = [self.SUPPORTED_LANGUAGES.get(t, t) for t in available_targets]
            
            raise ValueError(
                f"❌ Unsupported language pair: {src_name} → {self.SUPPORTED_LANGUAGES.get(tgt_lang, tgt_lang)}\n"
                f"✅ Supported from {src_name}: {', '.join(available_names)}\n"
                f"💡 Try multi-step translation for this pair"
            )
        
        if src_lang == tgt_lang:
            return text
        
        if not text.strip():
            return text
        
        try:
            start_time = time.time()
            logger.info(f"Enhanced translation: '{text}' from {src_lang} to {tgt_lang}")
            
            # Route to appropriate translation system
            if self._is_chinese_pair(src_lang, tgt_lang):
                # Use Chinese translator (OPUS-MT)
                # Convert eng_Latn to en for Chinese translator
                norm_src = "en" if src_lang == "eng_Latn" else src_lang
                norm_tgt = "en" if tgt_lang == "eng_Latn" else tgt_lang
                result = self.chinese_translator.translate(text, norm_src, norm_tgt)
                
            elif self._is_indictrans_pair(src_lang, tgt_lang):
                # Use IndicTrans2 system
                result = self._translate_indictrans(text, src_lang, tgt_lang)
                
            else:
                raise ValueError(f"Unsupported translation: {src_lang} → {tgt_lang}")
            
            translation_time = time.time() - start_time
            logger.info(f"Enhanced translation completed in {translation_time:.2f}s: '{result}'")
            
            return result
            
        except Exception as e:
            logger.error(f"Enhanced translation failed: {str(e)}")
            raise
    
    def _translate_indictrans(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Handle IndicTrans2 translations."""
        # Get appropriate model
        model_key = self._get_indictrans_model_key(src_lang, tgt_lang)
        model, tokenizer = self._load_indictrans_model(model_key)
        
        # Preprocess using IndicProcessor
        preprocessed = self.ip.preprocess_batch(
            [text], 
            src_lang=src_lang, 
            tgt_lang=tgt_lang
        )
        
        # Tokenize
        inputs = tokenizer(
            preprocessed,
            padding="longest",
            truncation=True,
            max_length=256,
            return_tensors="pt"
        ).to(self.device)
        
        # Generate translation
        with torch.no_grad():
            generated_ids = model.generate(
                **inputs,
                max_length=256,
                num_beams=5,
                length_penalty=0.8,
                early_stopping=True,
                no_repeat_ngram_size=2
            )
        
        # Decode
        decoded = tokenizer.batch_decode(
            generated_ids, 
            skip_special_tokens=True
        )[0]
        
        # Postprocess
        translated_text = self.ip.postprocess_batch([decoded], lang=tgt_lang)[0]
        
        return translated_text.strip()
    
    def translate_multi_step(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """
        Multi-step translation for unsupported direct pairs.
        Example: Hindi → Chinese (via English)
        """
        if self.is_supported_pair(src_lang, tgt_lang):
            return self.translate(text, src_lang, tgt_lang)
        
        if not self.is_multistep_supported(src_lang, tgt_lang):
            raise ValueError(
                f"❌ Multi-step translation not available: {src_lang} → {tgt_lang}\n"
                f"💡 No path available via English"
            )
        
        logger.info(f"Multi-step translation: {src_lang} → English → {tgt_lang}")
        
        # Step 1: Source → English
        if src_lang != "eng_Latn":
            english_text = self.translate(text, src_lang, "eng_Latn")
            logger.info(f"Step 1 complete: {src_lang} → English: '{english_text}'")
        else:
            english_text = text
        
        # Step 2: English → Target
        if tgt_lang != "eng_Latn":
            final_text = self.translate(english_text, "eng_Latn", tgt_lang)
            logger.info(f"Step 2 complete: English → {tgt_lang}: '{final_text}'")
        else:
            final_text = english_text
        
        return final_text
    
    def get_model_info(self) -> Dict[str, any]:
        """Get comprehensive information about all loaded models."""
        chinese_info = self.chinese_translator.get_model_info()
        
        info = {
            "device": self.device,
            "translation_systems": ["IndicTrans2", "OPUS-MT"],
            "indictrans_loaded_models": list(self.cached_indictrans_models.keys()),
            "chinese_loaded_models": chinese_info["loaded_models"],
            "supported_languages": self.SUPPORTED_LANGUAGES,
            "valid_pairs": self.VALID_PAIRS,
            "indictrans_models": self.INDICTRANS_MODELS,
            "chinese_models": chinese_info["model_mappings"]
        }
        return info