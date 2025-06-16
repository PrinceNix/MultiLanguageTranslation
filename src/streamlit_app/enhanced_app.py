import streamlit as st
import sys
import os
import io
import json
import csv
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.services.enhanced_unified_translator import EnhancedUnifiedTranslator
from src.services.file_translator import FileTranslator

# Page configuration
st.set_page_config(
    page_title="🌍 Enhanced Universal Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chinese-highlight {
        background: linear-gradient(90deg, #ff6b6b 0%, #ffa500 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'enhanced_translator' not in st.session_state:
    st.session_state.enhanced_translator = None
if 'file_translator' not in st.session_state:
    st.session_state.file_translator = None
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "home"

@st.cache_resource
def load_enhanced_translator():
    """Load and cache the enhanced translator."""
    return EnhancedUnifiedTranslator()

@st.cache_resource
def load_file_translator():
    """Load and cache the file translator."""
    return FileTranslator()

def get_language_options_enhanced(translator, src_lang=None, include_multistep=False):
    """Get available language options for enhanced translator (FIXED - dynamic based on multi-step)."""
    lang_display = {
        "eng_Latn": "🇺🇸 English",
        "hin_Deva": "🇮🇳 Hindi",
        "urd_Arab": "🇵🇰 Urdu",
        "zh": "🇨🇳 Chinese (Simplified)"
    }
    
    if src_lang:
        # Get available targets for this source (dynamic based on multi-step option)
        available_targets = translator.get_available_targets(src_lang, include_multistep=include_multistep)
        return [(lang, lang_display.get(lang, lang)) for lang in available_targets]
    else:
        # Return all languages for source selection
        supported_langs = translator.get_supported_languages()
        return [(lang, lang_display.get(lang, lang)) for lang in supported_langs.keys()]

def main():
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🌍 Enhanced Universal Translation System</h1>
        <p>English↔Hindi • English↔Urdu • English↔Chinese</p>
        <div class="chinese-highlight">
            🆕 NEW: Chinese (Simplified) Support Added!
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for mode selection
    st.sidebar.title("🚀 Navigation")
    
    # Mode selection with working buttons
    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.current_mode = "home"
    if st.sidebar.button("💬 Text Translation", use_container_width=True):
        st.session_state.current_mode = "text"
    if st.sidebar.button("📁 File Translation", use_container_width=True):
        st.session_state.current_mode = "file"
    if st.sidebar.button("ℹ️ System Info", use_container_width=True):
        st.session_state.current_mode = "info"
    
    # Language reference in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ✅ Supported Translations")
    st.sidebar.markdown("""
    **Direct Translations:**
    - **🇺🇸 English ↔ 🇮🇳 Hindi**
    - **🇺🇸 English ↔ 🇵🇰 Urdu**
    - **🇺🇸 English ↔ 🇨🇳 Chinese**
    
    **Multi-Step Available:**
    - **🇮🇳 Hindi ↔ 🇨🇳 Chinese** (via English)
    - **🇵🇰 Urdu ↔ 🇨🇳 Chinese** (via English)
    - **🇮🇳 Hindi ↔ 🇵🇰 Urdu** (via English)
    """)
    
    # Route to different modes
    if st.session_state.current_mode == "home":
        show_enhanced_home()
    elif st.session_state.current_mode == "text":
        show_enhanced_text_translation()
    elif st.session_state.current_mode == "file":
        show_enhanced_file_translation()
    elif st.session_state.current_mode == "info":
        show_enhanced_system_info()

def show_enhanced_home():
    """Show enhanced home page with Chinese support."""
    
    # Quick Start Section
    st.markdown("## 🚀 Quick Start")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💬 Text Translation", use_container_width=True, type="primary"):
            st.session_state.current_mode = "text"
            st.rerun()
    
    with col2:
        if st.button("📁 File Translation", use_container_width=True, type="primary"):
            st.session_state.current_mode = "file"
            st.rerun()
    
    with col3:
        if st.button("ℹ️ System Information", use_container_width=True, type="secondary"):
            st.session_state.current_mode = "info"
            st.rerun()
    
    st.markdown("---")
    
    # Initialize enhanced translator for quick translation
    if st.session_state.enhanced_translator is None:
        with st.spinner("🔄 Loading enhanced translation models..."):
            st.session_state.enhanced_translator = load_enhanced_translator()
    
    # Quick translation with smart language selection
    st.markdown("## 🎯 Quick Enhanced Translation")
    
    # Multi-step option (place it before language selection so it affects the options)
    use_multistep = st.checkbox("🔄 Use multi-step translation (enables all language pairs)", value=False, key="home_multistep")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Source language selection
        src_options = get_language_options_enhanced(st.session_state.enhanced_translator)
        src_lang = st.selectbox(
            "🔤 From",
            options=[opt[0] for opt in src_options],
            format_func=lambda x: dict(src_options)[x],
            key="enhanced_home_src"
        )
    
    with col2:
        # Target language selection (FIXED - dynamic based on multi-step option)
        tgt_options = get_language_options_enhanced(
            st.session_state.enhanced_translator, 
            src_lang, 
            include_multistep=use_multistep
        )
        if tgt_options:
            tgt_lang = st.selectbox(
                "🎯 To",
                options=[opt[0] for opt in tgt_options],
                format_func=lambda x: dict(tgt_options)[x],
                key="enhanced_home_tgt"
            )
        else:
            st.error("❌ No valid target languages for selected source")
            return
    
    # Show translation type
    if use_multistep and not st.session_state.enhanced_translator.is_supported_pair(src_lang, tgt_lang):
        st.info(f"🔄 Multi-step translation: {src_lang} → English → {tgt_lang}")
    elif st.session_state.enhanced_translator.is_supported_pair(src_lang, tgt_lang):
        st.info(f"⚡ Direct translation: {src_lang} → {tgt_lang}")
    
    # Text input for quick translation
    input_text = st.text_area(
        "📝 Enter text to translate:",
        height=100,
        placeholder="Type your text here...",
        key="enhanced_home_text"
    )
    
    # Quick translate button
    if st.button("🔄 Translate Now", type="primary", use_container_width=True):
        if input_text.strip():
            if src_lang == tgt_lang:
                st.warning("⚠️ Source and target languages are the same!")
            else:
                try:
                    with st.spinner("🔄 Translating..."):
                        if use_multistep:
                            result = st.session_state.enhanced_translator.translate_multi_step(input_text, src_lang, tgt_lang)
                        else:
                            result = st.session_state.enhanced_translator.translate(input_text, src_lang, tgt_lang)
                    
                    # Display result in columns
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**📝 Original:**")
                        st.info(input_text)
                    with col2:
                        st.markdown("**🌟 Translated:**")
                        st.success(result)
                
                except Exception as e:
                    st.error(f"❌ Translation failed: {str(e)}")
                    if "Unsupported language pair" in str(e) and not use_multistep:
                        st.info("💡 Try enabling 'Use multi-step translation' for this language pair")
        else:
            st.warning("⚠️ Please enter some text to translate!")
    
    st.markdown("---")
    
    # Features Overview
    st.markdown("## ✨ Enhanced Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ✅ Direct Translations
        - **🇺🇸 English → 🇮🇳 Hindi** (IndicTrans2)
        - **🇮🇳 Hindi → 🇺🇸 English** (IndicTrans2)
        - **🇺🇸 English → 🇵🇰 Urdu** (IndicTrans2)
        - **🇵🇰 Urdu → 🇺🇸 English** (IndicTrans2)
        - **🇺🇸 English → 🇨🇳 Chinese** (OPUS-MT) 🆕
        - **🇨🇳 Chinese → 🇺🇸 English** (OPUS-MT) 🆕
        """)
    
    with col2:
        st.markdown("""
        ### 🔄 Multi-Step Translations
        - **🇮🇳 Hindi → 🇨🇳 Chinese** (via English) 🆕
        - **🇨🇳 Chinese → 🇮🇳 Hindi** (via English) 🆕
        - **🇵🇰 Urdu → 🇨🇳 Chinese** (via English) 🆕
        - **🇨🇳 Chinese → 🇵🇰 Urdu** (via English) 🆕
        - **🇮🇳 Hindi ↔ 🇵🇰 Urdu** (via English)
        """)

def show_enhanced_text_translation():
    """Enhanced text translation page with all language support."""
    st.header("💬 Enhanced Text Translation")
    
    if st.session_state.enhanced_translator is None:
        with st.spinner("🔄 Loading enhanced translation models..."):
            st.session_state.enhanced_translator = load_enhanced_translator()
        st.success("✅ Enhanced translation system ready!")
    
    # Multi-step option (place it first so it affects language selection)
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col3:
        # Multi-step option
        use_multistep = st.checkbox("🔄 Multi-step", help="Enable all language pairs via multi-step translation", key="text_multistep")
    
    with col1:
        src_options = get_language_options_enhanced(st.session_state.enhanced_translator)
        src_lang = st.selectbox(
            "🔤 Source Language",
            options=[opt[0] for opt in src_options],
            format_func=lambda x: dict(src_options)[x],
            key="enhanced_text_src"
        )
    
    with col2:
        # FIXED: Dynamic target selection based on multi-step option
        tgt_options = get_language_options_enhanced(
            st.session_state.enhanced_translator, 
            src_lang, 
            include_multistep=use_multistep
        )
        if tgt_options:
            tgt_lang = st.selectbox(
                "🎯 Target Language",
                options=[opt[0] for opt in tgt_options],
                format_func=lambda x: dict(tgt_options)[x],
                key="enhanced_text_tgt"
            )
        else:
            st.error("❌ No valid target languages for selected source")
            return
    
    # Show translation path
    if use_multistep and not st.session_state.enhanced_translator.is_supported_pair(src_lang, tgt_lang):
        st.info(f"🔄 Multi-step translation: {src_lang} → English → {tgt_lang}")
    elif st.session_state.enhanced_translator.is_supported_pair(src_lang, tgt_lang):
        st.info(f"⚡ Direct translation: {src_lang} → {tgt_lang}")
    
    # Text input
    input_text = st.text_area(
        "📝 Enter text to translate:",
        height=200,
        placeholder="Type or paste your text here...",
        key="enhanced_text_input"
    )
    
    # Translation button
    if st.button("🔄 Translate", type="primary", use_container_width=True):
        if input_text.strip():
            try:
                with st.spinner("🔄 Translating..."):
                    start_time = time.time()
                    
                    if use_multistep:
                        result = st.session_state.enhanced_translator.translate_multi_step(input_text, src_lang, tgt_lang)
                        translation_type = "Multi-step"
                    else:
                        result = st.session_state.enhanced_translator.translate(input_text, src_lang, tgt_lang)
                        translation_type = "Direct"
                    
                    end_time = time.time()
                
                # Display result
                st.markdown("### 🌟 Translation Result")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**📝 Original:**")
                    st.info(input_text)
                
                with col2:
                    st.markdown("**🌟 Translated:**")
                    st.success(result)
                
                st.markdown(f"⏱️ **Translation time:** {end_time - start_time:.2f} seconds")
                st.markdown(f"🔄 **Translation type:** {translation_type}")
                
                # Copy to clipboard
                st.code(result, language=None)
                
            except Exception as e:
                st.error(f"❌ Translation failed: {str(e)}")
                if "Unsupported language pair" in str(e) and not use_multistep:
                    st.info("💡 Try enabling 'Multi-step' for this language pair")
        else:
            st.warning("⚠️ Please enter some text to translate!")

def show_enhanced_file_translation():
    """Enhanced file translation page (FIXED)."""
    st.header("📁 Enhanced File Translation")
    st.info("💡 Supports all language pairs including Chinese for .txt, .json, .csv files.")
    
    # Initialize both translators
    if st.session_state.enhanced_translator is None:
        with st.spinner("🔄 Loading enhanced translator..."):
            st.session_state.enhanced_translator = load_enhanced_translator()
    
    if st.session_state.file_translator is None:
        with st.spinner("🔄 Loading file translation system..."):
            st.session_state.file_translator = load_file_translator()
        st.success("✅ File translation system ready!")
    
    # File upload
    uploaded_file = st.file_uploader(
        "📤 Choose a file to translate",
        type=['txt', 'json', 'csv'],
        help="Supported formats: .txt, .json, .csv",
        key="enhanced_file"
    )
    
    if uploaded_file is not None:
        # File info
        st.markdown("### 📄 File Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📁 Filename", uploaded_file.name)
        with col2:
            st.metric("📏 Size", f"{uploaded_file.size} bytes")
        with col3:
            st.metric("📋 Type", uploaded_file.type)
        
        # Multi-step option for files
        use_multistep = st.checkbox("🔄 Use multi-step translation for files", help="Enable all language pairs", key="file_multistep")
        
        # Enhanced language selection (FIXED - dynamic based on multi-step)
        col1, col2 = st.columns(2)
        
        with col1:
            src_options = get_language_options_enhanced(st.session_state.enhanced_translator)
            src_lang = st.selectbox(
                "🔤 Source Language",
                options=[opt[0] for opt in src_options],
                format_func=lambda x: dict(src_options)[x],
                key="enhanced_file_src"
            )
        
        with col2:
            tgt_options = get_language_options_enhanced(
                st.session_state.enhanced_translator, 
                src_lang, 
                include_multistep=use_multistep
            )
            if tgt_options:
                tgt_lang = st.selectbox(
                    "🎯 Target Language",
                    options=[opt[0] for opt in tgt_options],
                    format_func=lambda x: dict(tgt_options)[x],
                    key="enhanced_file_tgt"
                )
            else:
                st.error("❌ No valid target languages for selected source")
                return
        
        # Show translation path for files
        if use_multistep and not st.session_state.enhanced_translator.is_supported_pair(src_lang, tgt_lang):
            st.info(f"🔄 File will be translated via multi-step: {src_lang} → English → {tgt_lang}")
        elif st.session_state.enhanced_translator.is_supported_pair(src_lang, tgt_lang):
            st.info(f"⚡ File will be translated directly: {src_lang} → {tgt_lang}")
        
        # Translate file button
        if st.button("🔄 Translate File", type="primary", use_container_width=True):
            try:
                with st.spinner("🔄 Translating file..."):
                    # Create a custom file translator that uses enhanced translator
                    temp_input_path = f"temp_input_{uploaded_file.name}"
                    with open(temp_input_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    
                    temp_output_path = f"temp_output_{uploaded_file.name}"
                    
                    # Use the existing file translator but with enhanced translation logic
                    # We need to monkey-patch the translator temporarily
                    original_translator = st.session_state.file_translator.translator
                    
                    # Create a wrapper that handles both direct and multi-step
                    class EnhancedFileTranslatorWrapper:
                        def __init__(self, enhanced_translator, use_multistep):
                            self.enhanced_translator = enhanced_translator
                            self.use_multistep = use_multistep
                        
                        def translate(self, text, src_lang, tgt_lang):
                            if self.use_multistep:
                                return self.enhanced_translator.translate_multi_step(text, src_lang, tgt_lang)
                            else:
                                return self.enhanced_translator.translate(text, src_lang, tgt_lang)
                    
                    # Temporarily replace the translator
                    st.session_state.file_translator.translator = EnhancedFileTranslatorWrapper(
                        st.session_state.enhanced_translator, use_multistep
                    )
                    
                    # Translate the file
                    stats = st.session_state.file_translator.translate_file(
                        temp_input_path, temp_output_path, src_lang, tgt_lang
                    )
                    
                    # Restore original translator
                    st.session_state.file_translator.translator = original_translator
                    
                    # Display results
                    st.markdown("### ✅ Translation Completed!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("⏱️ Time", f"{stats['processing_time']}s")
                    with col2:
                        if 'lines_processed' in stats:
                            st.metric("📄 Lines", stats['lines_processed'])
                        elif 'fields_translated' in stats:
                            st.metric("🏷️ Fields", stats['fields_translated'])
                        elif 'cells_translated' in stats:
                            st.metric("📊 Cells", stats['cells_translated'])
                    with col3:
                        translation_method = "Multi-step" if use_multistep else "Direct"
                        st.metric("🔄 Method", translation_method)
                    
                    # Download button
                    with open(temp_output_path, "rb") as f:
                        output_content = f.read()
                    
                    output_filename = f"translated_{uploaded_file.name}"
                    st.download_button(
                        label="📥 Download Translated File",
                        data=output_content,
                        file_name=output_filename,
                        mime=uploaded_file.type,
                        use_container_width=True
                    )
                    
                    # Cleanup
                    if os.path.exists(temp_input_path):
                        os.remove(temp_input_path)
                    if os.path.exists(temp_output_path):
                        os.remove(temp_output_path)
            
            except Exception as e:
                st.error(f"❌ File translation failed: {str(e)}")
                if "Unsupported language pair" in str(e) and not use_multistep:
                    st.info("💡 Try enabling 'Use multi-step translation for files'")

def show_enhanced_system_info():
    """Show enhanced system information."""
    st.header("ℹ️ Enhanced System Information")
    
    if st.session_state.enhanced_translator is None:
        with st.spinner("🔄 Loading enhanced translation models..."):
            st.session_state.enhanced_translator = load_enhanced_translator()
    
    info = st.session_state.enhanced_translator.get_model_info()
    
    # System metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🖥️ Device", info['device'])
    
    with col2:
        st.metric("🔄 Translation Systems", len(info['translation_systems']))
    
    with col3:
        st.metric("🌐 Supported Languages", len(info['supported_languages']))
    
    # Translation systems
    st.markdown("### 🔄 Translation Systems")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**IndicTrans2 (Hindi/Urdu):**")
        for model_key, model_name in info['indictrans_models'].items():
            status = "✅ Loaded" if model_key in info['indictrans_loaded_models'] else "⏳ Not Loaded"
            st.write(f"- **{model_key}**: {status}")
    
    with col2:
        st.markdown("**OPUS-MT (Chinese):**")
        for model_key, model_name in info['chinese_models'].items():
            status = "✅ Loaded" if model_key in info['chinese_loaded_models'] else "⏳ Not Loaded"
            st.write(f"- **{model_key}**: {status}")
    
    # Valid pairs
    st.markdown("### ✅ Supported Translation Pairs")
    st.markdown("**Direct Translations:**")
    for src, tgt in info['valid_pairs']:
        src_name = info['supported_languages'].get(src, src)
        tgt_name = info['supported_languages'].get(tgt, tgt)
        st.write(f"- **{src_name}** → **{tgt_name}**")
    
    # Multi-step pairs
    st.markdown("**Multi-Step Translations (via English):**")
    multistep_pairs = [
        ("hin_Deva", "zh", "Hindi → Chinese"),
        ("zh", "hin_Deva", "Chinese → Hindi"),
        ("urd_Arab", "zh", "Urdu → Chinese"),
        ("zh", "urd_Arab", "Chinese → Urdu"),
        ("hin_Deva", "urd_Arab", "Hindi → Urdu"),
        ("urd_Arab", "hin_Deva", "Urdu → Hindi"),
    ]
    
    for src, tgt, description in multistep_pairs:
        st.write(f"- **{description}** (via English)")
    
    # Languages
    st.markdown("### 🌐 Language Codes")
    for code, name in info['supported_languages'].items():
        st.write(f"- **{name}**: `{code}`")

if __name__ == "__main__":
    main()