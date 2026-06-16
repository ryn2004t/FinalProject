# Multi-Language Localization Guide

## Overview

Vertex now supports 6 languages with **zero-delay translations** using cached JSON files:

- 🇬🇧 **English** (en)
- 🇷🇺 **Russian** (ru)
- 🇪🇸 **Spanish** (es)
- 🇫🇷 **French** (fr)
- 🇨🇳 **Chinese** (zh)
- 🇯🇵 **Japanese** (ja)

## Frontend Usage (React/TypeScript)

### 1. Setup in Layout

Wrap your app with `LanguageProvider` in `frontend/app/layout.tsx`:

```typescript
import { LanguageProvider } from '@/context/LanguageContext';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <LanguageProvider>
          {children}
        </LanguageProvider>
      </body>
    </html>
  );
}
```

### 2. Use Hook in Components

```typescript
'use client';

import { useTranslation } from '@/hooks/useTranslation';

export function LoginForm() {
  const { t, language } = useTranslation();

  return (
    <form>
      <label>{t('auth.email')}</label>
      <input type="email" />
      
      <label>{t('auth.password')}</label>
      <input type="password" />
      
      <button>{t('auth.login')}</button>
      <a href="#">{t('auth.forgotPassword')}</a>
    </form>
  );
}
```

### 3. Add Language Switcher

```typescript
import { LanguageSwitcher } from '@/components/LanguageSwitcher';

export function Navbar() {
  return (
    <nav>
      <h1>Vertex</h1>
      <LanguageSwitcher />
    </nav>
  );
}
```

### 4. Translation Key Format

Use dot notation for nested keys:

```typescript
t('common.appName')        // "Vertex"
t('auth.login')            // "Login"
t('jobseeker.uploadCV')    // "Upload CV"
t('messages.0')            // First message
```

### 5. With Fallback

```typescript
t('custom.key', 'Default Text')  // Returns 'Default Text' if key not found
```

## Backend Usage (Python FastAPI)

### 1. Basic Translation

```python
from app.services.localization_service import LocalizationService, Language, t

# Using singleton
service = LocalizationService()
text = service.get_translation(Language.EN, 'auth.login')
print(text)  # "Login"

# Using helper
text = t(Language.RU, 'common.save')
print(text)  # "Сохранить"
```

### 2. In API Endpoints

```python
from fastapi import FastAPI, Header
from app.services.localization_service import LocalizationService, get_lang_from_header, Language

app = FastAPI()
localization = LocalizationService()

@app.get("/api/messages")
async def get_messages(accept_language: str = Header(None)):
    language = get_lang_from_header(accept_language)
    
    return {
        "success": localization.get_translation(language, 'messages.0'),
        "error": localization.get_translation(language, 'messages.3'),
    }
```

### 3. Translate Multiple Keys

```python
to_translate = {
    'submit_label': 'common.submit',
    'cancel_label': 'common.cancel',
    'save_label': 'common.save',
}

result = localization.translate_object(Language.FR, to_translate)
print(result)
# {'submit_label': 'Soumettre', 'cancel_label': 'Annuler', 'save_label': 'Enregistrer'}
```

### 4. Get All Languages

```python
languages = localization.get_supported_languages()
print(languages)  # ['en', 'ru', 'es', 'fr', 'zh', 'ja']

lang_names = localization.get_language_names(Language.EN)
print(lang_names)  # {'en': 'English', 'ru': 'Русский', ...}
```

## Translation File Structure

Each language file (`frontend/locales/{language}.json`) has this structure:

```json
{
  "common": {
    "appName": "Vertex",
    "tagline": "Job Matching & Talent Platform",
    "loading": "Loading...",
    "save": "Save",
    "cancel": "Cancel"
  },
  "auth": {
    "login": "Login",
    "email": "Email",
    "password": "Password"
  },
  "jobseeker": { },
  "company": { },
  "jobs": { },
  "notifications": { },
  "profile": { },
  "messages": []
}
```

## Adding New Translations

### 1. Add to All Language Files

Edit `frontend/locales/en.json`:

```json
{
  "common": {
    "newFeature": "New Feature"
  }
}
```

Then add to all other language files (`ru.json`, `es.json`, `fr.json`, `zh.json`, `ja.json`).

### 2. Use in Code

```typescript
const { t } = useTranslation();
return <div>{t('common.newFeature')}</div>;
```

## Performance

✅ **ZERO-DELAY**: All translations cached in memory  
✅ **Fast Lookups**: O(1) dictionary access  
✅ **No API Calls**: Translations loaded at startup  
✅ **Instant Language Switch**: No page reload needed  
✅ **Small Footprint**: ~15KB JSON for all 6 languages  

## Browser Preference

The app automatically detects browser language:

```typescript
// If browser language is Spanish, app loads in Spanish by default
// User can manually switch anytime
// Selection is saved to localStorage
```

## Accept-Language Header

Backend reads Accept-Language header for API responses:

```bash
curl -H "Accept-Language: fr-FR" http://localhost:8000/api/messages
# Returns French translations
```

## Directory Structure

```
frontend/
├── locales/
│   ├── en.json        # English translations
│   ├── ru.json        # Russian translations
│   ├── es.json        # Spanish translations
│   ├── fr.json        # French translations
│   ├── zh.json        # Chinese translations
│   └── ja.json        # Japanese translations
├── lib/
│   └── i18n.ts        # Translation utilities
├── context/
│   └── LanguageContext.tsx    # Language state
├── hooks/
│   └── useTranslation.ts      # Hook for using translations
└── components/
    └── LanguageSwitcher.tsx   # Language selector component

app/
└── services/
    └── localization_service.py    # Backend service
```

## Common Issues

### Missing Translation

```typescript
// If key not found, returns the key itself
t('missing.key')  // "missing.key"

// Or provide fallback
t('missing.key', 'Default Text')  // "Default Text"
```

### Language Not Switching

Ensure `LanguageProvider` wraps your app:

```typescript
// ❌ Won't work - no provider
const { t } = useTranslation();

// ✅ Correct - inside LanguageProvider
<LanguageProvider>
  <App />
</LanguageProvider>
```

### Server-Side Rendering

```typescript
// Use 'use client' directive in components using useTranslation()
'use client';

import { useTranslation } from '@/hooks/useTranslation';
```

## Updating Translations

1. Edit the appropriate language file in `frontend/locales/`
2. The app automatically reloads translations (no build needed in development)
3. In production, redeploy the frontend

## Testing

```typescript
import { t, getTranslations } from '@/lib/i18n';

// Test English
expect(t('en', 'common.save')).toBe('Save');

// Test Russian
expect(t('ru', 'common.save')).toBe('Сохранить');

// Test all languages
const langs = ['en', 'ru', 'es', 'fr', 'zh', 'ja'];
lang forEach(lang => {
  const trans = getTranslations(lang);
  expect(trans.common.save).toBeDefined();
});
```

## Support

For issues or new translations, update the JSON files and redeploy.
