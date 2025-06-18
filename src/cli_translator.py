#!/usr/bin/env python3
"""
Enhanced CLI interface for the unified translation system with file support.
Updated to use EnhancedUnifiedTranslator and support Chinese.
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.enhanced_unified_translator import EnhancedUnifiedTranslator
from src.services.file_translator import FileTranslator
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Enhanced Translation CLI with File Support")
    parser.add_argument("text", nargs="?", help="Text to translate")
    parser.add_argument("--src", choices=["eng_Latn", "hin_Deva", "urd_Arab", "zh"], 
                       help="Source language")
    parser.add_argument("--tgt", choices=["eng_Latn", "hin_Deva", "urd_Arab", "zh"],
                       help="Target language")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Start interactive mode")
    parser.add_argument("--info", action="store_true", help="Show system info")
    
    # File translation options
    parser.add_argument("--file", "-f", help="Path to file to translate")
    parser.add_argument("--output", "-o", help="Output file path (auto-generated if not provided)")
    parser.add_argument("--file-type", choices=["txt", "json", "csv"], 
                       help="Force file type (auto-detected if not provided)")
    parser.add_argument("--json-fields", nargs="+", 
                       help="Specific JSON fields to translate (all text fields if not provided)")
    parser.add_argument("--csv-columns", nargs="+",
                       help="Specific CSV columns to translate (all columns if not provided)")
    
    args = parser.parse_args()
    
    if args.file:
        # File translation mode
        file_translate_mode(args)
    else:
        # Text translation mode
        text_translate_mode(args)

def file_translate_mode(args):
    """Handle file translation."""
    if not args.src or not args.tgt:
        print("❌ For file translation, please provide both --src and --tgt")
        return
    
    print("🚀 Initializing File Translation System...")
    file_translator = FileTranslator()
    
    try:
        # Prepare kwargs for specific file types
        kwargs = {}
        if args.json_fields:
            kwargs['fields_to_translate'] = args.json_fields
        if args.csv_columns:
            kwargs['columns_to_translate'] = args.csv_columns
        
        print(f"🔄 Translating file: {args.file}")
        print(f"📝 From {args.src} to {args.tgt}")
        
        # Translate file
        stats = file_translator.translate_file(
            input_path=args.file,
            output_path=args.output,
            src_lang=args.src,
            tgt_lang=args.tgt,
            **kwargs
        )
        
        # Display results
        print(f"\n✅ File Translation Completed!")
        print(f"📁 Input:  {stats['input_file']}")
        print(f"📁 Output: {stats['output_file']}")
        print(f"⏱️  Time:   {stats['processing_time']}s")
        
        # File-specific stats
        if 'lines_processed' in stats:
            print(f"📄 Lines:  {stats['lines_processed']}")
        if 'fields_translated' in stats:
            print(f"🏷️  Fields: {stats['fields_translated']}")
        if 'cells_translated' in stats:
            print(f"📊 Cells:  {stats['cells_translated']}")
        
    except Exception as e:
        print(f"❌ File translation failed: {e}")

def text_translate_mode(args):
    """Handle text translation."""
    # Initialize translator
    print("🚀 Initializing Enhanced Translation System...")
    translator = EnhancedUnifiedTranslator()
    
    if args.info:
        info = translator.get_model_info()
        print("\n📊 System Information:")
        print(f"Device: {info['device']}")
        print(f"Translation systems: {info['translation_systems']}")
        print(f"Loaded models: {info['indictrans_loaded_models']} (IndicTrans), {info['chinese_loaded_models']} (Chinese)")
        print(f"Supported languages: {list(info['supported_languages'].keys())}")
        return
    
    if args.interactive:
        interactive_mode(translator)
    elif args.text and args.src and args.tgt:
        # Single translation
        try:
            # Check if direct translation is supported
            if translator.is_supported_pair(args.src, args.tgt):
                result = translator.translate(args.text, args.src, args.tgt)
                method = "direct"
            else:
                # Try multi-step translation
                result = translator.translate_multi_step(args.text, args.src, args.tgt)
                method = "multi-step"
                
            print(f"\n✅ Translation ({method}):")
            print(f"From ({args.src}): {args.text}")
            print(f"To   ({args.tgt}): {result}")
        except Exception as e:
            print(f"❌ Error: {e}")
    elif args.text:
        print("❌ For single translation, please provide both --src and --tgt")
    else:
        print("❌ Please provide text to translate, use --interactive mode, or --file for file translation")
        print("\nExamples:")
        print('  python3 src/cli_translator.py "Hello" --src eng_Latn --tgt hin_Deva')
        print('  python3 src/cli_translator.py "Hello" --src eng_Latn --tgt zh')
        print('  python3 src/cli_translator.py --interactive')
        print('  python3 src/cli_translator.py --file document.txt --src eng_Latn --tgt hin_Deva')

def interactive_mode(translator):
    """Interactive translation mode with file support."""
    print("\n🎯 Interactive Translation Mode")
    print("Commands: 'quit' to exit, 'help' for help, 'file' for file translation")
    
    # Language mappings for easier input
    lang_map = {
        "en": "eng_Latn", "english": "eng_Latn",
        "hi": "hin_Deva", "hindi": "hin_Deva", 
        "ur": "urd_Arab", "urdu": "urd_Arab",
        "zh": "zh", "chinese": "zh", "cn": "zh"
    }
    
    while True:
        try:
            print("\n" + "="*50)
            
            # Get mode
            mode = input("Mode (text/file/quit/help): ").strip().lower()
            
            if mode in ["quit", "exit"]:
                break
            elif mode == "help":
                print_help()
                continue
            elif mode == "file":
                interactive_file_mode()
                continue
            elif mode != "text":
                print("❌ Invalid mode. Use 'text', 'file', 'help', or 'quit'")
                continue
            
            # Text translation mode
            # Get source language
            src_input = input("Source language (en/hi/ur/zh): ").strip().lower()
            if src_input in ["quit", "exit"]:
                break
            
            src_lang = lang_map.get(src_input, src_input)
            supported_langs = translator.get_supported_languages()
            if src_lang not in supported_langs:
                print(f"❌ Unsupported source language: {src_input}")
                print(f"✅ Supported: {list(supported_langs.keys())}")
                continue
            
            # Get target language
            tgt_input = input("Target language (en/hi/ur/zh): ").strip().lower()
            if tgt_input in ["quit", "exit"]:
                break
                
            tgt_lang = lang_map.get(tgt_input, tgt_input)
            if tgt_lang not in supported_langs:
                print(f"❌ Unsupported target language: {tgt_input}")
                print(f"✅ Supported: {list(supported_langs.keys())}")
                continue
            
            # Get text to translate
            text = input("Enter text to translate: ").strip()
            if not text:
                continue
            if text.lower() in ["quit", "exit"]:
                break
            
            # Translate
            print("🔄 Translating...")
            
            # Check if direct or multi-step translation
            if translator.is_supported_pair(src_lang, tgt_lang):
                result = translator.translate(text, src_lang, tgt_lang)
                method = "direct"
            else:
                try:
                    result = translator.translate_multi_step(text, src_lang, tgt_lang)
                    method = "multi-step"
                except Exception as e:
                    print(f"❌ Translation not possible: {e}")
                    continue
            
            print(f"\n✅ Translation Result ({method}):")
            print(f"📝 Original ({supported_langs[src_lang]}): {text}")
            print(f"🌟 Translated ({supported_langs[tgt_lang]}): {result}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def interactive_file_mode():
    """Interactive file translation mode."""
    print("\n📁 File Translation Mode")
    
    file_translator = FileTranslator()
    lang_map = {
        "en": "eng_Latn", "english": "eng_Latn",
        "hi": "hin_Deva", "hindi": "hin_Deva", 
        "ur": "urd_Arab", "urdu": "urd_Arab",
        "zh": "zh", "chinese": "zh", "cn": "zh"
    }
    
    try:
        # Get file path
        file_path = input("Enter file path: ").strip()
        if not file_path or not os.path.exists(file_path):
            print("❌ File not found")
            return
        
        if not file_translator.is_supported_format(file_path):
            print(f"❌ Unsupported file format. Supported: {file_translator.SUPPORTED_FORMATS}")
            return
        
        # Get languages
        src_input = input("Source language (en/hi/ur/zh): ").strip().lower()
        src_lang = lang_map.get(src_input, src_input)
        
        tgt_input = input("Target language (en/hi/ur/zh): ").strip().lower()
        tgt_lang = lang_map.get(tgt_input, tgt_input)
        
        # Get output path (optional)
        output_path = input("Output file path (press Enter for auto-generated): ").strip()
        if not output_path:
            output_path = None
        
        print("🔄 Translating file...")
        stats = file_translator.translate_file(file_path, output_path, src_lang, tgt_lang)
        
        print(f"\n✅ File Translation Completed!")
        print(f"📁 Output: {stats['output_file']}")
        print(f"⏱️  Time: {stats['processing_time']}s")
        
    except Exception as e:
        print(f"❌ File translation error: {e}")

def print_help():
    """Print help information."""
    print("""
🆘 Help - Enhanced Translation System

Supported Languages:
  • en/english  -> English (eng_Latn)
  • hi/hindi    -> Hindi (hin_Deva)  
  • ur/urdu     -> Urdu (urd_Arab)
  • zh/chinese  -> Chinese Simplified (zh) 🆕

Supported File Formats:
  • .txt  -> Plain text files
  • .json -> JSON files (translates text fields)
  • .csv  -> CSV files (translates specified columns)

Text Translation Examples:
  Direct translation:
    Source: en
    Target: hi
    Text: Hello, how are you?
    Result: नमस्ते, आप कैसे हैं?
  
  Multi-step translation (via English):
    Source: hi
    Target: zh
    Text: नमस्ते
    Result: 你好

File Translation:
  Mode: file
  File: /path/to/document.txt
  Source: en
  Target: zh
  Output: Auto-generated or specify custom path

Commands:
  • quit/exit   -> Exit the program
  • help        -> Show this help
  • text        -> Text translation mode
  • file        -> File translation mode
""")

if __name__ == "__main__":
    main()
