# Model Setup for Backend Team

## Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements-core.txt
```

### 2. Download Models (Choose ONE option)

#### Option A: Download All Models at Once (Recommended)
```bash
python scripts/download_models.py
```
Wait 5-10 minutes. All models will be in `models/` directory.

#### Option B: Let Models Download Automatically
Just run any translation command:
```bash
python src/cli_translator.py "Hello" --src eng_Latn --tgt hin_Deva
```

### 3. Verify Models are Downloaded
```bash
ls -la models/indictrans2/
ls -la models/opus-mt/
```

You should see model files in these directories.

## What's in the Models Directory?

```
models/
├── indictrans2/           # Indian language models
│   ├── en-indic/         # English → Hindi/Urdu
│   └── indic-en/         # Hindi/Urdu → English
└── opus-mt/              # Chinese models
    ├── en-zh/            # English → Chinese
    └── zh-en/            # Chinese → English
```

## For Offline Deployment

1. Download models using the script
2. Copy entire `models/` directory to deployment server
3. No internet needed after that!

