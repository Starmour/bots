import json
import os

import requests


def log_in():
    url = "https://api.air.fail/auth/login"
    login = "s.tar.my@yandex.ru"
    password = "Incredible.099256"
    headers = {"Content-Type": "application/json"}
    data = {"email": login, "password": password}
    response = requests.post(url, json=data, headers=headers)

    with open('json/log_in_response.json', 'w') as outfile:
        json.dump(response.json(), outfile, indent=4)


def authorization():
    url = "https://api.air.fail/auth/me"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjcxODYyLCJpYXQiOjE3Mjk2Nzk4NjIsImp0aSI6IjQ0M2I2ODA3ZWRlYTQ3NDU5YzkwZDkyZTM1MjM5ODViIiwidWlkIjoiMDI3Yzk4YjktY2Y1NS00ZWIxLWI4ODAtZWJmZWFlMzQzZDc5In0.XYUEbOXhs1p289MGIIaXAc9RSc3Q1d5hYcYkIj9OfKg"}
    response = requests.get(url, headers=headers)
    with open('json/authorization_response.json', 'w') as outfile:
        json.dump(response.json(), outfile, indent=4)


def get_api_key():
    url = 'https://api.air.fail/public/api-key'
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjcxODYyLCJpYXQiOjE3Mjk2Nzk4NjIsImp0aSI6IjQ0M2I2ODA3ZWRlYTQ3NDU5YzkwZDkyZTM1MjM5ODViIiwidWlkIjoiMDI3Yzk4YjktY2Y1NS00ZWIxLWI4ODAtZWJmZWFlMzQzZDc5In0.XYUEbOXhs1p289MGIIaXAc9RSc3Q1d5hYcYkIj9OfKg',
        'Content-Type': 'application/json',
    }
    data = {'name': 'TestKey'}

    response = requests.post(url, json=data, headers=headers)
    with open('json/get_api_key_response.json', 'w') as outfile:
        json.dump(response.json(), outfile, indent=4)


def using_api():
    url = 'https://api.air.fail/public/me'
    headers = {
        'Authorization': 'sk-pwpVfy5Zz19l1KMf9PpBZP8bT0GKj'
    }

    response = requests.get(url, headers=headers)
    with open('json/using_api_key_response.json', 'w') as outfile:
        json.dump(response.json(), outfile, indent=4)


def get_all_text_models():
    url = 'https://api.air.fail/public/text'
    headers = {
        'Authorization': 'sk-pwpVfy5Zz19l1KMf9PpBZP8bT0GKj'
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    with open('json/get_all_text_models_response.txt', 'w') as new_file:
        new_file.write(response.text)


# log_in()
# authorization()
# get_api_key()
# using_api()
get_all_text_models()