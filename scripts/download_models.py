#!/usr/bin/env python3
"""
Download all models to local directory
This script downloads all translation models to the models/ directory
"""
import os
import sys
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from src.utils.model_config import MODEL_CONFIGS, MODELS_DIR

def download_model(model_id, cache_dir):
    """Download a single model"""
    print(f"📥 Downloading: {model_id}")
    
    try:
        start_time = time.time()
        
        # Create directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Download tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            cache_dir=cache_dir,
            trust_remote_code=True
        )
        
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_id,
            cache_dir=cache_dir,
            trust_remote_code=True
        )
        
        # Save to ensure files are in our directory
        tokenizer.save_pretrained(cache_dir)
        model.save_pretrained(cache_dir)
        
        elapsed_time = time.time() - start_time
        
        # Calculate directory size
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(cache_dir):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        
        size_mb = total_size / (1024 * 1024)
        print(f"✅ Downloaded {model_id} ({size_mb:.0f} MB) in {elapsed_time:.1f}s")
        
    except Exception as e:
        print(f"❌ Failed to download {model_id}: {str(e)}")

def main():
    """Main download function"""
    print("🚀 Translation Model Downloader")
    print(f"📁 Saving to: {MODELS_DIR}")
    
    total_models = sum(len(models) for models in MODEL_CONFIGS.values())
    current_model = 0
    
    # Download all models
    for model_type, models in MODEL_CONFIGS.items():
        for model_key, config in models.items():
            current_model += 1
            print(f"\n[{current_model}/{total_models}] {model_type}/{model_key}")
            download_model(config["model_id"], config["cache_dir"])
    
    print(f"\n✅ Download Complete! All models saved to: {MODELS_DIR}")

if __name__ == "__main__":
    main()
