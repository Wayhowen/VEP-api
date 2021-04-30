from django.shortcuts import render
from django.views.generic import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from persistence.models import Patient


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'chartjs/index.html')


COLOURS = {
    "transparent": 'rgba(255,100,200,0)',
    "line": [
        'rgb(220,10,10)',
        'rgb(220,192,10)',
        'rgb(49,220,10)',
        'rgb(10,220,188)',
        'rgb(10,70,220)',
        'rgb(110,50,194)',
        'rgb(205,21,239)',
        'rgb(208,118,18)',
        'rgb(16,0,0)',
        'rgb(87,66,60)',
        'rgb(127,116,116)',
        'rgb(111,1,1)'
    ]
}

"""
"red"
"yellow"
"green"
"turquoise"
"blue"
"purple"
"pink"
"orange"
"black"
"brown"
"gray"
"dark_red"
"""


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(responses={200: "Aggregated graph data"},
                         tags=["Graphs"], operation_description="Internal endpoint for returning "
                                                                "graphical data to the JS "
                                                                "visualizer")
    def get(self, request, patient_id):
        label_template = "training no. _"
        labels = []
        datasets = []
        last_used_colour = -1

        patient = Patient.objects.prefetch_related("activity_results")\
            .order_by("activity_results__id").get(id=patient_id)
        for index, ac in enumerate(patient.activity_results.all()):
            if ac.preprocessing_result:
                if "error" not in ac.preprocessing_result:
                    labels.append(label_template.replace("_", str(index)))
                    for key, value in ac.preprocessing_result.items():
                        li = find_label_index(key, datasets)
                        if li is not None:
                            datasets[li]["data"].append(value)
                        else:
                            last_used_colour += 1
                            line = {
                                "label": key,
                                "data": [value],
                                "backgroundColor": COLOURS["transparent"],
                                "borderColor": COLOURS["line"][last_used_colour]
                            }
                            datasets.append(line)
        data = {
            "labels": labels,
            "datasets": datasets
        }
        return Response(data)


def find_label_index(label, datasets):
    for index, line in enumerate(datasets):
        if label == line["label"]:
            return index
    return None
