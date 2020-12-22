import openaq
import json
import time


MAX_RETRIES = 5

api = openaq.OpenAQ()
all_locations = []

status, resp = api.locations()
no_pages = int(resp["meta"]["pages"])
all_locations += resp["results"]

for page_num in range(2, no_pages + 1):

    for ii in range(MAX_RETRIES):
        print(f"retrieving page #{page_num}, {ii} attempt")

        try:
            status, resp = api.locations(page=page_num)
        except openaq.exceptions.ApiError:
            time.sleep(1)
            continue
        else:
            break
    all_locations += resp["results"]
    time.sleep(1)

with open("all_openaq_locations.json", "w") as fout:
    json.dump(all_locations, fout)
