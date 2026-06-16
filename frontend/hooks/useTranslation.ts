'use client';

import { useLanguage } from '@/context/LanguageContext';
import { t, getTranslations, Language } from '@/lib/i18n';

/**
 * Hook for translation with current language
 * Provides instant translation without API delays
 * 
 * @returns Object with t() function and current language
 * 
 * @example
 * const { t, language } = useTranslation();
 * return <button>{t('common.save')}</button>
 */
export function useTranslation() {
  const { language } = useLanguage();

  return {
    /**
     * Translate a key
     * @param key - Translation key (e.g., 'auth.login', 'messages.0')
     * @param fallback - Optional fallback text
     */
    t: (key: string, fallback?: string) => t(language, key, fallback),
    
    /**
     * Get all translations for current language
     */
    translations: getTranslations(language),
    
    /**
     * Current language code
     */
    language,
  };
}
