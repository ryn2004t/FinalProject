"""
Fast, zero-delay localization service for backend
All translations are cached in-memory
"""

import json
import os
from typing import Dict, Any, Optional
from enum import Enum

class Language(str, Enum):
    EN = "en"
    RU = "ru"
    ES = "es"
    FR = "fr"
    ZH = "zh"
    JA = "ja"

class LocalizationService:
    """Handles all localization with zero-delay cached translations"""
    
    _instance = None
    _translations: Dict[Language, Dict[str, Any]] = {}
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocalizationService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not LocalizationService._initialized:
            self._load_translations()
            LocalizationService._initialized = True

    def _load_translations(self) -> None:
        """Load all translation files into memory (one-time operation)"""
        frontend_locale_path = os.path.join(
            os.path.dirname(__file__), 
            '../../frontend/locales'
        )
        
        for lang in Language:
            file_path = os.path.join(frontend_locale_path, f"{lang.value}.json")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    LocalizationService._translations[lang] = json.load(f)
            except FileNotFoundError:
                print(f"Warning: Translation file not found for {lang.value}")
                LocalizationService._translations[lang] = {}

    def get_translation(self, language: Language, key: str, default: str = None) -> str:
        """
        Get a translation value using dot notation
        ZERO-DELAY: Returns instantly from memory cache
        
        Args:
            language: Language enum (en, ru, es, fr, zh, ja)
            key: Translation key using dot notation (e.g., 'auth.login', 'messages.0')
            default: Default value if translation not found
            
        Returns:
            Translated string or default value
            
        Example:
            service = LocalizationService()
            text = service.get_translation(Language.EN, 'common.appName')
        """
        translations = LocalizationService._translations.get(language, {})
        value = self._get_nested_value(translations, key)
        return value if value else (default or key)

    def get_all_translations(self, language: Language) -> Dict[str, Any]:
        """
        Get all translations for a language
        ZERO-DELAY: Returns instantly from memory cache
        """
        return LocalizationService._translations.get(language, {})

    def translate_object(self, language: Language, obj: Dict[str, str]) -> Dict[str, str]:
        """
        Translate multiple keys at once
        Useful for API responses
        
        Args:
            language: Target language
            obj: Dictionary with keys as translation keys and values as defaults
            
        Returns:
            Dictionary with translated values
            
        Example:
            to_translate = {'title': 'common.appName', 'button': 'common.save'}
            result = service.translate_object(Language.RU, to_translate)
            # result = {'title': 'Vertex', 'button': 'Сохранить'}
        """
        return {
            key: self.get_translation(language, value, value)
            for key, value in obj.items()
        }

    def get_supported_languages(self) -> list:
        """
        Get list of all supported languages
        Returns:
            List of language codes ['en', 'ru', 'es', 'fr', 'zh', 'ja']
        """
        return [lang.value for lang in Language]

    def get_language_names(self, language: Language = Language.EN) -> Dict[str, str]:
        """
        Get names of all languages in specified language
        
        Args:
            language: Language to return names in
            
        Returns:
            Dictionary with language codes as keys and names as values
        """
        language_names = {
            Language.EN: {'en': 'English', 'ru': 'Русский', 'es': 'Español', 'fr': 'Français', 'zh': '中文', 'ja': '日本語'},
            Language.RU: {'en': 'Английский', 'ru': 'Русский', 'es': 'Испанский', 'fr': 'Французский', 'zh': 'Китайский', 'ja': 'Японский'},
            Language.ES: {'en': 'Inglés', 'ru': 'Ruso', 'es': 'Español', 'fr': 'Francés', 'zh': 'Chino', 'ja': 'Japonés'},
            Language.FR: {'en': 'Anglais', 'ru': 'Russe', 'es': 'Espagnol', 'fr': 'Français', 'zh': 'Chinois', 'ja': 'Japonais'},
            Language.ZH: {'en': '英文', 'ru': '俄文', 'es': '西班牙文', 'fr': '法文', 'zh': '中文', 'ja': '日文'},
            Language.JA: {'en': '英語', 'ru': 'ロシア語', 'es': 'スペイン語', 'fr': 'フランス語', 'zh': '中国語', 'ja': '日本語'},
        }
        return language_names.get(language, language_names[Language.EN])

    @staticmethod
    def _get_nested_value(obj: Dict[str, Any], path: str) -> Optional[str]:
        """
        Get nested value from dictionary using dot notation
        Handles array indices too (e.g., 'messages.0')
        """
        parts = path.split('.')
        current = obj
        
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif isinstance(current, list):
                try:
                    index = int(part)
                    current = current[index]
                except (ValueError, IndexError):
                    return None
            else:
                return None
                
        return current if isinstance(current, str) else None


# Singleton instance
localization_service = LocalizationService()

# Helper functions for convenience
def t(language: Language, key: str, default: str = None) -> str:
    """
    Quick translation helper
    
    Usage:
        from app.services.localization_service import t, Language
        text = t(Language.EN, 'common.save')
    """
    return localization_service.get_translation(language, key, default)

def get_lang_from_header(accept_language: str = None) -> Language:
    """
    Extract language preference from Accept-Language header
    
    Args:
        accept_language: Accept-Language header value
        
    Returns:
        Language enum or Language.EN as default
    """
    if not accept_language:
        return Language.EN
    
    # Parse Accept-Language header
    langs = accept_language.lower().split(',')
    for lang_range in langs:
        lang_code = lang_range.split(';')[0].strip().split('-')[0]
        try:
            return Language(lang_code)
        except ValueError:
            continue
    
    return Language.EN
