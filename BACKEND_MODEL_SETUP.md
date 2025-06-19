# Backend Model Setup - v3.0.0

## Quick Backend Setup (3 Steps)

### 1. Install Core Dependencies
```bash
# Backend-only setup (20 packages, ~200MB)
pip install -r requirements-core.txt
```

### 2. Download Models
```bash
# Option A: Download all models (5-10 minutes)
python scripts/download_models.py

# Option B: Auto-download on first use
python src/cli_translator.py "Hello" --src eng_Latn --tgt hin_Deva
```

### 3. Verify Installation
```bash
# Test system
python tests/test_enhanced_unified_translator.py

# Test CLI
python src/cli_translator.py "Test" --src eng_Latn --tgt hin_Deva
```

## Backend Integration - NEW v3.0.0

### Simple Translation Wrapper
```python
from src.services.translation_wrapper import translate_wrapper

# Automatic routing (direct or multi-step)
result = translate_wrapper(text, src_lang, tgt_lang)
```

### File Translation
```python
from src.services.translation_wrapper import WrappedTranslator
from src.services.file_translator import FileTranslator

file_translator = FileTranslator(translator=WrappedTranslator())
stats = file_translator.translate_file(input_path, output_path, src_lang, tgt_lang)
```

### FastAPI Integration Example
```python
from fastapi import FastAPI, UploadFile
from src.services.translation_wrapper import translate_wrapper, WrappedTranslator
from src.services.file_translator import FileTranslator

app = FastAPI()

@app.post("/translate")
async def translate_text(text: str, src_lang: str, tgt_lang: str):
    result = translate_wrapper(text, src_lang, tgt_lang)
    return {"translated_text": result}

@app.post("/translate/file")
async def translate_file_endpoint(file: UploadFile, src_lang: str, tgt_lang: str):
    # Save uploaded file
    input_path = f"temp_{file.filename}"
    with open(input_path, "wb") as f:
        f.write(await file.read())
    
    # Translate
    file_translator = FileTranslator(translator=WrappedTranslator())
    output_path = f"translated_{file.filename}"
    stats = file_translator.translate_file(input_path, output_path, src_lang, tgt_lang)
    
    return {"status": "success", "output_file": output_path, "stats": stats}
```

## Language Codes for API
```python
SUPPORTED_LANGUAGES = {
    "eng_Latn": "English",
    "hin_Deva": "Hindi", 
    "urd_Arab": "Urdu",
    "zh": "Chinese"
}
```

## Model Storage
```
models/
├── indictrans2/           # Hindi/Urdu models (~400MB)
│   ├── en-indic/         # English → Hindi/Urdu  
│   └── indic-en/         # Hindi/Urdu → English
└── opus-mt/              # Chinese models (~600MB)
    ├── en-zh/            # English → Chinese
    └── zh-en/            # Chinese → English
```

## Deployment Notes
- **Total size**: ~1GB (models) + 200MB (dependencies)
- **Memory**: 2-4GB RAM recommended
- **First run**: 30-60 seconds model loading
- **Subsequent runs**: <5 seconds per translation

## What's New in v3.0.0
- ✅ Translation wrapper for automatic routing
- ✅ Simplified API integration
- ✅ File translation with custom translators
- ✅ Backend-ready FastAPI examples