# tests/test_chinese_translator_safe.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.chinese_translator import ChineseTranslator
import time

def test_chinese_translator():
    """Test Chinese translation functionality safely."""
    print("🧪 Testing Chinese Translator - Safe Implementation")
    print("="*60)
    
    # Initialize Chinese translator
    translator = ChineseTranslator()
    
    # Basic system info
    info = translator.get_model_info()
    print("📊 System Information:")
    print(f"Device: {info['device']}")
    print(f"Supported languages: {info['supported_languages']}")
    print(f"Valid pairs: {info['valid_pairs']}")
    
    # Simple test cases
    test_cases = [
        {
            "text": "Hello, world!",
            "src_lang": "en",
            "tgt_lang": "zh",
            "description": "English → Chinese (Simple)"
        },
        {
            "text": "How are you today?",
            "src_lang": "en",
            "tgt_lang": "zh",
            "description": "English → Chinese (Question)"
        },
        {
            "text": "你好！",
            "src_lang": "zh",
            "tgt_lang": "en",
            "description": "Chinese → English (Simple)"
        },
        {
            "text": "你今天好吗？",
            "src_lang": "zh",
            "tgt_lang": "en",
            "description": "Chinese → English (Question)"
        }
    ]
    
    success_count = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            print(f"\n{i}. {test_case['description']}")
            print(f"   Input:  {test_case['text']}")
            
            start_time = time.time()
            translation = translator.translate(
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
    print(f"\n" + "="*60)
    print(f"🎯 Chinese Translator Test Summary: {success_count}/{total_tests} tests passed")
    print(f"Success Rate: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print(f"🎉 All Chinese translation tests passed!")
        print(f"✅ Ready for integration with existing system!")
    else:
        print(f"⚠️  Some tests failed. Check implementation.")
    
    return success_count == total_tests

def test_chinese_integration_compatibility():
    """Test compatibility with existing system patterns."""
    print("\n🔧 Testing Integration Compatibility")
    print("="*60)
    
    # Test import compatibility
    try:
        from src.services.unified_translator import UnifiedTranslator
        print("✅ Existing UnifiedTranslator import: SUCCESS")
        existing_working = True
    except Exception as e:
        print(f"❌ Existing UnifiedTranslator import: FAILED - {e}")
        existing_working = False
    
    # Test Chinese translator import
    try:
        from src.services.chinese_translator import ChineseTranslator
        print("✅ New ChineseTranslator import: SUCCESS")
        chinese_working = True
    except Exception as e:
        print(f"❌ New ChineseTranslator import: FAILED - {e}")
        chinese_working = False
    
    # Test device compatibility
    if chinese_working:
        chinese_translator = ChineseTranslator()
        chinese_device = chinese_translator.device
        print(f"✅ Chinese translator device: {chinese_device}")
    
    if existing_working:
        existing_translator = UnifiedTranslator()
        existing_device = existing_translator.device
        print(f"✅ Existing translator device: {existing_device}")
        
        if chinese_working and chinese_device == existing_device:
            print("✅ Device compatibility: PERFECT MATCH")
        else:
            print("⚠️  Device compatibility: Different devices detected")
    
    return existing_working and chinese_working

if __name__ == "__main__":
    print("🚀 Starting Safe Chinese Translation Tests")
    print("="*80)
    
    # Test compatibility first
    compatibility_success = test_chinese_integration_compatibility()
    
    # Test Chinese functionality
    chinese_success = test_chinese_translator()
    
    # Overall summary
    print(f"\n" + "="*80)
    print(f"🏆 SAFE INTEGRATION TEST RESULTS:")
    print(f"   System Compatibility:   {'✅ PASSED' if compatibility_success else '❌ FAILED'}")
    print(f"   Chinese Translation:    {'✅ PASSED' if chinese_success else '❌ FAILED'}")
    
    if compatibility_success and chinese_success:
        print(f"\n🎉 SAFE CHINESE INTEGRATION READY!")
        print(f"🚀 Your existing system is intact and Chinese support is working!")
        print(f"📋 Next step: Integrate Chinese support into your interfaces")
    else:
        print(f"\n⚠️  Issues detected. Review before proceeding.")