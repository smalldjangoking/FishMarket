from django.http import JsonResponse
from novapost.models import Warehouses, Cities


def get_city(request):
    if request.method == 'POST':
        city_name = request.POST.get('city', None)

        if not city_name:
            return JsonResponse({'success': False})

        city_objects = Cities.objects.filter(city_name=city_name)
        return JsonResponse(city_objects, safe=False)


def get_warehouses(request):
    if request.method == 'POST':
        city_id = request.POST.get('ref_to_warehouses', None)
        warehouses = Warehouses.objects.filter(city=city_id).values('name_ua')

        if city_id and warehouses.exits():
            return JsonResponse({'success': True, 'warehouses': warehouses})
