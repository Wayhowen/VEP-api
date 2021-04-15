# from django.http import JsonResponse
import random

from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response


MEMORY = [0, 10, 5, 2, 20, 30, 45]
MEMORY2 = list(reversed(MEMORY))


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'chartjs/index.html')


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, patient_id):
        print(patient_id)
        MEMORY.append(random.randint(0, 100))
        MEMORY2.append(random.randint(0, 100))
        chartdata = MEMORY
        anotherdata = MEMORY2
        labels = [no for no in range(0, len(chartdata))]
        data = {
            "labels": labels,
            "datasets": [
                {
                    "label": "Steps Number",
                    "data": chartdata,
                    "backgroundColor": 'rgba(255,100,200,0)',
                    'borderColor': 'rgba(255,3,3)'
                },
                {
                    "label": "Asymetry",
                    "data": anotherdata,
                    "backgroundColor": 'rgba(255,100,200,0)',
                    'borderColor':'rgba(255,251,3)',
                }
            ]
        }
        return Response(data)
