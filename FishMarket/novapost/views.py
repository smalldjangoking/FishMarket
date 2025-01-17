from django.db.models import Q
from django.http import JsonResponse
from novapost.models import Warehouses, Cities


def get_city(request):
    if request.method == 'POST':
        city_name = request.POST.get('city', None)

        if not city_name:
            return JsonResponse({'success': False})

        city_objects = Cities.objects.filter(Q(city_name_ua__icontains=city_name.lower()) |
                                             Q(city_name_ru__icontains=city_name.lower())).values(
            'city_name_ua', 'city_state', 'ref_to_warehouses').order_by('city_state')

        if city_objects.exists():
            return JsonResponse({'success': True, 'data_array': list(city_objects)})
        else:
            return JsonResponse({'success': False})


def get_warehouses(request):
    if request.method == 'POST':
        city_id = request.POST.get('city_ref', None)
        type_of_ware = request.POST.get('typeofware', None)
        search_ware = request.POST.get('search_ware', None)

        if not search_ware:
            warehouses = Warehouses.objects.filter(city_id__exact=city_id,
                                                   typeofwarehouse__exact=type_of_ware).order_by('number')[
                         :15].values('address_ua', 'number', 'id')
            if warehouses.exists():
                return JsonResponse({'success': True, 'data_array': list(warehouses)})
            else:
                return JsonResponse({'success': False})
        else:
            if search_ware.isnumeric():
                warehouses = Warehouses.objects.filter(
                    Q(city_id__exact=city_id) &
                    Q(typeofwarehouse__exact=type_of_ware) &
                    Q(number__exact=search_ware)
                ).values('address_ua', 'number', 'id')

                if warehouses.exists():
                    return JsonResponse({'success': True, 'data_array': list(warehouses)})
                else:
                    return JsonResponse({'success': False})
            else:
                warehouses = Warehouses.objects.filter(
                    Q(city_id__exact=city_id) &
                    Q(typeofwarehouse__exact=type_of_ware) &
                    (Q(address_ru__icontains=search_ware.lower()) | Q(address_ua__icontains=search_ware.lower()))
                ).order_by('number').values('address_ua', 'number', 'id')
                if warehouses.exists():
                    print(len(list(warehouses)))
                    return JsonResponse({'success': True, 'data_array': list(warehouses)})
                else:
                    return JsonResponse({'success': False})
