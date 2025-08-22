"""
Configuración de la API de Validación de Textos
"""

# Configuración del servidor
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000
DEBUG = True

# Configuración de modelos
SENTIMENT_MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
MAX_TEXT_LENGTH = 1000
EMOTION_THRESHOLDS = {
    "very_negative": 0.2,
    "negative": 0.4,
    "neutral": 0.6,
    "positive": 0.8
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