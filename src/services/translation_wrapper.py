"""
Translation Wrapper Module

Provides unified interface for automatic single-step and multi-step translation routing.
Compatible with MultiLanguage Translation System v2.0.0
"""

from src.services.enhanced_unified_translator import EnhancedUnifiedTranslator
from src.utils.logger import setup_logger

logger = setup_logger("translation_wrapper")

def translate_wrapper(text: str, src_lang: str, tgt_lang: str) -> str:
    """
    Wrapper function to choose between single-step and multi-step translation.
    
    Args:
        text: Text to translate
        src_lang: Source language code (e.g., 'eng_Latn')
        tgt_lang: Target language code (e.g., 'hin_Deva')
    
    Returns:
        Translated text
    """
    translator = EnhancedUnifiedTranslator()
    if translator.is_supported_pair(src_lang, tgt_lang):
        logger.info(f"Using direct translation: {src_lang} → {tgt_lang}")
        return translator.translate(text, src_lang, tgt_lang)
    else:
        logger.info(f"Using multi-step translation: {src_lang} → {tgt_lang} via English")
        return translator.translate_multi_step(text, src_lang, tgt_lang)

class WrappedTranslator:
    """
    Custom translator for FileTranslator that uses translate_wrapper.
    """
    def __init__(self):
        self.translator = EnhancedUnifiedTranslator()
        logger.info("WrappedTranslator initialized")
    
    def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Translate using the wrapper function."""
        return translate_wrapper(text, src_lang, tgt_lang)

def print_translation(text_or_file: str, src_lang: str, tgt_lang: str, is_file: bool = False) -> None:
    """
    Test function for translation validation.
    
    Args:
        text_or_file: Text string or file path to translate
        src_lang: Source language code
        tgt_lang: Target language code
        is_file: If True, treat input as file path; else, treat as text
    """
    if is_file:
        import os
        from src.services.file_translator import FileTranslator
        file_translator = FileTranslator(translator=WrappedTranslator())
        output_path = f"translated_{os.path.basename(text_or_file)}"
        stats = file_translator.translate_file(text_or_file, output_path, src_lang, tgt_lang)
        
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Translated file: {output_path}")
        print(f"Content preview: {content[:100]}...")
        print(f"Stats: {stats}")
    else:
        result = translate_wrapper(text_or_file, src_lang, tgt_lang)
        print(f"Original: {text_or_file}")
        print(f"Translated: {result}")
