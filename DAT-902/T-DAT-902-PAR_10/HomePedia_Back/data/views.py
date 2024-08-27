from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from firebase_admin import credentials, db

@api_view(['POST'])
@permission_classes([AllowAny])
def get_population_data(request):
    try:
        ref = db.reference('countries/country1/regions')
        regions = ref.get()

        if not regions:
            return JsonResponse({'error': 'No data found'}, status=404)

        # Collecting population data for each region
        population_data = []
        for region_id, region_data in regions.items():
            region_name = region_data.get('name')
            population = region_data.get('population')
            population_data.append({
                'region': region_name,
                'population': population
            })

        # Returning the population data
        return JsonResponse(population_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_communes_by_department(request):
    department_code = request.GET.get('department_code')

    if not department_code:
        return JsonResponse({"error": "Missing 'department_code' in request data"}, status=400)

    ref = db.reference(f'countries/country1/regions')
    regions = ref.get()

    department_communes = []
    for region_id, region_data in regions.items():
        for dept_id, dept_data in region_data["departments"].items():
            if dept_id == department_code:
                for commune_id, commune_data in dept_data["communes"].items():
                    commune_data["insee_com"] = commune_id
                    commune_data["code_dept"] = dept_id
                    commune_data["nom_dept"] = [dept_data["name"]]
                    # Use the exact name from the Firebase data
                    commune_data["nom_region"] = [region_data["name"]]
                    department_communes.append(commune_data)
                break

    if not department_communes:
        return JsonResponse({"error": "Department not found"}, status=404)

    return JsonResponse(department_communes, safe=False)
