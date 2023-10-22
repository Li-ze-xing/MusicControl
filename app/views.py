import uuid

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from app.models import User, MusicList
from django.core.cache import cache


# Create your views here.
class Index1(View):
    def get(self,request):
        path=request.GET.get("from")
        if not path:
            path = "home"
        data={
            "path":path
        }
        # ////ac=request.COOKIE.get("account")
        # ////se=request.COOKIE.get("sessionid")
        #
        # ////cache.get("session"+se)
        response=JsonResponse(data)
        return response
    def post(self,request):
        fm=request.GET.get("from")
        print(fm)
        account=request.POST.get("account")
        password=request.POST.get("password")
        # nickname=request.POST.get("nickname")

        # # 验证验证码是否正确
        # code_client = request.POST.get("code")
        # # 去session中获取创建时的验证码
        # code_session = request.session.get("code")

        # if code_client.upper() != code_session.upper():
        #     return redirect("/app/login/")

        # 验证账号是否存在
        # 验证密码是否正确
        # 返回响应
        # return HttpResponse("登录成功")
        if not account or not password :
            data = {
                "success": False,
                "message": "账号或密码为空",
                "code": 10,
                "from":fm
            }
            return JsonResponse(data,status=400)
        # if code_client.upper() != code_session.upper():
        #     data = {
        #         "success": False,
        #         "message": "验证码错误",
        #         "code": 10,
        #         "from": fm
        #     }
        #     return JsonResponse(data, status=400)
        try:
            user=User.objects.get(account=account)
        except User.DoesNotExist as e:
            data={
                "success":False,
                "message":"账号不存在",
                "code":10,
                "from": fm
            }
            return JsonResponse(data,status=400)

        if user.password!=password:
            data = {
                "success": False,
                "message": "密码错误",
                "code": 10,
                "from": fm
            }
            return JsonResponse(data,status=400)
        # if code_client.upper() != code_session.upper():
        #     data = {
        #         "success": False,
        #         "message": "验证码错误",
        #         "code": 10,
        #         "from": fm
        #     }
        #     return JsonResponse(data, status=400)

        # ////request.session["token"]=str(uuid.uuid4())[:8]
        # ////request.session.set_expiry(30)

        data={
            "success": True,
            "message": "账号密码正确",
            "code": 20,
            "account":user.account,
            "from":fm
        }
        response = JsonResponse(data, status=200)
        # 1、写session
        request.session["account"] = user.account

        token_value = str(uuid.uuid4())[:8]
        response.set_cookie("token", token_value)

        # 写缓存
        cache.set(user.account, token_value, 60 * 60 * 24 * 7)

        return response


        # ////response = JsonResponse(data, status=200)
        # ////response.set_cookie("account",user.account)
        # ////eturn response



class Index2(View):
    def get(self,request):
        pass

    def post(self,request):
        account=request.POST.get("account")
        password=request.POST.get("password")
        nickname=request.POST.get("nickname")
        if not account or not password or not nickname:
            data = {
                "success": False,
                "message": "账号或密码或昵称为空",
                "code": 10,
            }
            return JsonResponse(data,status=400)
        try:
            print("111111111111111")
            user = User.objects.create(account=account,
                                       password=password,
                                       nickname=nickname,
                                       # music_id=MusicList(1),
                                       cardNum=0)
            print("2222222222222")
            data = {
                "success": True,
                "message": "注册成功",
                "code":20
            }
            return JsonResponse(data, status=200)
        except Exception as e:
            print(e)
            data = {
                "success": False,
                "message": "注册失败",
                "code":10
            }
            return JsonResponse(data, status=400)


        # try:
        #     userac=User.objects.get(account=account)
        # except User.DoesNotExist as e:
        #     # user=User.create
        #     # stu = Student.create(str(uuid.uuid4())[:8], 38, 1, "he iss", Grade.objects.get(id=1))
        #     # stu.save()
        #     # return HttpResponse(f"{stu.name}学生添加成功")
        #     try:
        #         userni = User.objects.get(nickname=nickname)
        #     except User.DoesNotExist as n:
        #         user=User(account=account,password=password,nickname=nickname,cardNum=0)
        #         user.save()
        #         data={
        #             "success": True,
        #             "message": "注册成功",
        #             "code": 20,
        #         }
        #         return JsonResponse(data,status=300)
        #     data={
        #         "success": False,
        #         "message": "昵称不能重复",
        #         "code": 10,
        #     }
        #     return JsonResponse(data,status=400)
        # data={
        #     "success":False,
        #     "message":"该用户名已存在",
        #     "code":10
        # }
        # return JsonResponse(data,status=400)




"""
使用pillow模块：pip install pillow
"""
from PIL import Image, ImageDraw, ImageFont
import random
import io

class Index3(View):
    def get(self,request):
        key = request.GET.get("key")  # register_code   login_code

        #1 创建画面对象
        width = 100
        height = 50
        bgcolor = (random.randrange(20, 100), random.randrange(20, 100), random.randrange(20, 100))
        im = Image.new("RGB", (width, height), bgcolor)

        #2 创建画笔
        draw = ImageDraw.Draw(im)

        #3 生成噪点
        for i in range(0, 100):
            # 绘制噪点
            xy = (random.randrange(0, width), random.randrange(0, height))
            fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
            # 参数1：点的位置
            # 参数2：点的颜色
            draw.point(xy, fill)

        #4 生成随机验证码
        base_str = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM"
        code_str = ""
        for i in range(0, 4):
            code_str += random.choice(base_str)
        print("--------------code_str =", code_str)

        #5 构造字体对象
        #参数1：字体文件路径  C:\Windows\Fonts\AdobeArabic-Bold.otf
        #参数2：字体大小
        font = ImageFont.truetype("D:\ziti\Adobe Arabic Bold.otf", 40)

        #6 写入内容
        # 参数1：位置
        # 参数2：内容
        # 参数font：字体
        # 参数fill：颜色
        draw.text((5, 2), code_str[0], font=font, fill=(255, random.randrange(0, 255), 255, random.randrange(0, 255)))
        draw.text((25, 2), code_str[1], font=font, fill=(255, random.randrange(0, 255), 255, random.randrange(0, 255)))
        draw.text((50, 2), code_str[2], font=font, fill=(255, random.randrange(0, 255), 255, random.randrange(0, 255)))
        draw.text((75, 2), code_str[3], font=font, fill=(255, random.randrange(0, 255), 255, random.randrange(0, 255)))

        #7 释放
        del draw

        #8 内存文件操作
        buf = io.BytesIO()
        im.save(buf, "png")

        #9 写入session
        request.session[key] = code_str

        #10 响应验证码数据
        return HttpResponse(buf.getvalue(),"image/png")


# class Index4(View):
#     def get(self,request):



