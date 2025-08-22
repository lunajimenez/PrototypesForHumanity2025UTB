# Ejemplos de Uso de la API

## 🚀 Inicio Rápido

### 1. Iniciar la API

**Linux/Mac:**
```bash
./start_api.sh
```

**Windows:**
```cmd
start_api.bat
```

**Manual:**
```bash
python main.py
```

### 2. Verificar que la API esté funcionando

```bash
curl http://localhost:8000/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "models_loaded": true,
  "gpu_available": false
}
```

## 📝 Ejemplos de Validación de Textos

### Ejemplo 1: Texto Positivo

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "¡Me encanta este proyecto! Es muy interesante y útil para la comunidad.",
       "language": "es"
     }'
```

**Respuesta esperada:**
```json
{
  "original_text": "¡Me encanta este proyecto! Es muy interesante y útil para la comunidad.",
  "is_offensive": false,
  "has_profanity": false,
  "emotion_score": 0.9,
  "emotion_label": "Muy Positivo",
  "profanity_count": 0,
  "suggestions": ["Tu texto está bien escrito y es apropiado para redes sociales"],
  "corrected_text": "¡Me encanta este proyecto! Es muy interesante y útil para la comunidad.",
  "confidence": 0.95
}
```

### Ejemplo 2: Texto con Groserías

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Este código es una mierda, el desarrollador es un gilipollas",
       "language": "es"
     }'
```

**Respuesta esperada:**
```json
{
  "original_text": "Este código es una mierda, el desarrollador es un gilipollas",
  "is_offensive": true,
  "has_profanity": true,
  "emotion_score": 0.2,
  "emotion_label": "Muy Negativo",
  "profanity_count": 2,
  "suggestions": [
    "Reemplaza las groserías con palabras más apropiadas",
    "Usa un lenguaje más profesional y respetuoso",
    "Considera el impacto de tus palabras en diferentes audiencias"
  ],
  "corrected_text": "Este código es un problema, el desarrollador es una persona",
  "confidence": 0.6
}
```

### Ejemplo 3: Texto Negativo sin Groserías

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Estoy muy decepcionado con los resultados del proyecto",
       "language": "es"
     }'
```

**Respuesta esperada:**
```json
{
  "original_text": "Estoy muy decepcionado con los resultados del proyecto",
  "is_offensive": true,
  "has_profanity": false,
  "emotion_score": 0.3,
  "emotion_label": "Negativo",
  "profanity_count": 0,
  "suggestions": [
    "Considera usar palabras más positivas y constructivas",
    "Evita términos que puedan generar emociones negativas",
    "Enfócate en soluciones en lugar de problemas"
  ],
  "corrected_text": "Estoy muy decepcionado con los resultados del proyecto",
  "confidence": 0.8
}
```

## 🔧 Uso con Python

### Cliente Python Simple

```python
import requests
import json

def validate_text(text, language="es"):
    """Valida un texto usando la API"""
    url = "http://localhost:8000/validate"
    payload = {
        "text": text,
        "language": language
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la API: {e}")
        return None

# Ejemplos de uso
texts = [
    "¡Excelente trabajo equipo!",
    "Este producto es una basura",
    "Necesito ayuda con mi proyecto"
]

for text in texts:
    print(f"\n📝 Validando: '{text}'")
    result = validate_text(text)
    if result:
        print(f"   Es ofensivo: {result['is_offensive']}")
        print(f"   Emoción: {result['emotion_label']} ({result['emotion_score']:.2f})")
        print(f"   Groserías: {result['profanity_count']}")
        print(f"   Sugerencia: {result['suggestions'][0]}")
```

## 🌐 Uso con JavaScript/Fetch

### Cliente JavaScript

```javascript
async function validateText(text, language = 'es') {
    const url = 'http://localhost:8000/validate';
    const payload = {
        text: text,
        language: language
    };
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error en la API:', error);
        return null;
    }
}

// Ejemplo de uso
const text = "Este código es increíble, me encanta!";
validateText(text).then(result => {
    if (result) {
        console.log('Resultado:', result);
        console.log('Es ofensivo:', result.is_offensive);
        console.log('Emoción:', result.emotion_label);
    }
});
```

## 📊 Análisis en Lote

### Script de Validación Múltiple

```bash
#!/bin/bash

# Lista de textos a validar
texts=(
    "¡Hola! ¿Cómo estás?"
    "Este producto es terrible"
    "Me encanta trabajar en este proyecto"
    "El servicio al cliente es pésimo"
    "Gracias por tu ayuda"
)

echo "🧪 Validando ${#texts[@]} textos..."

for text in "${texts[@]}"; do
    echo -e "\n--- Validando: '$text' ---"
    
    result=$(curl -s -X POST "http://localhost:8000/validate" \
        -H "Content-Type: application/json" \
        -d "{\"text\": \"$text\", \"language\": \"es\"}")
    
    if [ $? -eq 0 ]; then
        echo "✅ Éxito"
        echo "   Es ofensivo: $(echo $result | jq -r '.is_offensive')"
        echo "   Emoción: $(echo $result | jq -r '.emotion_label')"
        echo "   Groserías: $(echo $result | jq -r '.profanity_count')"
    else
        echo "❌ Error en la validación"
    fi
done
```

## 🔍 Monitoreo y Debugging

### Verificar Estado de la API

```bash
# Health check
curl http://localhost:8000/health

# Información general
curl http://localhost:8000/

# Logs del servidor (en la terminal donde ejecutaste main.py)
```

### Métricas de Rendimiento

```bash
# Medir tiempo de respuesta
time curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Texto de prueba", "language": "es"}'
```

## 🚨 Casos de Error

### Texto Vacío

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{"text": "", "language": "es"}'
```

**Respuesta esperada:**
```json
{
  "detail": "El texto no puede estar vacío"
}
```

### Texto Demasiado Largo

```bash
# Generar texto de más de 1000 caracteres
long_text=$(printf 'a%.0s' {1..1001})

curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"$long_text\", \"language\": \"es\"}"
```

**Respuesta esperada:**
```json
{
  "detail": "El texto es demasiado largo (máximo 1000 caracteres)"
}
```

## 🎯 Casos de Uso Comunes

### 1. Validación de Posts de Redes Sociales

```bash
# Antes de publicar en Twitter
text="¡Qué día tan horrible! Todo está saliendo mal"
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"$text\", \"language\": \"es\"}"
```

### 2. Revisión de Comentarios

```bash
# Validar comentario antes de aprobarlo
comment="Este artículo es muy útil, gracias por compartirlo"
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"$comment\", \"language\": \"es\"}"
```

### 3. Análisis de Feedback

```bash
# Analizar feedback de usuarios
feedback="El producto funciona bien pero podría mejorar"
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"$feedback\", \"language\": \"es\"}"
```

## 🔧 Personalización

### Cambiar Idioma (si se implementa en el futuro)

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "This is a test message",
       "language": "en"
     }'
```

### Headers Personalizados

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -H "User-Agent: MyApp/1.0" \
     -H "X-API-Key: my-key" \
     -d '{"text": "Texto de prueba", "language": "es"}'
```

---

**💡 Tip**: Usa `jq` para formatear las respuestas JSON de manera más legible:

```bash
curl -s -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Texto de prueba", "language": "es"}' | jq '.'
``` 