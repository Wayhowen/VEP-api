from django.urls import reverse
from django.utils.dateparse import parse_datetime


def check_sent_data(sent_data, response, method):
    for key, value in sent_data.items():
        if key == 'assigned_practitioner_id':
            method(response.data['assigned_practitioner'], value)
        # Needed for comparing the datetime objects
        elif "datetime" in key:
            saved_datetime = parse_datetime(response.data[key]).replace(microsecond=0, tzinfo=None)
            value = value.replace(microsecond=0)
            method(saved_datetime, value)
        else:
            method(response.data[key], value)


def login(email, password, client):
    data = {"email": email, "password": password}
    response = client.post(reverse('login'), data)
