from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class LoginViewMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "POST" and request.path not in ["/app/index1/", "/app/index2/", "/app/index3/"]:
            cookie_token = request.COOKIES.get("token")

            account = request.session["account"]

            cache_token = cache.get(account)

            if cookie_token != cache_token:
                data = {
                    "success": False,
                    "message": "未登录"
                }
                return JsonResponse(data, status=400)


