"""
Utilidades para el procesamiento y validación de textos
"""

import re
from typing import List, Dict, Any
from config import PROFANITY_REPLACEMENTS, SUGGESTION_TEMPLATES, EMOTION_THRESHOLDS

def clean_text(text: str) -> str:
    """Limpia y normaliza el texto"""
    # Eliminar espacios extra
    text = re.sub(r'\s+', ' ', text.strip())
    # Eliminar caracteres especiales problemáticos
    text = re.sub(r'[^\w\s\.,!?¿¡áéíóúüñÁÉÍÓÚÜÑ]', '', text)
    return text

def get_emotion_label(score: float) -> str:
    """Determina la etiqueta de emoción basada en el score"""
    if score <= EMOTION_THRESHOLDS["very_negative"]:
        return "Muy Negativo"
    elif score <= EMOTION_THRESHOLDS["negative"]:
        return "Negativo"
    elif score <= EMOTION_THRESHOLDS["neutral"]:
        return "Neutral"
    elif score <= EMOTION_THRESHOLDS["positive"]:
        return "Positivo"
    else:
        return "Muy Positivo"

def generate_suggestions(text: str, emotion_score: float, profanity_count: int) -> List[str]:
    """Genera sugerencias personalizadas para mejorar el texto"""
    suggestions = []
    
    # Sugerencias basadas en emociones negativas
    if emotion_score < EMOTION_THRESHOLDS["negative"]:
        suggestions.extend(SUGGESTION_TEMPLATES["negative_emotion"])
    
    # Sugerencias basadas en groserías
    if profanity_count > 0:
        suggestions.extend(SUGGESTION_TEMPLATES["profanity"])
    
    # Sugerencias basadas en longitud
    if len(text) > 280:  # Límite de Twitter
        suggestions.extend(SUGGESTION_TEMPLATES["length"])
    
    # Si no hay sugerencias específicas, dar feedback positivo
    if not suggestions:
        suggestions.extend(SUGGESTION_TEMPLATES["positive"])
    
    # Limitar a máximo 5 sugerencias
    return suggestions[:5]

def correct_text(text: str, profanity_words: List[str]) -> str:
    """Corrige el texto reemplazando groserías con alternativas apropiadas"""
    corrected_text = text
    
    for profanity in profanity_words:
        if profanity.lower() in PROFANITY_REPLACEMENTS:
            replacement = PROFANITY_REPLACEMENTS[profanity.lower()]
            corrected_text = re.sub(
                re.escape(profanity), 
                replacement, 
                corrected_text, 
                flags=re.IGNORECASE
            )
    
    return corrected_text

def calculate_confidence(emotion_confidence: float, profanity_count: int) -> float:
    """Calcula la confianza general del análisis"""
    # Reducir confianza por cada grosería detectada
    profanity_penalty = min(0.3, profanity_count * 0.1)
    
    # Calcular confianza final
    confidence = emotion_confidence - profanity_penalty
    
    # Asegurar que esté en el rango [0, 1]
    return max(0.0, min(1.0, confidence))

def validate_input(text: str, max_length: int = 1000) -> Dict[str, Any]:
    """Valida la entrada del usuario"""
    errors = []
    
    if not text or not text.strip():
        errors.append("El texto no puede estar vacío")
    
    if len(text) > max_length:
        errors.append(f"El texto es demasiado largo (máximo {max_length} caracteres)")
    
    # Verificar caracteres problemáticos
    if re.search(r'[<>{}[\]]', text):
        errors.append("El texto contiene caracteres no permitidos")
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

def format_response_time(seconds: float) -> str:
    """Formatea el tiempo de respuesta en formato legible"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    else:
        return f"{seconds:.2f}s" 