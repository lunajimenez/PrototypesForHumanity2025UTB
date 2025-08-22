from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import torch
from transformers import pipeline
from spanlp.palabrotas import Palabrotas
from spanlp.normalizer import Normalizer
import re

# Configuración de la API
app = FastAPI(
    title="API de Validación de Textos para Redes Sociales",
    description="API que valida textos para detectar emociones negativas y groserías antes de publicar en redes sociales",
    version="1.0.0"
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

# Inicializar modelos
print("Cargando modelos...")

# Modelo de análisis de sentimientos en español
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment",
    device=0 if torch.cuda.is_available() else -1
)

# Inicializar spanlp para detección de groserías
profanity_detector = Palabrotas()
normalizer = Normalizer()

print("Modelos cargados exitosamente!")

def analyze_emotion(text: str) -> Dict[str, Any]:
    """Analiza la emoción del texto usando transformers"""
    try:
        # Normalizar el texto
        normalized_text = normalizer.normalize(text)
        
        # Analizar sentimiento
        result = sentiment_analyzer(normalized_text[:512])  # Limitar longitud para el modelo
        
        # Convertir puntuación de 1-5 a 0-1
        score = float(result[0]['label'].split()[0]) / 5.0
        
        # Determinar etiqueta de emoción
        if score <= 0.2:
            emotion_label = "Muy Negativo"
        elif score <= 0.4:
            emotion_label = "Negativo"
        elif score <= 0.6:
            emotion_label = "Neutral"
        elif score <= 0.8:
            emotion_label = "Positivo"
        else:
            emotion_label = "Muy Positivo"
        
        return {
            "score": score,
            "label": emotion_label,
            "confidence": result[0]['score']
        }
    except Exception as e:
        print(f"Error en análisis de emoción: {e}")
        return {
            "score": 0.5,
            "label": "Neutral",
            "confidence": 0.0
        }

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

def generate_suggestions(text: str, emotion_score: float, profanity_count: int) -> List[str]:
    """Genera sugerencias para mejorar el texto"""
    suggestions = []
    
    # Sugerencias basadas en emociones negativas
    if emotion_score < 0.4:
        suggestions.append("Considera usar palabras más positivas y constructivas")
        suggestions.append("Evita términos que puedan generar emociones negativas")
        suggestions.append("Enfócate en soluciones en lugar de problemas")
    
    # Sugerencias basadas en groserías
    if profanity_count > 0:
        suggestions.append("Reemplaza las groserías con palabras más apropiadas")
        suggestions.append("Usa un lenguaje más profesional y respetuoso")
        suggestions.append("Considera el impacto de tus palabras en diferentes audiencias")
    
    # Sugerencias generales
    if len(text) > 280:  # Límite de Twitter
        suggestions.append("El texto es muy largo, considera dividirlo en partes")
    
    if not suggestions:
        suggestions.append("Tu texto está bien escrito y es apropiado para redes sociales")
    
    return suggestions

def correct_text(text: str, profanity_words: List[str]) -> str:
    """Corrige el texto reemplazando groserías"""
    corrected_text = text
    
    # Diccionario de reemplazos para groserías comunes
    replacements = {
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
        "guey": "amigo"
    }
    
    # Aplicar reemplazos
    for profanity in profanity_words:
        if profanity.lower() in replacements:
            corrected_text = re.sub(
                re.escape(profanity), 
                replacements[profanity.lower()], 
                corrected_text, 
                flags=re.IGNORECASE
            )
    
    return corrected_text

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "API de Validación de Textos para Redes Sociales",
        "version": "1.0.0",
        "endpoints": {
            "/validate": "POST - Valida un texto",
            "/health": "GET - Estado de salud de la API"
        }
    }

@app.get("/health")
async def health_check():
    """Verifica el estado de salud de la API"""
    return {
        "status": "healthy",
        "models_loaded": True,
        "gpu_available": torch.cuda.is_available()
    }

@app.post("/validate", response_model=TextResponse)
async def validate_text(request: TextRequest):
    """Valida un texto para detectar emociones negativas y groserías"""
    try:
        # Validar entrada
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="El texto no puede estar vacío")
        
        if len(request.text) > 1000:
            raise HTTPException(status_code=400, detail="El texto es demasiado largo (máximo 1000 caracteres)")
        
        # Analizar emoción
        emotion_result = analyze_emotion(request.text)
        
        # Detectar groserías
        profanity_result = detect_profanity(request.text)
        
        # Determinar si es ofensivo en general
        is_offensive = emotion_result["score"] < 0.4 or profanity_result["has_profanity"]
        
        # Generar sugerencias
        suggestions = generate_suggestions(
            request.text, 
            emotion_result["score"], 
            profanity_result["profanity_count"]
        )
        
        # Corregir texto
        corrected_text = correct_text(request.text, profanity_result["profanity_words"])
        
        # Calcular confianza general
        confidence = (emotion_result["confidence"] + (1.0 - profanity_result["profanity_count"] * 0.1)) / 2
        confidence = max(0.0, min(1.0, confidence))
        
        return TextResponse(
            original_text=request.text,
            is_offensive=is_offensive,
            has_profanity=profanity_result["has_profanity"],
            emotion_score=emotion_result["score"],
            emotion_label=emotion_result["label"],
            profanity_count=profanity_result["profanity_count"],
            suggestions=suggestions,
            corrected_text=corrected_text,
            confidence=confidence
        )
        
    except Exception as e:
        print(f"Error en validación: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 