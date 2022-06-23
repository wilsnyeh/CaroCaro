import django
import os
import sys
import time
import json
import requests

sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service_project.settings")
django.setup()

from service_rest.models import AutomobileVO


def get_inventory():
    response = requests.get("http://inventory-api:8000/api/automobiles/")
    content = json.loads(response.content)
    # print(content)
    for auto in content["autos"]:
        AutomobileVO.objects.update_or_create(
            vin=auto["vin"],
            defaults={
                "color": auto["color"],
                "year": auto["year"],
                "model": auto["model"],
                "vip": auto["vip"],
            },
        )


def poll():
    while True:
        print("Service poller polling for data")
        try:
            get_inventory()
            pass
        except Exception as e:
            # print(e, file=sys.stderr)
        time.sleep(60)


if __name__ == "__main__":
    poll()
