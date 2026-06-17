// Fast, zero-delay translation system
// All translations are loaded statically - NO API CALLS

import en from '../locales/en.json';
import ru from '../locales/ru.json';
import es from '../locales/es.json';
import fr from '../locales/fr.json';
import zh from '../locales/zh.json';
import ja from '../locales/ja.json';

export type Language = 'en' | 'ru' | 'es' | 'fr' | 'zh' | 'ja';

const translations: Record<Language, any> = {
  en,
  ru,
  es,
  fr,
  zh,
  ja,
};

// Get nested translation value using dot notation
function getNestedValue(obj: any, path: string): string {
  return path.split('.').reduce((current, prop) => current?.[prop], obj) || path;
}

/**
 * Get translation for a key
 * @param language - Language code (en, ru, es, fr, zh, ja)
 * @param key - Translation key using dot notation (e.g., 'auth.login', 'messages.0')
 * @param fallback - Fallback text if translation not found
 * @returns Translated string
 */
export function t(language: Language, key: string, fallback?: string): string {
  const translation = getNestedValue(translations[language], key);
  return translation || fallback || key;
}

/**
 * Get all translations for a language
 * @param language - Language code
 * @returns Full translation object
 */
export function getTranslations(language: Language) {
  return translations[language];
}

/**
 * Get browser's preferred language
 * @returns Language code or 'en' as default
 */
export function getBrowserLanguage(): Language {
  const browserLang = typeof navigator !== 'undefined' ? navigator.language : 'en';
  const langCode = browserLang.split('-')[0].toLowerCase();
  
  const supportedLanguages: Language[] = ['en', 'ru', 'es', 'fr', 'zh', 'ja'];
  return supportedLanguages.includes(langCode as Language) ? (langCode as Language) : 'en';
}

/**
 * Get language name in English
 */
export function getLanguageName(language: Language): string {
  const names: Record<Language, string> = {
    en: 'English',
    ru: 'Русский',
    es: 'Español',
    fr: 'Français',
    zh: '中文',
    ja: '日本語',
  };
  return names[language];
}

/**
 * All supported languages
 */
export const SUPPORTED_LANGUAGES: Language[] = ['en', 'ru', 'es', 'fr', 'zh', 'ja'];
