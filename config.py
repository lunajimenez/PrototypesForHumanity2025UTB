"""
Configuración de la API de Validación de Textos
"""

# Configuración del servidor
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000
DEBUG = True

# Configuración de modelos
SENTIMENT_MODELS = {
    "transformers": "nlptown/bert-base-multilingual-uncased-sentiment",
    "textblob": "textblob",
    "vader": "vader"
}

DEFAULT_SENTIMENT_METHOD = "transformers"  # Opción 2 del proyecto existente
MAX_TEXT_LENGTH = 1000

# Umbrales para diferentes métodos
EMOTION_THRESHOLDS = {
    "transformers": {
        "very_negative": 0.2,
        "negative": 0.4,
        "neutral": 0.6,
        "positive": 0.8
    },
    "textblob": {
        "very_negative": -0.6,
        "negative": -0.1,
        "neutral": 0.1,
        "positive": 0.6
    },
    "vader": {
        "very_negative": -0.5,
        "negative": -0.1,
        "neutral": 0.1,
        "positive": 0.5
    }
}

# Configuración de groserías
PROFANITY_REPLACEMENTS = {
    "puta": "persona",
    "mierda": "problema",
    "cabrón": "persona",
    "gilipollas": "persona",
    "hijo de puta": "persona",
    "coño": "expresión",
    "joder": "expresión",
    "follar": "expresión",
    "polla": "expresión",
    "pene": "expresión",
    "vagina": "expresión",
    "teta": "expresión",
    "culo": "expresión",
    "pendejo": "persona",
    "pendeja": "persona",
    "güey": "amigo",
    "wey": "amigo",
    "guey": "amigo",
    "carajo": "expresión",
    "verga": "expresión",
    "chingar": "expresión",
    "pinche": "expresión",
    "chingada": "expresión"
}

# Configuración de sugerencias
SUGGESTION_TEMPLATES = {
    "negative_emotion": [
        "Considera usar palabras más positivas y constructivas",
        "Evita términos que puedan generar emociones negativas",
        "Enfócate en soluciones en lugar de problemas",
        "Usa un tono más optimista y motivador"
    ],
    "profanity": [
        "Reemplaza las groserías con palabras más apropiadas",
        "Usa un lenguaje más profesional y respetuoso",
        "Considera el impacto de tus palabras en diferentes audiencias",
        "Mantén un tono respetuoso y constructivo"
    ],
    "length": [
        "El texto es muy largo, considera dividirlo en partes",
        "Mantén tu mensaje conciso y directo",
        "Considera usar hilos para textos extensos"
    ],
    "positive": [
        "Tu texto está bien escrito y es apropiado para redes sociales",
        "Excelente tono y contenido para compartir",
        "Mantén este nivel de calidad en tus publicaciones"
    ]
}

# Configuración de CORS
CORS_ORIGINS = ["*"]
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Configuración de análisis de sentimientos
SENTIMENT_ANALYSIS_CONFIG = {
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
} 