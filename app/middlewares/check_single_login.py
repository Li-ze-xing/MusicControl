from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class LoginViewMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "POST" and request.path not in ["/app/login/", "/app/register/", "/app/code/"]:
            cookie_token = request.COOKIES.get("token")
            print(request)
            print("------------------request.COOKIES", request.COOKIES)
            print("------------------cookie_token", cookie_token)
            account = request.session.get("account")
            print("------------------account",account)
            cache_token = cache.get(account)
            print("------------------cache_token", cache_token)

            if cookie_token != cache_token:
                data = {
                    "success": False,
                    "message": "未登录"
                }
                return JsonResponse(data, status=400)


