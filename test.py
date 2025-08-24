from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country
from spanlp.domain.strategies import JaccardIndex

# Inicializamos API
app = FastAPI(
    title="API Anti-Ciberacoso",
    description="API para detectar contenido ofensivo y groserías en texto",
    version="1.1.0"
)

# Modelo de Sentimiento (BERT multilingüe)
sentiment_analyzer = pipeline(
    "sentiment-analysis", 
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

# Configuración de spanlp (detección de malas palabras)
jaccard = JaccardIndex(threshold=0.9, normalize=False, n_gram=1)
palabrota = Palabrota(
    censor_char="*", 
    countries=[Country.COLOMBIA], 
    distance_metric=jaccard
)

class Message(BaseModel):
    text: str

def is_offensive_sentiment(sentiment_result):
    """Determina si el sentimiento es ofensivo basado en el score"""
    label = sentiment_result[0]['label']
    score = sentiment_result[0]['score']
    
    # Para el modelo nlptown, las etiquetas van de 1-5 estrellas
    # 1-2 estrellas = negativo/ofensivo, 4-5 = positivo, 3 = neutral
    if label in ['1 star', '2 stars'] and score > 0.7:
        return True
    return False

def extract_profanity_words(original_text, censored_text):
    """Extrae las palabras que fueron censuradas"""
    original_words = original_text.split()
    censored_words = censored_text.split()
    
    profanity_found = []
    
    for i, (orig, cens) in enumerate(zip(original_words, censored_words)):
        if orig != cens and '*' in cens:
            profanity_found.append(orig)
    
    return profanity_found

def generate_suggestions(profanity_words, is_offensive):
    """Genera sugerencias para mejorar el texto"""
    suggestions = []
    
    if profanity_words:
        suggestions.append(f"Se detectaron {len(profanity_words)} groserías. Considera usar un lenguaje más apropiado.")
        suggestions.append("Palabras detectadas: " + ", ".join(profanity_words))
    
    if is_offensive:
        suggestions.append("El tono del mensaje parece negativo u ofensivo. Intenta reformularlo de manera más constructiva.")
    
    if not profanity_words and not is_offensive:
        suggestions.append("El texto parece apropiado y no contiene contenido ofensivo.")
    
    return suggestions

# Ruta principal
@app.post("/analyze")
def analyze_message(message: Message):
    """Analiza un mensaje para detectar contenido ofensivo y groserías"""
    
    # Detectar y censurar malas palabras con fallback
    try:
        censored_text = palabrota.censor(message.text)
        profanity_words = extract_profanity_words(message.text, censored_text)
    except Exception as e:
        censored_text = message.text  # no censuramos si falla spanlp
        profanity_words = []
    
    has_profanity = len(profanity_words) > 0
    
    # Analizar sentimiento con BERT (siempre se ejecuta)
    sentiment_result = sentiment_analyzer(message.text[:512])  # límite de tokens
    is_offensive = is_offensive_sentiment(sentiment_result)
    
    # Generar sugerencias
    suggestions = generate_suggestions(profanity_words, is_offensive)
    
    # Resultado
    return {
        "original_text": message.text,
        "censored_text": censored_text,
        "is_offensive": is_offensive or has_profanity,
        "has_profanity": has_profanity,
        "profanity_words": profanity_words,
        "sentiment_analysis": {
            "label": sentiment_result[0]['label'],
            "confidence": round(sentiment_result[0]['score'], 3)
        },
        "suggestions": suggestions
    }

# Ruta de información
@app.get("/")
def root():
    return {
        "message": "API Anti-Ciberacoso activa",
        "usage": "Envía un POST a /analyze con {'text': 'tu mensaje'}"
    }

# Ruta de health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}
