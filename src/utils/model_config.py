"""
Model configuration and paths
"""
import os
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

# Create directories if they don't exist
MODELS_DIR.mkdir(exist_ok=True)
(MODELS_DIR / "indictrans2").mkdir(exist_ok=True)
(MODELS_DIR / "opus-mt").mkdir(exist_ok=True)

# Model information
MODEL_CONFIGS = {
    "indictrans2": {
        "en_to_indic": {
            "model_id": "ai4bharat/indictrans2-en-indic-dist-200M",
            "cache_dir": str(MODELS_DIR / "indictrans2" / "en-indic")
        },
        "indic_to_en": {
            "model_id": "ai4bharat/indictrans2-indic-en-dist-200M",
            "cache_dir": str(MODELS_DIR / "indictrans2" / "indic-en")
        }
    },
    "opus_mt": {
        "en_to_zh": {
            "model_id": "Helsinki-NLP/opus-mt-en-zh",
            "cache_dir": str(MODELS_DIR / "opus-mt" / "en-zh")
        },
        "zh_to_en": {
            "model_id": "Helsinki-NLP/opus-mt-zh-en",
            "cache_dir": str(MODELS_DIR / "opus-mt" / "zh-en")
        }
    }
}

def get_model_path(model_type, model_key):
    """Get model configuration"""
    return MODEL_CONFIGS[model_type][model_key]

def get_models_directory():
    """Get models directory path"""
    return str(MODELS_DIR)
