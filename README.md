# 🌍 MultiLanguage Translation System - Quick Setup

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Multi-language translation supporting English↔Hindi↔Urdu↔Chinese with CLI, Web UI, and API integration.**

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/your-username/MultiLanguageTranslation.git
cd MultiLanguageTranslation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements-core.txt  # Backend only (20 packages)
# OR
pip install -r requirements.txt       # Full with UI (86 packages)

# Download models (5-10 minutes)
python scripts/download_models.py
```

### 2. Verify Installation
```bash
# Test CLI
python src/cli_translator.py "Hello world" --src eng_Latn --tgt hin_Deva

# Test system
python tests/test_enhanced_unified_translator.py
```

## 💻 CLI Usage

### Basic Translation
```bash
# Direct translation
python src/cli_translator.py "Hello" --src eng_Latn --tgt hin_Deva
python src/cli_translator.py "你好" --src zh --tgt eng_Latn

# File translation
python src/cli_translator.py --file document.txt --src eng_Latn --tgt zh --output translated.txt

# Interactive mode
python src/cli_translator.py --interactive
```

### Language Codes
| Language | Code | Example |
|----------|------|---------|
| English | `eng_Latn` | Hello |
| Hindi | `hin_Deva` | नमस्ते |
| Urdu | `urd_Arab` | سلام |
| Chinese | `zh` | 你好 |

## 🌐 Web Interface

```bash
# Start Streamlit app
streamlit run run_enhanced_streamlit.py

# Access at: http://localhost:8501
```

## 🧪 Testing

### CLI Testing
```bash
# Comprehensive system test
python tests/test_enhanced_unified_translator.py

# CLI functionality test
python src/cli_translator.py "Test message" --src eng_Latn --tgt hin_Deva
```

### Expected Output
```
✅ Enhanced Unified Translator: PASSED
✅ Multi-Step Translation: PASSED  
✅ Language Support Validation: PASSED
🎉 ALL TESTS PASSED!
```

## 🔌 Backend API Integration

### Text Translation
```python
from src.services.translation_wrapper import translate_wrapper

# In FastAPI endpoint:
@app.post("/translate")
async def translate_text(text: str, src_lang: str, tgt_lang: str):
    result = translate_wrapper(text, src_lang, tgt_lang)
    return {"translated_text": result}
```

### File Translation
```python
from src.services.translation_wrapper import WrappedTranslator
from src.services.file_translator import FileTranslator

# In FastAPI endpoint:
@app.post("/translate/file")
async def translate_file(file: UploadFile, src_lang: str, tgt_lang: str):
    file_translator = FileTranslator(translator=WrappedTranslator())
    stats = file_translator.translate_file(input_path, output_path, src_lang, tgt_lang)
    return {"status": "success", "stats": stats}
```

### FastAPI Setup Example
```python
from fastapi import FastAPI
from src.services.translation_wrapper import translate_wrapper

app = FastAPI()

@app.post("/translate")
async def translate(text: str, src_lang: str, tgt_lang: str):
    return {"result": translate_wrapper(text, src_lang, tgt_lang)}
```

## 📊 Supported Translations

### Direct Translations
- English ↔ Hindi (IndicTrans2)
- English ↔ Urdu (IndicTrans2)  
- English ↔ Chinese (OPUS-MT)

### Multi-Step Translations (via English)
- Hindi ↔ Chinese
- Urdu ↔ Chinese
- Hindi ↔ Urdu

## 🛠️ Troubleshooting

### Common Issues
```bash
# Module not found
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"

# Models not downloading
python scripts/download_models.py

# Import errors
pip install -r requirements-core.txt --upgrade
```

### System Info
```bash
python src/cli_translator.py --info
```

## 📁 Project Structure
```
MultiLanguageTranslation/
├── src/services/           # Translation services
├── scripts/               # Setup scripts  
├── models/                # Downloaded models (~1GB)
├── tests/                 # Test suite
└── requirements-core.txt  # Backend dependencies
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.