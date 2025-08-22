from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import torch
from transformers import pipeline
from spanlp.palabrotas import Palabrotas
from spanlp.normalizer import Normalizer
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import time
from config import SENTIMENT_MODELS, DEFAULT_SENTIMENT_METHOD, SENTIMENT_ANALYSIS_CONFIG
from utils import (
    get_emotion_label, generate_suggestions, correct_text, 
    calculate_confidence, validate_input, get_method_info, compare_methods
)

# Configuración de la API
app = FastAPI(
    title="API de Validación de Textos para Redes Sociales",
    description="API que valida textos para detectar emociones negativas y groserías antes de publicar en redes sociales. Integra múltiples métodos de análisis: Transformers (BERT), TextBlob y VADER.",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class TextRequest(BaseModel):
    text: str
    language: str = "es"
    sentiment_method: Optional[str] = DEFAULT_SENTIMENT_METHOD

class TextResponse(BaseModel):
    original_text: str
    is_offensive: bool
    has_profanity: bool
    emotion_score: float
    emotion_label: str
    profanity_count: int
    suggestions: List[str]
    corrected_text: str
    confidence: float
    sentiment_method: str
    method_info: Dict[str, Any]
    processing_time: float

class MethodComparisonResponse(BaseModel):
    methods: Dict[str, Any]
    recommended: str

# Inicializar modelos
print("Cargando modelos de análisis de sentimientos...")

# Modelo de análisis de sentimientos en español (Opción 2 del proyecto)
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model=SENTIMENT_MODELS["transformers"],
    device=0 if torch.cuda.is_available() else -1
)

# Inicializar spanlp para detección de groserías
profanity_detector = Palabrotas()
normalizer = Normalizer()

# Inicializar VADER para análisis rápido
vader_analyzer = SentimentIntensityAnalyzer()

print("Modelos cargados exitosamente!")

def analyze_emotion_transformers(text: str) -> Dict[str, Any]:
    """Analiza la emoción del texto usando transformers (Opción 2 del proyecto)"""
    try:
        # Normalizar el texto
        normalized_text = normalizer.normalize(text)
        
        # Analizar sentimiento
        result = sentiment_analyzer(normalized_text[:512])  # Limitar longitud para el modelo
        
        # Convertir puntuación de 1-5 a 0-1
        score = float(result[0]['label'].split()[0]) / 5.0
        
        return {
            "score": score,
            "label": get_emotion_label(score, "transformers"),
            "confidence": result[0]['score'],
            "method": "transformers"
        }
    except Exception as e:
        print(f"Error en análisis de emoción con transformers: {e}")
        return {
            "score": 0.5,
            "label": "Neutral",
            "confidence": 0.0,
            "method": "transformers"
        }

def analyze_emotion_textblob(text: str) -> Dict[str, Any]:
    """Analiza la emoción del texto usando TextBlob"""
    try:
        # Crear objeto TextBlob
        blob = TextBlob(text)
        
        # Obtener polaridad (-1 a 1) y subjetividad (0 a 1)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        return {
            "score": polarity,
            "label": get_emotion_label(polarity, "textblob"),
            "confidence": abs(polarity) + (1 - subjectivity) / 2,  # Combinar polaridad y subjetividad
            "method": "textblob",
            "subjectivity": subjectivity
        }
    except Exception as e:
        print(f"Error en análisis de emoción con TextBlob: {e}")
        return {
            "score": 0.0,
            "label": "Neutral",
            "confidence": 0.0,
            "method": "textblob"
        }

def analyze_emotion_vader(text: str) -> Dict[str, Any]:
    """Analiza la emoción del texto usando VADER"""
    try:
        # Analizar sentimiento con VADER
        scores = vader_analyzer.polarity_scores(text)
        
        # Obtener score compuesto (-1 a 1)
        compound_score = scores['compound']
        
        return {
            "score": compound_score,
            "label": get_emotion_label(compound_score, "vader"),
            "confidence": abs(compound_score),
            "method": "vader",
            "detailed_scores": scores
        }
    except Exception as e:
        print(f"Error en análisis de emoción con VADER: {e}")
        return {
            "score": 0.0,
            "label": "Neutral",
            "confidence": 0.0,
            "method": "vader"
        }

def analyze_emotion(text: str, method: str = DEFAULT_SENTIMENT_METHOD) -> Dict[str, Any]:
    """Analiza la emoción del texto usando el método especificado"""
    if method == "transformers":
        return analyze_emotion_transformers(text)
    elif method == "textblob":
        return analyze_emotion_textblob(text)
    elif method == "vader":
        return analyze_emotion_vader(text)
    else:
        print(f"Método '{method}' no reconocido, usando transformers por defecto")
        return analyze_emotion_transformers(text)

def detect_profanity(text: str) -> Dict[str, Any]:
    """Detecta groserías usando spanlp"""
    try:
        # Normalizar el texto
        normalized_text = normalizer.normalize(text)
        
        # Detectar groserías
        profanity_words = profanity_detector.palabrotas(normalized_text)
        
        # Contar groserías
        profanity_count = len(profanity_words)
        
        # Determinar si es ofensivo
        is_offensive = profanity_count > 0
        
        return {
            "has_profanity": is_offensive,
            "profanity_count": profanity_count,
            "profanity_words": profanity_words
        }
    except Exception as e:
        print(f"Error en detección de groserías: {e}")
        return {
            "has_profanity": False,
            "profanity_count": 0,
            "profanity_words": []
        }

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "API de Validación de Textos para Redes Sociales v2.0",
        "version": "2.0.0",
        "description": "Integra múltiples métodos de análisis de sentimientos: Transformers (BERT), TextBlob y VADER",
        "endpoints": {
            "/validate": "POST - Valida un texto",
            "/health": "GET - Estado de salud de la API",
            "/methods": "GET - Información sobre métodos de análisis",
            "/compare": "GET - Comparación de métodos"
        },
        "default_method": DEFAULT_SENTIMENT_METHOD,
        "available_methods": list(SENTIMENT_MODELS.keys())
    }

@app.get("/health")
async def health_check():
    """Verifica el estado de salud de la API"""
    return {
        "status": "healthy",
        "models_loaded": True,
        "gpu_available": torch.cuda.is_available(),
        "available_methods": list(SENTIMENT_MODELS.keys()),
        "default_method": DEFAULT_SENTIMENT_METHOD
    }

@app.get("/methods")
async def get_methods():
    """Obtiene información sobre los métodos de análisis disponibles"""
    return {
        "available_methods": SENTIMENT_ANALYSIS_CONFIG,
        "default_method": DEFAULT_SENTIMENT_METHOD,
        "recommendations": {
            "transformers": "Para análisis de alta precisión y multilingüe",
            "textblob": "Para análisis rápido y eficiente",
            "vader": "Para análisis en tiempo real y redes sociales"
        }
    }

@app.get("/compare")
async def compare_analysis_methods():
    """Compara los diferentes métodos de análisis de sentimientos"""
    return MethodComparisonResponse(
        methods=compare_methods(),
        recommended=DEFAULT_SENTIMENT_METHOD
    )

@app.post("/validate", response_model=TextResponse)
async def validate_text(request: TextRequest):
    """Valida un texto para detectar emociones negativas y groserías"""
    start_time = time.time()
    
    try:
        # Validar entrada
        validation_result = validate_input(request.text)
        if not validation_result["is_valid"]:
            raise HTTPException(status_code=400, detail=validation_result["errors"][0])
        
        # Validar método de análisis
        if request.sentiment_method not in SENTIMENT_MODELS:
            raise HTTPException(
                status_code=400, 
                detail=f"Método '{request.sentiment_method}' no válido. Métodos disponibles: {list(SENTIMENT_MODELS.keys())}"
            )
        
        # Analizar emoción
        emotion_result = analyze_emotion(request.text, request.sentiment_method)
        
        # Detectar groserías
        profanity_result = detect_profanity(request.text)
        
        # Determinar si es ofensivo en general
        is_offensive = emotion_result["score"] < 0.4 or profanity_result["has_profanity"]
        
        # Generar sugerencias
        suggestions = generate_suggestions(
            request.text, 
            emotion_result["score"], 
            profanity_result["profanity_count"],
            request.sentiment_method
        )
        
        # Corregir texto
        corrected_text = correct_text(request.text, profanity_result["profanity_words"])
        
        # Calcular confianza general
        confidence = calculate_confidence(
            emotion_result["confidence"], 
            profanity_result["profanity_count"],
            request.sentiment_method
        )
        
        # Obtener información del método
        method_info = get_method_info(request.sentiment_method)
        
        # Calcular tiempo de procesamiento
        processing_time = time.time() - start_time
        
        return TextResponse(
            original_text=request.text,
            is_offensive=is_offensive,
            has_profanity=profanity_result["has_profanity"],
            emotion_score=emotion_result["score"],
            emotion_label=emotion_result["label"],
            profanity_count=profanity_result["profanity_count"],
            suggestions=suggestions,
            corrected_text=corrected_text,
            confidence=confidence,
            sentiment_method=request.sentiment_method,
            method_info=method_info,
            processing_time=processing_time
        )
        
    except Exception as e:
        print(f"Error en validación: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

@app.post("/validate/batch")
async def validate_texts_batch(texts: List[str], method: str = Query(DEFAULT_SENTIMENT_METHOD)):
    """Valida múltiples textos en lote"""
    if not texts:
        raise HTTPException(status_code=400, detail="La lista de textos no puede estar vacía")
    
    if len(texts) > 50:
        raise HTTPException(status_code=400, detail="Máximo 50 textos por lote")
    
    results = []
    for text in texts:
        try:
            # Validar entrada
            validation_result = validate_input(text)
            if not validation_result["is_valid"]:
                results.append({
                    "text": text,
                    "error": validation_result["errors"][0],
                    "valid": False
                })
                continue
            
            # Analizar emoción
            emotion_result = analyze_emotion(text, method)
            
            # Detectar groserías
            profanity_result = detect_profanity(text)
            
            # Determinar si es ofensivo
            is_offensive = emotion_result["score"] < 0.4 or profanity_result["has_profanity"]
            
            results.append({
                "text": text,
                "is_offensive": is_offensive,
                "emotion_score": emotion_result["score"],
                "emotion_label": emotion_result["label"],
                "profanity_count": profanity_result["profanity_count"],
                "valid": True
            })
            
        except Exception as e:
            results.append({
                "text": text,
                "error": str(e),
                "valid": False
            })
    
    return {
        "method": method,
        "total_texts": len(texts),
        "valid_texts": len([r for r in results if r["valid"]]),
        "results": results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 