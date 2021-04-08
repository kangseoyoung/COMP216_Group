import random


start_id = 111


def create_data():
    global start_id
    hosts = ["google.com", "yahoo.com", "facebook.com", "twitter.com"]
    start_id += 1
    payload = {
        "id": start_id,
        "Course name": "Networking for software Development",
        "Course code": "Comp216"
    }
    return payload


def print_data(payload):
    print("Message ID: {}\n"\
    "Course name: {}\n"\
    "Course code: {}\n"\
    .format(payload.get("id"),
    payload.get("Course name"),
    payload.get("Course code")))