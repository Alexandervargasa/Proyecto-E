from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
from dotenv import load_dotenv
import os, json
from productos.models import Producto
# 🔹 Cargar variables del archivo .env
load_dotenv()

# 🔹 Configurar la API con la clave del .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            from productos.models import Producto

            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"reply": "⚠️ No se recibió ningún mensaje."})

            # Obtener productos
            productos = Producto.objects.all()
            # 🔹 Obtener productos
            productos = Producto.objects.all()

            catalogo = "\n".join([
                f"- {p.nombre or 'No tiene especificado'} | "
                f"{p.descripcion or 'No tiene especificado'} | "
                f"Precio: ${p.precio if p.precio else 'No tiene especificado'} | "
                f"Stock: {p.stock if p.stock else 'No tiene especificado'} | "
                f"Categoría: {p.categoria or 'No tiene especificado'} | "
                f"Marca: {p.marca or 'No tiene especificado'}"
                for p in productos
            ])

            # Prompt mejorado y más breve
            prompt = f"""
Eres un asistente de compras amable y directo. 
Responde solo a lo que te pregunten con respuestas cortas (máx. 2 líneas) 
y puedes sugerir productos del catálogo si es relevante.

Catálogo disponible:
{catalogo}

Usuario: {user_message}
Respuesta:
"""

            model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
            response = model.generate_content(prompt)

            return JsonResponse({"reply": response.text.strip()})

        except Exception as e:
            return JsonResponse({"reply": f"⚠️ Error al conectar con la IA: {str(e)}"})

    elif request.method == "GET":
        return render(request, "ia/chat.html")

    return JsonResponse({"error": "Método no permitido"}, status=405)