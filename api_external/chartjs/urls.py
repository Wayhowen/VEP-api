from django.urls import path

from chartjs import views

urlpatterns = [
    path('chart_data/<int:patient_id>', views.ChartData.as_view()),
    path('chart/<int:patient_id>', views.HomeView.as_view()),
]
