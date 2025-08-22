"""
Script de prueba para la API de Validación de Textos v2.0
Integra múltiples métodos de análisis: Transformers (BERT), TextBlob y VADER
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
            print(f"   Métodos disponibles: {response.json().get('available_methods', [])}")
            print(f"   Método por defecto: {response.json().get('default_method', 'N/A')}")
        else:
            print(f"❌ Error en health check: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_methods_info():
    """Prueba el endpoint de información de métodos"""
    print("\n📚 Probando información de métodos...")
    try:
        response = requests.get(f"{API_BASE_URL}/methods")
        if response.status_code == 200:
            data = response.json()
            print("✅ Información de métodos obtenida:")
            for method, info in data["available_methods"].items():
                print(f"   🔹 {method}: {info['description']}")
                print(f"      Ventajas: {', '.join(info['advantages'])}")
                print(f"      Desventajas: {', '.join(info['disadvantages'])}")
        else:
            print(f"❌ Error obteniendo métodos: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_method_comparison():
    """Prueba el endpoint de comparación de métodos"""
    print("\n⚖️ Probando comparación de métodos...")
    try:
        response = requests.get(f"{API_BASE_URL}/compare")
        if response.status_code == 200:
            data = response.json()
            print("✅ Comparación de métodos obtenida:")
            print(f"   Método recomendado: {data['recommended']}")
            for method, info in data['methods'].items():
                print(f"   🔹 {method}: {info['recommended_for']}")
        else:
            print(f"❌ Error obteniendo comparación: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_text_validation_with_method(text, description, method="transformers"):
    """Prueba la validación de un texto específico con un método determinado"""
    print(f"\n📝 Probando: {description}")
    print(f"   Texto: '{text}'")
    print(f"   Método: {method}")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}/validate",
            json={"text": text, "language": "es", "sentiment_method": method}
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Validación exitosa ({end_time - start_time:.2f}s)")
            print(f"   Es ofensivo: {result['is_offensive']}")
            print(f"   Tiene groserías: {result['has_profanity']}")
            print(f"   Score de emoción: {result['emotion_score']:.3f} ({result['emotion_label']})")
            print(f"   Número de groserías: {result['profanity_count']}")
            print(f"   Confianza: {result['confidence']:.3f}")
            print(f"   Método usado: {result['sentiment_method']}")
            print(f"   Tiempo de procesamiento: {result['processing_time']:.3f}s")
            print(f"   Texto corregido: '{result['corrected_text']}'")
            print("   Sugerencias:")
            for i, suggestion in enumerate(result['suggestions'], 1):
                print(f"     {i}. {suggestion}")
        else:
            print(f"❌ Error en validación: {response.status_code}")
            print(f"   Detalle: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def test_all_methods_with_same_text(text, description):
    """Prueba todos los métodos de análisis con el mismo texto"""
    print(f"\n🧪 Probando todos los métodos con: '{description}'")
    
    methods = ["transformers", "textblob", "vader"]
    results = {}
    
    for method in methods:
        try:
            response = requests.post(
                f"{API_BASE_URL}/validate",
                json={"text": text, "language": "es", "sentiment_method": method}
            )
            
            if response.status_code == 200:
                result = response.json()
                results[method] = {
                    "score": result['emotion_score'],
                    "label": result['emotion_label'],
                    "confidence": result['confidence'],
                    "processing_time": result['processing_time']
                }
            else:
                results[method] = {"error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            results[method] = {"error": str(e)}
    
    # Mostrar comparación
    print("   📊 Comparación de métodos:")
    for method, result in results.items():
        if "error" in result:
            print(f"     ❌ {method}: {result['error']}")
        else:
            print(f"     ✅ {method}: Score={result['score']:.3f}, Label={result['label']}, Conf={result['confidence']:.3f}, Time={result['processing_time']:.3f}s")

def test_batch_validation():
    """Prueba la validación en lote"""
    print("\n📦 Probando validación en lote...")
    
    texts = [
        "Excelente trabajo equipo!",
        "Me siento frustrado con los resultados",
        "Este es un proyecto increíble",
        "No puedo creer lo mal que está esto"
    ]
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/validate/batch",
            params={"method": "transformers"},
            json=texts
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Procesados {result['total_texts']} textos con método {result['method']}")
            print(f"   Textos válidos: {result['valid_texts']}")
            
            for i, text_result in enumerate(result['results']):
                if text_result['valid']:
                    status = "🟢" if not text_result['is_offensive'] else "🔴"
                    print(f"   {status} Texto {i+1}: Score={text_result['emotion_score']:.3f}, Groserías={text_result['profanity_count']}")
                else:
                    print(f"   ❌ Texto {i+1}: {text_result['error']}")
        else:
            print(f"❌ Error en validación por lotes: {response.status_code}")
            print(f"   Detalle: {response.text}")
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas de la API de Validación de Textos v2.0\n")
    
    # Prueba de salud
    test_health_check()
    
    # Información de métodos
    test_methods_info()
    
    # Comparación de métodos
    test_method_comparison()
    
    # Casos de prueba con diferentes métodos
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
    
    print(f"\n🧪 Ejecutando {len(test_cases)} casos de prueba con método por defecto...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Prueba {i}/{len(test_cases)} ---")
        test_text_validation_with_method(test_case["text"], test_case["description"])
        time.sleep(1)  # Pausa entre pruebas
    
    # Prueba de comparación de métodos
    print(f"\n🔬 Probando comparación de métodos...")
    test_all_methods_with_same_text(
        "Este producto es increíble, me encanta mucho!",
        "Texto positivo para comparar métodos"
    )
    
    test_all_methods_with_same_text(
        "Estoy muy decepcionado con la calidad del servicio",
        "Texto negativo para comparar métodos"
    )
    
    # Prueba de validación en lote
    test_batch_validation()
    
    print("\n🎉 Todas las pruebas completadas!")

def test_performance_comparison():
    """Prueba de rendimiento comparando métodos"""
    print("\n⚡ Prueba de rendimiento comparando métodos...")
    
    test_text = "Este es un texto de prueba para medir el rendimiento de diferentes métodos de análisis de sentimientos."
    
    methods = ["transformers", "textblob", "vader"]
    performance_results = {}
    
    for method in methods:
        print(f"\n   🔍 Probando método: {method}")
        times = []
        
        # Ejecutar 5 veces para obtener promedio
        for i in range(5):
            try:
                start_time = time.time()
                response = requests.post(
                    f"{API_BASE_URL}/validate",
                    json={"text": test_text, "language": "es", "sentiment_method": method}
                )
                end_time = time.time()
                
                if response.status_code == 200:
                    processing_time = response.json().get('processing_time', end_time - start_time)
                    times.append(processing_time)
                    print(f"     Ejecución {i+1}: {processing_time:.3f}s")
                else:
                    print(f"     ❌ Error en ejecución {i+1}")
                    
            except Exception as e:
                print(f"     ❌ Error en ejecución {i+1}: {e}")
        
        if times:
            avg_time = sum(times) / len(times)
            performance_results[method] = avg_time
            print(f"     ⏱️  Tiempo promedio: {avg_time:.3f}s")
    
    # Mostrar resumen de rendimiento
    print(f"\n📊 Resumen de rendimiento:")
    sorted_methods = sorted(performance_results.items(), key=lambda x: x[1])
    for i, (method, time) in enumerate(sorted_methods):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
        print(f"   {medal} {method}: {time:.3f}s promedio")

if __name__ == "__main__":
    print("=" * 70)
    print("🧪 TESTER DE API DE VALIDACIÓN DE TEXTOS v2.0")
    print("🚀 Integra: Transformers (BERT), TextBlob y VADER")
    print("=" * 70)
    
    try:
        run_all_tests()
        test_performance_comparison()
    except KeyboardInterrupt:
        print("\n⏹️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n💥 Error general: {e}")
    
    print("\n" + "=" * 70)
    print("🏁 Fin de las pruebas")
    print("=" * 70) 