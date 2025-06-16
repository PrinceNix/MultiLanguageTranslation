# src/services/file_translator.py
import os
import json
import csv
from typing import List, Dict, Tuple
from pathlib import Path
import time
from src.services.unified_translator import UnifiedTranslator
from src.utils.logger import setup_logger

logger = setup_logger("file_translator")

class FileTranslator:
    """
    File translation system supporting various file formats.
    Supports: .txt, .json, .csv files
    """
    
    SUPPORTED_FORMATS = ['.txt', '.json', '.csv']
    
    def __init__(self):
        self.translator = UnifiedTranslator()
        logger.info("File Translator initialized")
    
    def is_supported_format(self, file_path: str) -> bool:
        """Check if file format is supported."""
        return Path(file_path).suffix.lower() in self.SUPPORTED_FORMATS
    
    def translate_text_file(self, input_path: str, output_path: str, 
                           src_lang: str, tgt_lang: str, 
                           preserve_formatting: bool = True) -> Dict:
        """
        Translate a plain text file.
        
        Args:
            input_path: Path to input text file
            output_path: Path to output translated file
            src_lang: Source language code
            tgt_lang: Target language code
            preserve_formatting: Whether to preserve line breaks and formatting
            
        Returns:
            Translation statistics
        """
        try:
            logger.info(f"Translating text file: {input_path}")
            start_time = time.time()
            
            # Read input file
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if preserve_formatting:
                # Translate line by line to preserve formatting
                lines = content.split('\n')
                translated_lines = []
                
                for line in lines:
                    if line.strip():  # Only translate non-empty lines
                        translated = self.translator.translate(line.strip(), src_lang, tgt_lang)
                        translated_lines.append(translated)
                    else:
                        translated_lines.append(line)  # Preserve empty lines
                
                translated_content = '\n'.join(translated_lines)
            else:
                # Translate entire content as one block
                translated_content = self.translator.translate(content, src_lang, tgt_lang)
            
            # Write output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            end_time = time.time()
            
            stats = {
                'input_file': input_path,
                'output_file': output_path,
                'src_lang': src_lang,
                'tgt_lang': tgt_lang,
                'original_length': len(content),
                'translated_length': len(translated_content),
                'lines_processed': len(lines) if preserve_formatting else 1,
                'processing_time': round(end_time - start_time, 2),
                'status': 'success'
            }
            
            logger.info(f"Text file translation completed in {stats['processing_time']}s")
            return stats
            
        except Exception as e:
            logger.error(f"Text file translation failed: {str(e)}")
            raise
    
    def translate_json_file(self, input_path: str, output_path: str,
                           src_lang: str, tgt_lang: str,
                           fields_to_translate: List[str] = None) -> Dict:
        """
        Translate specific fields in a JSON file.
        
        Args:
            input_path: Path to input JSON file
            output_path: Path to output translated file
            src_lang: Source language code
            tgt_lang: Target language code
            fields_to_translate: List of field names to translate (if None, translate all string values)
            
        Returns:
            Translation statistics
        """
        try:
            logger.info(f"Translating JSON file: {input_path}")
            start_time = time.time()
            
            # Read JSON file
            with open(input_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            translations_count = 0
            
            def translate_recursive(obj, path=""):
                nonlocal translations_count
                
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        current_path = f"{path}.{key}" if path else key
                        
                        if isinstance(value, str) and value.strip():
                            # Check if we should translate this field
                            if fields_to_translate is None or key in fields_to_translate:
                                obj[key] = self.translator.translate(value, src_lang, tgt_lang)
                                translations_count += 1
                                logger.info(f"Translated field '{current_path}': {value[:50]}...")
                        elif isinstance(value, (dict, list)):
                            translate_recursive(value, current_path)
                
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        translate_recursive(item, f"{path}[{i}]")
            
            # Translate the data
            translate_recursive(data)
            
            # Write output file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            end_time = time.time()
            
            stats = {
                'input_file': input_path,
                'output_file': output_path,
                'src_lang': src_lang,
                'tgt_lang': tgt_lang,
                'fields_translated': translations_count,
                'fields_to_translate': fields_to_translate,
                'processing_time': round(end_time - start_time, 2),
                'status': 'success'
            }
            
            logger.info(f"JSON file translation completed: {translations_count} fields in {stats['processing_time']}s")
            return stats
            
        except Exception as e:
            logger.error(f"JSON file translation failed: {str(e)}")
            raise
    
    def translate_csv_file(self, input_path: str, output_path: str,
                          src_lang: str, tgt_lang: str,
                          columns_to_translate: List[str] = None) -> Dict:
        """
        Translate specific columns in a CSV file.
        
        Args:
            input_path: Path to input CSV file
            output_path: Path to output translated file
            src_lang: Source language code
            tgt_lang: Target language code
            columns_to_translate: List of column names to translate (if None, translate all text columns)
            
        Returns:
            Translation statistics
        """
        try:
            logger.info(f"Translating CSV file: {input_path}")
            start_time = time.time()
            
            translated_rows = []
            translations_count = 0
            
            # Read CSV file
            with open(input_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                
                # Determine which columns to translate
                if columns_to_translate is None:
                    # Auto-detect text columns by checking first few rows
                    columns_to_translate = headers  # Translate all by default
                
                for row_num, row in enumerate(reader):
                    translated_row = row.copy()
                    
                    for column in columns_to_translate:
                        if column in row and row[column] and row[column].strip():
                            try:
                                translated_value = self.translator.translate(
                                    row[column], src_lang, tgt_lang
                                )
                                translated_row[column] = translated_value
                                translations_count += 1
                                
                                if row_num < 3:  # Log first few translations
                                    logger.info(f"Translated column '{column}': {row[column][:30]}...")
                                    
                            except Exception as e:
                                logger.warning(f"Failed to translate row {row_num}, column '{column}': {e}")
                                # Keep original value if translation fails
                                translated_row[column] = row[column]
                    
                    translated_rows.append(translated_row)
            
            # Write output CSV
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                if translated_rows:
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(translated_rows)
            
            end_time = time.time()
            
            stats = {
                'input_file': input_path,
                'output_file': output_path,
                'src_lang': src_lang,
                'tgt_lang': tgt_lang,
                'rows_processed': len(translated_rows),
                'cells_translated': translations_count,
                'columns_translated': columns_to_translate,
                'processing_time': round(end_time - start_time, 2),
                'status': 'success'
            }
            
            logger.info(f"CSV file translation completed: {translations_count} cells in {stats['processing_time']}s")
            return stats
            
        except Exception as e:
            logger.error(f"CSV file translation failed: {str(e)}")
            raise
    
    def translate_file(self, input_path: str, output_path: str = None,
                      src_lang: str = None, tgt_lang: str = None,
                      **kwargs) -> Dict:
        """
        Auto-detect file type and translate accordingly.
        
        Args:
            input_path: Path to input file
            output_path: Path to output file (auto-generated if None)
            src_lang: Source language code
            tgt_lang: Target language code
            **kwargs: Additional arguments specific to file type
            
        Returns:
            Translation statistics
        """
        # Validate inputs
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if not self.is_supported_format(input_path):
            raise ValueError(f"Unsupported file format. Supported: {self.SUPPORTED_FORMATS}")
        
        # Auto-generate output path if not provided
        if output_path is None:
            input_path_obj = Path(input_path)
            output_path = str(input_path_obj.parent / f"{input_path_obj.stem}_translated_{tgt_lang}{input_path_obj.suffix}")
        
        # Get file extension
        file_ext = Path(input_path).suffix.lower()
        
        # Route to appropriate translator
        if file_ext == '.txt':
            return self.translate_text_file(input_path, output_path, src_lang, tgt_lang, **kwargs)
        elif file_ext == '.json':
            return self.translate_json_file(input_path, output_path, src_lang, tgt_lang, **kwargs)
        elif file_ext == '.csv':
            return self.translate_csv_file(input_path, output_path, src_lang, tgt_lang, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
