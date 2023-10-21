from django.http import JsonResponse, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class VfcodeViewMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "POST" and request.path in ["/app/login/", "/app/register/"]:
            key = str(request.GET.get("key"))
            code_client = request.POST.get("code")

            code_session = request.session.get(key)# register_code  login_code
            print("--------------",code_session,code_client,key,request.session.session_key)

            if code_client.upper() != code_session.upper():
                data = {
                    "success": False,
                    "message": "验证码错误"
                }
                return JsonResponse(data)

    def proces_response(self, request, response):
        # 删除验证码session
        key = request.GET.get("key")
        del request.session[key]

        return response
