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

            # 🔹 Obtener todos los productos de la base de datos
            productos = Producto.objects.all()
            
            if productos.exists():
                catalogo = "📦 **PRODUCTOS DISPONIBLES EN NUESTRA TIENDA:**\n\n"
                for p in productos:
                    catalogo += f"• **{p.nombre}**\n"
                    if p.descripcion:
                        catalogo += f"  📝 {p.descripcion}\n"
                    catalogo += f"  💰 Precio: ${p.precio:,.0f} COP\n"
                    catalogo += f"  📦 Stock: {p.stock} unidades\n"
                    if p.categoria:
                        catalogo += f"  🏷️ Categoría: {p.categoria}\n"
                    if p.marca:
                        catalogo += f"  🏭 Marca: {p.marca}\n"
                    catalogo += "\n"
            else:
                catalogo = "⚠️ Actualmente no hay productos registrados en la tienda."

            # Prompt mejorado para el chatbot
            prompt = f"""
Eres un asistente de ventas profesional y amigable de EmprendeApp. 
Tu trabajo es ayudar a los clientes a encontrar los productos perfectos para sus necesidades.

IMPORTANTE:
- Responde de forma clara, concisa y amigable (máximo 3-4 líneas por respuesta)
- Si te preguntan por productos, recomienda basándose SOLO en el catálogo real
- Si un producto no está en el catálogo, di que no lo tienes disponible
- Puedes recomendar productos según necesidades (ej: "para trabajar", "para el hogar", etc.)
- Sé específico con precios, marcas y características
- Usa emojis para hacer la conversación más amena

{catalogo}

Pregunta del cliente: {user_message}

Respuesta (máximo 3-4 líneas):
"""

            model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
            response = model.generate_content(prompt)

            return JsonResponse({"reply": response.text.strip()})

        except Exception as e:
            return JsonResponse({"reply": f"⚠️ Error al conectar con la IA: {str(e)}"})

    elif request.method == "GET":
        return render(request, "ia/chat.html")

    return JsonResponse({"error": "Método no permitido"}, status=405)