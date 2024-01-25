import base64
import requests


class MoonPhaseApi:

    def __init__(self, app_id:str, app_secret:str) -> None:
        userpass = f"{app_id}:{app_secret}"
        self.auth_string = base64.b64encode(userpass.encode()).decode()
    
    