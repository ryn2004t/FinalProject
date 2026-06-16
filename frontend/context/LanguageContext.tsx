'use client';

import React, { createContext, useState, useContext, useEffect } from 'react';
import { Language, getBrowserLanguage, SUPPORTED_LANGUAGES } from '@/lib/i18n';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  isLoading: boolean;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Language>('en');
  const [isLoading, setIsLoading] = useState(true);

  // Initialize language from localStorage or browser preference
  useEffect(() => {
    const storedLanguage = typeof window !== 'undefined' ? localStorage.getItem('language') : null;
    const initialLanguage = (storedLanguage as Language) || getBrowserLanguage();
    
    if (SUPPORTED_LANGUAGES.includes(initialLanguage)) {
      setLanguageState(initialLanguage);
    } else {
      setLanguageState('en');
    }
    setIsLoading(false);
  }, []);

  const setLanguage = (lang: Language) => {
    if (SUPPORTED_LANGUAGES.includes(lang)) {
      setLanguageState(lang);
      if (typeof window !== 'undefined') {
        localStorage.setItem('language', lang);
      }
    }
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, isLoading }}>
      {children}
    </LanguageContext.Provider>
  );
}

/**
 * Hook to use language context
 * @returns Language context with language, setLanguage, and isLoading
 */
export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
