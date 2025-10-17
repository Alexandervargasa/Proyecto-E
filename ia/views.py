from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
from dotenv import load_dotenv
import os, json

# 🔹 Cargar variables del archivo .env
load_dotenv()

# 🔹 Configurar la API con la clave del .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@csrf_exempt  # (Temporal; luego puedes usar CSRF Token en fetch)
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"reply": "⚠️ No se recibió ningún mensaje."})

            model = genai.GenerativeModel("models/gemini-2.0-flash-exp")
            response = model.generate_content(user_message)

            return JsonResponse({"reply": response.text})

        except Exception as e:
            return JsonResponse({"reply": f"⚠️ Error al conectar con la IA: {str(e)}"})

    elif request.method == "GET":
        return render(request, "ia/chat.html")

    return JsonResponse({"error": "Método no permitido"}, status=405)
