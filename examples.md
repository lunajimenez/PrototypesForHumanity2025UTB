# Ejemplos de Uso de la API v2.0

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
  "gpu_available": false,
  "available_methods": ["transformers", "textblob", "vader"],
  "default_method": "transformers"
}
```

### 3. Ver métodos disponibles

```bash
curl http://localhost:8000/methods
```

**Respuesta esperada:**
```json
{
  "available_methods": {
    "transformers": {
      "description": "Modelo BERT multilingüe avanzado (Opción 2 del proyecto)",
      "advantages": ["Alta precisión", "Multilingüe", "Contexto avanzado"],
      "disadvantages": ["Más lento", "Requiere más recursos"]
    },
    "textblob": {
      "description": "Análisis rápido y eficiente con TextBlob",
      "advantages": ["Rápido", "Ligero", "Fácil de usar"],
      "disadvantages": ["Menos preciso", "Optimizado para inglés"]
    },
    "vader": {
      "description": "Análisis basado en reglas léxicas (VADER)",
      "advantages": ["Muy rápido", "No requiere modelos", "Bueno para redes sociales"],
      "disadvantages": ["Basado en reglas", "Menos contexto"]
    }
  },
  "default_method": "transformers",
  "recommendations": {
    "transformers": "Para análisis de alta precisión y multilingüe",
    "textblob": "Para análisis rápido y eficiente",
    "vader": "Para análisis en tiempo real y redes sociales"
  }
}
```

## 📝 Ejemplos de Validación con Diferentes Métodos

### Ejemplo 1: Usando Transformers (Método por defecto - Opción 2 del proyecto)

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "¡Me encanta este proyecto! Es muy interesante y útil para la comunidad.",
       "language": "es",
       "sentiment_method": "transformers"
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
  "confidence": 0.95,
  "sentiment_method": "transformers",
  "method_info": {
    "description": "Modelo BERT multilingüe avanzado (Opción 2 del proyecto)",
    "advantages": ["Alta precisión", "Multilingüe", "Contexto avanzado"],
    "disadvantages": ["Más lento", "Requiere más recursos"]
  },
  "processing_time": 1.234
}
```

### Ejemplo 2: Usando TextBlob (Análisis rápido)

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Este producto es terrible, no funciona nada bien.",
       "language": "es",
       "sentiment_method": "textblob"
     }'
```

**Respuesta esperada:**
```json
{
  "original_text": "Este producto es terrible, no funciona nada bien.",
  "is_offensive": true,
  "has_profanity": false,
  "emotion_score": -0.8,
  "emotion_label": "Muy Negativo",
  "profanity_count": 0,
  "suggestions": [
    "Considera usar palabras más positivas y constructivas",
    "Evita términos que puedan generar emociones negativas",
    "Enfócate en soluciones en lugar de problemas"
  ],
  "corrected_text": "Este producto es terrible, no funciona nada bien.",
  "confidence": 0.8,
  "sentiment_method": "textblob",
  "method_info": {
    "description": "Análisis rápido y eficiente con TextBlob",
    "advantages": ["Rápido", "Ligero", "Fácil de usar"],
    "disadvantages": ["Menos preciso", "Optimizado para inglés"]
  },
  "processing_time": 0.045
}
```

### Ejemplo 3: Usando VADER (Análisis en tiempo real)

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Estoy muy decepcionado con los resultados del proyecto",
       "language": "es",
       "sentiment_method": "vader"
     }'
```

**Respuesta esperada:**
```json
{
  "original_text": "Estoy muy decepcionado con los resultados del proyecto",
  "is_offensive": true,
  "has_profanity": false,
  "emotion_score": -0.6,
  "emotion_label": "Negativo",
  "profanity_count": 0,
  "suggestions": [
    "Considera usar palabras más positivas y constructivas",
    "Evita términos que puedan generar emociones negativas",
    "Enfócate en soluciones en lugar de problemas"
  ],
  "corrected_text": "Estoy muy decepcionado con los resultados del proyecto",
  "confidence": 0.6,
  "sentiment_method": "vader",
  "method_info": {
    "description": "Análisis basado en reglas léxicas (VADER)",
    "advantages": ["Muy rápido", "No requiere modelos", "Bueno para redes sociales"],
    "disadvantages": ["Basado en reglas", "Menos contexto"]
  },
  "processing_time": 0.012
}
```

### Ejemplo 4: Texto con Groserías (Cualquier método)

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Este código es una mierda, el desarrollador es un gilipollas",
       "language": "es",
       "sentiment_method": "transformers"
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
  "confidence": 0.6,
  "sentiment_method": "transformers",
  "method_info": {...},
  "processing_time": 1.156
}
```

## 🔬 Comparación de Métodos

### Comparar todos los métodos con el mismo texto

```bash
# Texto positivo
text="¡Este proyecto es increíble! Me encanta mucho."

echo "=== TRANSFORMERS ==="
curl -s -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"$text\", \"language\": \"es\", \"sentiment_method\": \"transformers\"}" | jq '.emotion_score, .emotion_label, .processing_time'

echo "=== TEXTBLOB ==="
curl -s -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"$text\", \"language\": \"es\", \"sentiment_method\": \"textblob\"}" | jq '.emotion_score, .emotion_label, .processing_time'

echo "=== VADER ==="
curl -s -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d "{\"text\": \"$text\", \"language\": \"es\", \"sentiment_method\": \"vader\"}" | jq '.emotion_score, .emotion_label, .processing_time'
```

## 📊 Validación en Lote

### Procesar múltiples textos

```bash
curl -X POST "http://localhost:8000/validate/batch" \
     -H "Content-Type: application/json" \
     -G -d "method=transformers" \
     -d '[
       "Excelente trabajo equipo!",
       "Me siento frustrado con los resultados",
       "Este es un proyecto increíble",
       "No puedo creer lo mal que está esto"
     ]'
```

**Respuesta esperada:**
```json
{
  "method": "transformers",
  "total_texts": 4,
  "valid_texts": 4,
  "results": [
    {
      "text": "Excelente trabajo equipo!",
      "is_offensive": false,
      "emotion_score": 0.9,
      "emotion_label": "Muy Positivo",
      "profanity_count": 0,
      "valid": true
    },
    {
      "text": "Me siento frustrado con los resultados",
      "is_offensive": true,
      "emotion_score": 0.3,
      "emotion_label": "Negativo",
      "profanity_count": 0,
      "valid": true
    }
  ]
}
```

## 🔧 Uso con Python

### Cliente Python con Selección de Método

```python
import requests
import json

def validate_text(text, language="es", method="transformers"):
    """Valida un texto usando la API con método específico"""
    url = "http://localhost:8000/validate"
    payload = {
        "text": text,
        "language": language,
        "sentiment_method": method
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la API: {e}")
        return None

def compare_methods(text):
    """Compara todos los métodos de análisis para un texto"""
    methods = ["transformers", "textblob", "vader"]
    results = {}
    
    for method in methods:
        result = validate_text(text, method=method)
        if result:
            results[method] = {
                "score": result['emotion_score'],
                "label": result['emotion_label'],
                "confidence": result['confidence'],
                "processing_time": result['processing_time']
            }
    
    return results

# Ejemplos de uso
texts = [
    "¡Excelente trabajo equipo!",
    "Este producto es una basura",
    "Necesito ayuda con mi proyecto"
]

print("=== Análisis con Transformers (Opción 2 del proyecto) ===")
for text in texts:
    result = validate_text(text, method="transformers")
    if result:
        print(f"Texto: '{text[:50]}...'")
        print(f"  Score: {result['emotion_score']:.3f} ({result['emotion_label']})")
        print(f"  Tiempo: {result['processing_time']:.3f}s")

print("\n=== Comparación de Métodos ===")
comparison = compare_methods("Este proyecto es increíble!")
for method, data in comparison.items():
    print(f"{method.upper()}: Score={data['score']:.3f}, Time={data['processing_time']:.3f}s")
```

## 🌐 Uso con JavaScript/Fetch

### Cliente JavaScript con Múltiples Métodos

```javascript
async function validateText(text, language = 'es', method = 'transformers') {
    const url = 'http://localhost:8000/validate';
    const payload = {
        text: text,
        language: language,
        sentiment_method: method
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

async function compareAllMethods(text) {
    const methods = ['transformers', 'textblob', 'vader'];
    const results = {};
    
    for (const method of methods) {
        const result = await validateText(text, 'es', method);
        if (result) {
            results[method] = {
                score: result.emotion_score,
                label: result.emotion_label,
                confidence: result.confidence,
                processingTime: result.processing_time
            };
        }
    }
    
    return results;
}

// Ejemplo de uso
const text = "Este código es increíble, me encanta!";

// Análisis con método específico
validateText(text, 'es', 'textblob').then(result => {
    if (result) {
        console.log('Resultado TextBlob:', result);
        console.log('Score:', result.emotion_score);
        console.log('Tiempo:', result.processing_time);
    }
});

// Comparar todos los métodos
compareAllMethods(text).then(results => {
    console.log('Comparación de métodos:', results);
    
    // Encontrar el más rápido
    const fastest = Object.entries(results).reduce((a, b) => 
        a[1].processingTime < b[1].processingTime ? a : b
    );
    console.log('Método más rápido:', fastest[0]);
});
```

## 📈 Análisis de Rendimiento

### Script de Benchmark

```bash
#!/bin/bash

echo "🚀 Benchmark de Métodos de Análisis de Sentimientos"
echo "=================================================="

text="Este es un texto de prueba para medir el rendimiento de diferentes métodos de análisis de sentimientos."

methods=("transformers" "textblob" "vader")
iterations=10

for method in "${methods[@]}"; do
    echo -e "\n🔍 Probando método: $method"
    times=()
    
    for i in $(seq 1 $iterations); do
        start_time=$(date +%s.%N)
        
        response=$(curl -s -X POST "http://localhost:8000/validate" \
            -H "Content-Type: application/json" \
            -d "{\"text\": \"$text\", \"language\": \"es\", \"sentiment_method\": \"$method\"}")
        
        end_time=$(date +%s.%N)
        
        # Calcular tiempo
        elapsed=$(echo "$end_time - $start_time" | bc)
        times+=($elapsed)
        
        echo "  Ejecución $i: ${elapsed}s"
    done
    
    # Calcular promedio
    total=0
    for t in "${times[@]}"; do
        total=$(echo "$total + $t" | bc)
    done
    avg=$(echo "scale=3; $total / ${#times[@]}" | bc)
    
    echo "  ⏱️  Tiempo promedio: ${avg}s"
done

echo -e "\n🏁 Benchmark completado!"
```

## 🎯 Casos de Uso por Método

### 1. Transformers (BERT) - Opción 2 del proyecto
- **Cuándo usar**: Análisis de alta precisión, textos en español, contexto importante
- **Ejemplo**: Revisar posts importantes antes de publicar en redes sociales profesionales

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Nuestro nuevo producto revoluciona el mercado con tecnología de vanguardia",
       "language": "es",
       "sentiment_method": "transformers"
     }'
```

### 2. TextBlob - Análisis rápido
- **Cuándo usar**: Análisis en tiempo real, múltiples textos, recursos limitados
- **Ejemplo**: Moderación de comentarios en tiempo real

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Great product, I love it!",
       "language": "en",
       "sentiment_method": "textblob"
     }'
```

### 3. VADER - Tiempo real
- **Cuándo usar**: Análisis instantáneo, redes sociales, textos cortos
- **Ejemplo**: Validación de tweets antes de publicar

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "¡Increíble día! #feliz #contento",
       "language": "es",
       "sentiment_method": "vader"
     }'
```

## 🔍 Monitoreo y Debugging

### Verificar Estado de la API

```bash
# Health check
curl http://localhost:8000/health

# Información general
curl http://localhost:8000/

# Métodos disponibles
curl http://localhost:8000/methods

# Comparación de métodos
curl http://localhost:8000/compare

# Logs del servidor (en la terminal donde ejecutaste main.py)
```

### Métricas de Rendimiento

```bash
# Medir tiempo de respuesta por método
time curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Texto de prueba", "language": "es", "sentiment_method": "transformers"}'

time curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Texto de prueba", "language": "es", "sentiment_method": "textblob"}'

time curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Texto de prueba", "language": "es", "sentiment_method": "vader"}'
```

## 🚨 Casos de Error

### Método no válido

```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Texto de prueba",
       "language": "es",
       "sentiment_method": "metodo_invalido"
     }'
```

**Respuesta esperada:**
```json
{
  "detail": "Método 'metodo_invalido' no válido. Métodos disponibles: ['transformers', 'textblob', 'vader']"
}
```

### Texto vacío

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

## 🎉 Resumen de Nuevas Funcionalidades

### ✨ **API v2.0 - Características Principales:**

1. **Múltiples Métodos de Análisis**:
   - **Transformers (BERT)**: Opción 2 del proyecto existente - Alta precisión
   - **TextBlob**: Análisis rápido y eficiente
   - **VADER**: Análisis en tiempo real para redes sociales

2. **Nuevos Endpoints**:
   - `/methods` - Información detallada de métodos
   - `/compare` - Comparación de métodos
   - `/validate/batch` - Validación en lote

3. **Métricas Mejoradas**:
   - Tiempo de procesamiento por método
   - Información del método utilizado
   - Comparación de rendimiento

4. **Flexibilidad**:
   - Selección de método por solicitud
   - Análisis adaptativo según necesidades
   - Compatibilidad con el proyecto existente

---

**💡 Tip**: Usa `jq` para formatear las respuestas JSON de manera más legible:

```bash
curl -s -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Texto de prueba", "language": "es", "sentiment_method": "textblob"}' | jq '.'
``` 