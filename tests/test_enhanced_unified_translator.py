# tests/test_enhanced_unified_translator.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.enhanced_unified_translator import EnhancedUnifiedTranslator
import time

def test_enhanced_unified_translator():
    """Test the enhanced unified translator with Chinese support."""
    print("🧪 Testing Enhanced Unified Translator")
    print("="*80)
    
    # Initialize enhanced translator
    translator = EnhancedUnifiedTranslator()
    
    # Display system info
    info = translator.get_model_info()
    print("📊 System Information:")
    print(f"Device: {info['device']}")
    print(f"Translation systems: {info['translation_systems']}")
    print(f"Supported languages: {len(info['supported_languages'])}")
    print(f"Valid pairs: {len(info['valid_pairs'])}")
    
    print("\n" + "="*80)
    
    # FIXED: Comprehensive test cases using correct language codes
    test_cases = [
        # IndicTrans2 tests (existing functionality)
        {
            "text": "Hello, how are you today?",
            "src_lang": "eng_Latn",
            "tgt_lang": "hin_Deva",
            "description": "English → Hindi (IndicTrans2)",
            "category": "IndicTrans2"
        },
        {
            "text": "नमस्ते, आप कैसे हैं?",
            "src_lang": "hin_Deva",
            "tgt_lang": "eng_Latn",
            "description": "Hindi → English (IndicTrans2)",
            "category": "IndicTrans2"
        },
        {
            "text": "Welcome to our beautiful country.",
            "src_lang": "eng_Latn",
            "tgt_lang": "urd_Arab",
            "description": "English → Urdu (IndicTrans2)",
            "category": "IndicTrans2"
        },
        {
            "text": "آپ کا استقبال ہے۔",
            "src_lang": "urd_Arab",
            "tgt_lang": "eng_Latn",
            "description": "Urdu → English (IndicTrans2)",
            "category": "IndicTrans2"
        },
        
        # OPUS-MT tests (FIXED: using correct language codes)
        {
            "text": "Hello, how are you today?",
            "src_lang": "eng_Latn",  # FIXED: was "en"
            "tgt_lang": "zh",
            "description": "English → Chinese (OPUS-MT)",
            "category": "OPUS-MT"
        },
        {
            "text": "你好，你今天好吗？",
            "src_lang": "zh",
            "tgt_lang": "eng_Latn",  # FIXED: was "en"
            "description": "Chinese → English (OPUS-MT)",
            "category": "OPUS-MT"
        },
        {
            "text": "Welcome to our beautiful country.",
            "src_lang": "eng_Latn",  # FIXED: was "en"
            "tgt_lang": "zh",
            "description": "English → Chinese (Complex)",
            "category": "OPUS-MT"
        },
        {
            "text": "欢迎来到我们美丽的国家。",
            "src_lang": "zh",
            "tgt_lang": "eng_Latn",  # FIXED: was "en"
            "description": "Chinese → English (Complex)",
            "category": "OPUS-MT"
        },
        
        # Cross-system tests (these were already working)
        {
            "text": "Hello, how are you?",
            "src_lang": "eng_Latn",
            "tgt_lang": "zh",
            "description": "English (IndicTrans) → Chinese (Cross-system)",
            "category": "Cross-system"
        },
        {
            "text": "你好，你好吗？",
            "src_lang": "zh",
            "tgt_lang": "eng_Latn",
            "description": "Chinese → English (IndicTrans) (Cross-system)",
            "category": "Cross-system"
        }
    ]
    
    # Track results by category
    results = {
        "IndicTrans2": {"success": 0, "total": 0},
        "OPUS-MT": {"success": 0, "total": 0},
        "Cross-system": {"success": 0, "total": 0}
    }
    
    overall_success = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        category = test_case['category']
        results[category]["total"] += 1
        
        try:
            print(f"\n{i}. {test_case['description']}")
            print(f"   Category: {category}")
            print(f"   Input:    {test_case['text']}")
            print(f"   Route:    {test_case['src_lang']} → {test_case['tgt_lang']}")
            
            start_time = time.time()
            translation = translator.translate(
                test_case['text'],
                test_case['src_lang'],
                test_case['tgt_lang']
            )
            end_time = time.time()
            
            print(f"   Output:   {translation}")
            print(f"   Time:     {end_time - start_time:.2f}s")
            print(f"   ✅ Success")
            
            results[category]["success"] += 1
            overall_success += 1
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")
            # Don't print full traceback for cleaner output
            if "Unsupported language pair" not in str(e):
                import traceback
                traceback.print_exc()
    
    # Detailed summary by category
    print(f"\n" + "="*80)
    print(f"🎯 ENHANCED TRANSLATOR TEST RESULTS:")
    print(f"="*80)
    
    for category, data in results.items():
        success_rate = (data["success"] / data["total"]) * 100 if data["total"] > 0 else 0
        status = "✅ PASSED" if data["success"] == data["total"] else "❌ FAILED"
        print(f"{category:15}: {data['success']}/{data['total']} tests ({success_rate:.1f}%) {status}")
    
    # Overall summary
    overall_rate = (overall_success / total_tests) * 100
    print(f"\n{'OVERALL':15}: {overall_success}/{total_tests} tests ({overall_rate:.1f}%)")
    
    if overall_success == total_tests:
        print(f"\n🎉 ALL ENHANCED TRANSLATION TESTS PASSED!")
        print(f"🚀 Enhanced system with Chinese support is fully functional!")
    else:
        print(f"\n⚠️  Some tests failed. Review implementation.")
    
    return overall_success == total_tests

def test_multi_step_translation():
    """Test multi-step translation capabilities."""
    print("\n🧪 Testing Multi-Step Translation")
    print("="*80)
    
    translator = EnhancedUnifiedTranslator()
    
    # Multi-step test cases
    test_cases = [
        {
            "text": "नमस्ते, आप कैसे हैं?",
            "src_lang": "hin_Deva",
            "tgt_lang": "zh", 
            "description": "Hindi → Chinese (via English)"
        },
        {
            "text": "你好，你好吗？",
            "src_lang": "zh",
            "tgt_lang": "hin_Deva",
            "description": "Chinese → Hindi (via English)"
        },
        {
            "text": "آپ کیسے ہیں؟",
            "src_lang": "urd_Arab",
            "tgt_lang": "zh",
            "description": "Urdu → Chinese (via English)"
        },
        {
            "text": "你今天怎么样？",
            "src_lang": "zh",
            "tgt_lang": "urd_Arab",
            "description": "Chinese → Urdu (via English)"
        }
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            print(f"\n{i}. {test_case['description']}")
            print(f"   Input:  {test_case['text']}")
            
            start_time = time.time()
            translation = translator.translate_multi_step(
                test_case['text'],
                test_case['src_lang'],
                test_case['tgt_lang']
            )
            end_time = time.time()
            
            print(f"   Output: {translation}")
            print(f"   Time:   {end_time - start_time:.2f}s")
            print(f"   ✅ Success")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Summary
    print(f"\n" + "="*80)
    print(f"🎯 Multi-Step Translation Summary: {success_count}/{total_tests} tests passed")
    print(f"Success Rate: {(success_count/total_tests)*100:.1f}%")
    
    return success_count == total_tests

def test_language_support_verification():
    """Verify language support and valid pairs."""
    print("\n🧪 Testing Language Support Verification")
    print("="*80)
    
    translator = EnhancedUnifiedTranslator()
    
    # Get system info
    info = translator.get_model_info()
    
    print("📋 Supported Languages:")
    for code, name in info['supported_languages'].items():
        print(f"   {code:10} → {name}")
    
    print(f"\n📋 Valid Translation Pairs ({len(info['valid_pairs'])} total):")
    for i, (src, tgt) in enumerate(info['valid_pairs'], 1):
        src_name = info['supported_languages'].get(src, src)
        tgt_name = info['supported_languages'].get(tgt, tgt)
        print(f"   {i:2}. {src:10} → {tgt:10} ({src_name} → {tgt_name})")
    
    # Test pair validation
    print(f"\n🔍 Testing Pair Validation:")
    
    test_pairs = [
        ("eng_Latn", "hin_Deva", True),
        ("eng_Latn", "zh", True),
        ("zh", "eng_Latn", True),
        ("hin_Deva", "zh", False),  # Should be false (needs multi-step)
        ("en", "zh", False),  # Should be false (wrong format)
    ]
    
    validation_success = 0
    for src, tgt, expected in test_pairs:
        result = translator.is_supported_pair(src, tgt)
        status = "✅" if result == expected else "❌"
        print(f"   {status} {src} → {tgt}: Expected {expected}, Got {result}")
        if result == expected:
            validation_success += 1
    
    print(f"\n📊 Validation Results: {validation_success}/{len(test_pairs)} correct")
    
    return validation_success == len(test_pairs)

if __name__ == "__main__":
    print("🚀 Starting Enhanced Unified Translator Test Suite")
    print("="*100)
    
    # Run all tests
    enhanced_success = test_enhanced_unified_translator()
    multi_step_success = test_multi_step_translation()
    validation_success = test_language_support_verification()
    
    # Overall summary
    print(f"\n" + "="*100)
    print(f"🏆 FINAL TEST RESULTS:")
    print(f"   Enhanced Unified Translator: {'✅ PASSED' if enhanced_success else '❌ FAILED'}")
    print(f"   Multi-Step Translation:      {'✅ PASSED' if multi_step_success else '❌ FAILED'}")
    print(f"   Language Support Validation: {'✅ PASSED' if validation_success else '❌ FAILED'}")
    
    all_passed = enhanced_success and multi_step_success and validation_success
    
    if all_passed:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"🌍 Enhanced translation system with Chinese support is ready for production!")
        print(f"\n📋 Next Steps:")
        print(f"   1. Run enhanced Streamlit app: python3 run_enhanced_streamlit.py")
        print(f"   2. Test file translation with Chinese content")
        print(f"   3. System is ready for deployment!")
    else:
        print(f"\n⚠️  Some tests failed. Please review the implementation.")
        
    print(f"\n🎯 System Status: {'🟢 READY' if all_passed else '🟡 NEEDS REVIEW'}")