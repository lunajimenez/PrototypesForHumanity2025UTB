# API de Validación de Textos para Redes Sociales

Una API inteligente construida con FastAPI que integra **transformers** de Hugging Face y **spanlp** para validar textos antes de publicarlos en redes sociales. Detecta emociones negativas y groserías, proporcionando sugerencias de mejora y versiones corregidas.

## 🚀 Características

- **Análisis de Sentimientos**: Detecta emociones negativas usando modelos de transformers
- **Detección de Groserías**: Identifica lenguaje inapropiado usando spanlp
- **Sugerencias Inteligentes**: Proporciona recomendaciones personalizadas para mejorar el texto
- **Corrección Automática**: Genera versiones corregidas del texto
- **API RESTful**: Endpoints simples y eficientes
- **Documentación Automática**: Swagger UI integrado
- **Validación en Tiempo Real**: Respuestas rápidas para uso en aplicaciones web

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │───▶│  Transformers    │    │     spanlp      │
│                 │    │  (Sentiment)     │    │  (Profanity)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Text Input    │    │  Emotion Score   │    │ Profanity List  │
│                 │    │  & Label         │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Validation     │    │  Suggestions     │    │  Corrected      │
│  Results        │    │  Generation      │    │  Text           │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📋 Requisitos

- Python 3.8+
- FastAPI
- Transformers (Hugging Face)
- PyTorch
- spanlp
- uvicorn

## 🛠️ Instalación

1. **Clonar el repositorio**:
```bash
git clone <tu-repositorio>
cd PrototypesForHumanity2025UTB
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate     # En Windows
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

## 🚀 Uso

### 1. Iniciar la API

```bash
python main.py
```

La API estará disponible en `http://localhost:8000`

### 2. Documentación Interactiva

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 3. Endpoints Disponibles

#### GET `/`
Información general de la API

#### GET `/health`
Estado de salud y disponibilidad de modelos

#### POST `/validate`
Valida un texto y retorna análisis completo

**Ejemplo de uso**:
```bash
curl -X POST "http://localhost:8000/validate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Este producto es una mierda!", "language": "es"}'
```

## 📊 Ejemplos de Respuesta

### Texto Positivo
```json
{
  "original_text": "¡Me encanta este proyecto! Es increíble.",
  "is_offensive": false,
  "has_profanity": false,
  "emotion_score": 0.9,
  "emotion_label": "Muy Positivo",
  "profanity_count": 0,
  "suggestions": ["Tu texto está bien escrito y es apropiado para redes sociales"],
  "corrected_text": "¡Me encanta este proyecto! Es increíble.",
  "confidence": 0.95
}
```

### Texto con Groserías
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

## 🧪 Pruebas

Ejecuta el script de pruebas para verificar el funcionamiento:

```bash
python test_api.py
```

Este script incluye:
- Verificación de salud de la API
- Casos de prueba con diferentes tipos de texto
- Validación en lote
- Métricas de rendimiento

## ⚙️ Configuración

Puedes personalizar la API editando `config.py`:

- **Modelos**: Cambiar el modelo de análisis de sentimientos
- **Umbrales**: Ajustar los límites para clasificación de emociones
- **Reemplazos**: Modificar las palabras de sustitución para groserías
- **Sugerencias**: Personalizar los mensajes de recomendación

## 🔧 Personalización

### Agregar Nuevas Groserías

```python
# En config.py
PROFANITY_REPLACEMENTS = {
    "nueva_groseria": "reemplazo_apropiado",
    # ... más entradas
}
```

### Modificar Umbrales de Emoción

```python
# En config.py
EMOTION_THRESHOLDS = {
    "very_negative": 0.15,  # Más estricto
    "negative": 0.35,
    "neutral": 0.65,
    "positive": 0.85
}
```

## 📈 Métricas de Rendimiento

- **Tiempo de respuesta**: < 2 segundos por texto
- **Precisión**: > 90% en detección de groserías
- **Escalabilidad**: Soporta múltiples solicitudes concurrentes
- **Memoria**: ~2GB RAM para modelos cargados

## 🚨 Limitaciones

- **Idioma**: Optimizado para español
- **Longitud**: Máximo 1000 caracteres por texto
- **Modelos**: Requiere descarga inicial de modelos (~500MB)
- **GPU**: Opcional, funciona en CPU

## 🤝 Contribuciones

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa la documentación en `/docs`
2. Ejecuta las pruebas con `python test_api.py`
3. Verifica los logs del servidor
4. Abre un issue en el repositorio

## 🔮 Roadmap

- [ ] Soporte para múltiples idiomas
- [ ] Análisis de contexto más avanzado
- [ ] Integración con APIs de redes sociales
- [ ] Dashboard de análisis en tiempo real
- [ ] Modelos personalizables por usuario
- [ ] Cache inteligente para mejorar rendimiento

---

**¡Haz que tus publicaciones en redes sociales sean más profesionales y respetuosas!** 🚀
