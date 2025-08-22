"""
Script de prueba para la API de Validación de Textos
"""

import requests
import json
import time

# Configuración
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Prueba el endpoint de salud"""
    print("🔍 Probando endpoint de salud...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API está funcionando correctamente")
            print(f"   GPU disponible: {response.json().get('gpu_available', False)}")
        else:
            print(f"❌ Error en health check: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_text_validation(text, description):
    """Prueba la validación de un texto específico"""
    print(f"\n📝 Probando: {description}")
    print(f"   Texto: '{text}'")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}/validate",
            json={"text": text, "language": "es"}
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Validación exitosa ({end_time - start_time:.2f}s)")
            print(f"   Es ofensivo: {result['is_offensive']}")
            print(f"   Tiene groserías: {result['has_profanity']}")
            print(f"   Score de emoción: {result['emotion_score']:.2f} ({result['emotion_label']})")
            print(f"   Número de groserías: {result['profanity_count']}")
            print(f"   Confianza: {result['confidence']:.2f}")
            print(f"   Texto corregido: '{result['corrected_text']}'")
            print("   Sugerencias:")
            for i, suggestion in enumerate(result['suggestions'], 1):
                print(f"     {i}. {suggestion}")
        else:
            print(f"❌ Error en validación: {response.status_code}")
            print(f"   Detalle: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas de la API de Validación de Textos\n")
    
    # Prueba de salud
    test_health_check()
    
    # Casos de prueba
    test_cases = [
        {
            "text": "Hola, me encanta este proyecto! Es muy interesante y útil.",
            "description": "Texto positivo y apropiado"
        },
        {
            "text": "Este producto es una mierda, no funciona nada bien.",
            "description": "Texto con grosería y emoción negativa"
        },
        {
            "text": "Estoy muy enojado con el servicio al cliente, son unos incompetentes.",
            "description": "Texto con emoción negativa pero sin groserías"
        },
        {
            "text": "¡Qué día tan maravilloso! El sol brilla y todo está perfecto.",
            "description": "Texto muy positivo"
        },
        {
            "text": "Este código está mal hecho, el desarrollador es un gilipollas.",
            "description": "Texto con grosería y crítica negativa"
        },
        {
            "text": "Necesito ayuda con mi proyecto, ¿alguien puede ayudarme?",
            "description": "Texto neutral solicitando ayuda"
        }
    ]
    
    print(f"\n🧪 Ejecutando {len(test_cases)} casos de prueba...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Prueba {i}/{len(test_cases)} ---")
        test_text_validation(test_case["text"], test_case["description"])
        time.sleep(1)  # Pausa entre pruebas
    
    print("\n🎉 Todas las pruebas completadas!")

def test_batch_validation():
    """Prueba la validación de múltiples textos en lote"""
    print("\n📦 Probando validación en lote...")
    
    texts = [
        "Excelente trabajo equipo!",
        "Me siento frustrado con los resultados",
        "Este es un proyecto increíble",
        "No puedo creer lo mal que está esto"
    ]
    
    results = []
    for text in texts:
        try:
            response = requests.post(
                f"{API_BASE_URL}/validate",
                json={"text": text, "language": "es"}
            )
            if response.status_code == 200:
                result = response.json()
                results.append({
                    "text": text,
                    "is_offensive": result["is_offensive"],
                    "emotion_score": result["emotion_score"],
                    "has_profanity": result["has_profanity"]
                })
        except Exception as e:
            print(f"Error procesando: {text} - {e}")
    
    print(f"✅ Procesados {len(results)} textos:")
    for result in results:
        status = "🟢" if not result["is_offensive"] else "🔴"
        print(f"   {status} '{result['text'][:50]}...' - Score: {result['emotion_score']:.2f}")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTER DE API DE VALIDACIÓN DE TEXTOS")
    print("=" * 60)
    
    try:
        run_all_tests()
        test_batch_validation()
    except KeyboardInterrupt:
        print("\n⏹️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n💥 Error general: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 Fin de las pruebas")
    print("=" * 60) 