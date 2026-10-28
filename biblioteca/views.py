# LIBRERIAS
import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from .models import Libro


def leer_json(request):
    """Convierte el body en diccionario; devuelve None si no es JSON válido."""
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None


# VISTA
@method_decorator(csrf_exempt, name='dispatch')
class LibroView(View):

    def get(self, request, pk=None):
        if pk is None:
            libros = [model_to_dict(l) for l in Libro.objects.all()]
            return JsonResponse({'libros': libros})
        libro = get_object_or_404(Libro, pk=pk)
        return JsonResponse(model_to_dict(libro))

    def post(self, request):
        datos = leer_json(request)
        if not datos or 'titulo' not in datos or 'autor' not in datos:
            return JsonResponse({'error': 'Faltan titulo y autor'}, status=400)
        libro = Libro.objects.create(
            titulo=datos['titulo'],
            autor=datos['autor'],
            anio=datos.get('anio'),
        )
        return JsonResponse(model_to_dict(libro), status=201)

    def put(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        datos = leer_json(request)
        if datos is None:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
        libro.titulo = datos.get('titulo', libro.titulo)
        libro.autor = datos.get('autor', libro.autor)
        libro.anio = datos.get('anio', libro.anio)
        libro.disponible = datos.get('disponible', libro.disponible)
        libro.save()
        return JsonResponse(model_to_dict(libro))

    def delete(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        libro.delete()
        return JsonResponse({'mensaje': 'Libro eliminado'}, status=200)