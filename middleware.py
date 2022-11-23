from rest_framework.response import Response
from datetime import datetime


class CheckTime():
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        print('Hello')
        start = datetime.now()
        response: Response = self.get_response(request)
        end = datetime.now()
        print('total time'.upper(), end-start)

        return response
        