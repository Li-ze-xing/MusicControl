from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app.models import User, MusicList, MusicType, MusicComments, Sign
from django.views.generic import View
from django.core.paginator import Paginator


# Create your views here.

#  ChenYiMing -------------------------------------------------------------------------------------

class TypeView(View):
    def get(self, request):
        types = list(MusicType.objects.all().values())
        typedict = {
            "types": types
        }
        return JsonResponse(typedict)


class AssignView(View):
    def post(self, request, mid, pid, cid):
        page_num = pid
        per_page = cid
        assign_type = list(MusicList.objects.all().filter(
            music_type=MusicType.objects.get(name=mid)).values())  # [start_index:end_index])
        paginator = Paginator(assign_type, per_page)
        pg = paginator.page(page_num)
        assign_typedict = {
            "pg_con": list(pg),
            "page_left": pg.has_previous(),
            "page_right": pg.has_next(),
        }
        return JsonResponse(assign_typedict)


class LookView(View):
    def get(self, request, q_con, pid, cid):
        query_content = q_con
        page_num = pid  # 获取页数信息
        per_page = cid
        query_music = list(MusicList.objects.all().filter(name__contains=query_content).values())
        paginator = Paginator(query_music, per_page)
        pg = paginator.page(page_num)
        query_music_dict = {
            "pg_con": list(pg),
            "page_left": pg.has_previous(),
            "page_right": pg.has_next(),
        }
        return JsonResponse(query_music_dict)


class CollectView(View):
    def post(self, request, pid, cid):
        # 现在用的传参确定用户,后续改成根据当前登录用户确定
        user_acc = request.POST.get("account")

        if user_acc:
            user = User.objects.get(account=user_acc)
            page_num = pid  # 获取页数信息
            per_page = cid
            user_music = list(user.music_id.all().values())
            paginator = Paginator(user_music, per_page)
            pg = paginator.page(page_num)
            music_list = {
                "nickname": user.nickname,
                "pg_con": list(pg),
                "page_left": pg.has_previous(),
                "page_right": pg.has_next()
            }
            return JsonResponse(music_list)
        else:
            music_list = {
                "nickname": None
            }
            return JsonResponse(music_list)


class DetailView(View):
    def post(self, request, m_name, pid, cid):
        music_name = m_name
        text = request.POST.get("text")
        user = request.POST.get("account")

        try:
            MusicComments.objects.create(comments=text, user_id=User.objects.get(account=user),
                                         music_comments=MusicList.objects.get(name=music_name))
            data = {
                "success": True,
                "message": ""
            }
            return JsonResponse(data)
        except Exception as e:
            data = {
                "success": False,
                "message": str(e)
            }
            return JsonResponse(data)

    def get(self, request, m_name, pid, cid):
        page_num = pid  # 获取页数信息
        per_page = cid
        music = MusicList.objects.get(name=m_name)
        music_detail = list(MusicComments.objects.select_related("user_id").filter(music_comments=int(music.id)).values(
            'user_id__nickname', 'comments'))[::-1]
        paginator = Paginator(music_detail, per_page)
        pg = paginator.page(page_num)
        music_detail_dict = {
            "pg_con": list(pg),
            "page_left": pg.has_previous(),
            "page_right": pg.has_next()
        }
        return JsonResponse(music_detail_dict)


#  YanZhenHao -------------------------------------------------------------------------------------
class Charts(View):
    """类视图：处理排行榜"""

    def get(self, request):
        """处理GET请求，返回票数页面"""
        info = list(MusicList.objects.all().order_by('-callNum').values())[:10]
        data = {'c': info}
        return JsonResponse(data)


# YangFengYuan --------------------------------------------------------------------------------
class Index1(View):
    def post(self, request):
        account = request.POST.get("account")
        password = request.POST.get("password")

        try:
            user = User.objects.get(account=account)
        except User.DoesNotExist as e:
            data = {
                "success": False,
                "message": "账号不存在",
            }
            return JsonResponse(data)

        if user.password != password:
            data = {
                "success": False,
                "message": "密码错误",
            }
            return JsonResponse(data)

        data = {
            "success": True,
            "message": "账号密码正确",
            "account": [user.account, user.nickname],
        }

        return JsonResponse(data)


class Index2(View):
    def get(self, request):
        pass

    def post(self, request):
        account = request.POST.get("account")
        password = request.POST.get("password")
        nickname = request.POST.get("nickname")
        try:
            User.objects.create(account=account,
                                password=password,
                                nickname=nickname,
                                cardNum=0)
            data = {
                "success": True,
                "message": "注册成功",
            }
            return JsonResponse(data)
        except Exception as e:
            print("-------------------e3", e)

            if f"Duplicate entry '{nickname}' for key 'user.nickname'" in str(e):
                data = {
                    "success": False,
                    "message": "昵称重复",
                }
                return JsonResponse(data)
            elif f"Duplicate entry '{account}' for key 'user.account'" in str(e):
                data = {
                    "success": False,
                    "message": "用户已存在",
                }
                return JsonResponse(data)

            data = {
                "success": False,
                "message": "不可抗力原因注册失败",
            }
            return JsonResponse(data)


# GaoZeXu ------------------------------------------------------------------------------------------

class CheckIn(View):
    def get(self, request):
        try:
            user = request.GET.get("account")  # 获取当前用户
            info = User.objects.get(account=user)
            data = {
                "success": True,
                "userinfo": info.cardNum
            }
            return JsonResponse(data)
        except Exception as e:
            print("e", e)
            data = {
                "success": False,
                "userinfo": e
            }
            return JsonResponse(data)

    def post(self, request):
        try:
            user = request.POST.get("account")  # 获取当前用户
            today = timezone.now().date()  # 获取当前日期
            # 检查用户今日是否登录
            user, created = User.objects.get_or_create(account=user)
            sign = Sign.objects.filter(user=user, datatime=today).first()  # 检查用户今日是否签到

            if not sign:  # 如果用户尚未签到
                Sign.objects.create(user=user, datatime=today)  # 创建签到记录
                user.cardNum += 5
                user.save()
                data = {
                    'success': True,
                    'message': '签到成功，获得5张票'
                }
                # 增加用户的票数（假设User.cardNum是一个字段）
                return JsonResponse(data)
            else:
                data = {
                    'success': False,
                    'message': '您已签到，无需重复操作'
                }
                return JsonResponse(data)  # 如果用户已经签到，返回错误消息
        except Exception as e:
            return JsonResponse({'success': False, 'message': '服务器错误，请稍后再试'})


class Relation(View):

    def get(self, request, uer_id, musiclist_id):
        user = User.objects.get(account=uer_id)  # 用你的实际逻辑获取用户
        music_list = MusicList.objects.get(name=musiclist_id)  # 用你的实际逻辑获取音乐列表

        # 使用filter方法来检查关系是否存在
        if user.music_id.filter(pk=music_list.id).exists():
            # 关系已经建立
            print("关系已建立")
            data = {
                'success': True,
                'userNum': user.cardNum,
                "musicNum": music_list.callNum
            }
            return JsonResponse(data)  # 如果用户已经签到，返回错误消息

        else:
            # 关系未建立
            print("关系未建立")
            data = {
                'success': False,
                'userNum': user.cardNum,
                "musicNum": music_list.callNum
            }
            return JsonResponse(data)  # 如果用户已经签到，返回错误消息

    def post(self, request, uer_id, musiclist_id):
        try:
            # 找到id为的用户
            user = User.objects.get(account=uer_id)
            # 找到id为musiclist_id的音乐
            music = MusicList.objects.get(name=musiclist_id)

            # 将两个对象形成关系
            user.music_id.add(music)

            # 将关系数据存到第三张表中
            music.save()
            data = {
                "success": True,
                "error": None
            }
            return JsonResponse(data)
        except Exception as e:
            data = {
                "success": False,
                "error": e
            }
            return JsonResponse(data)

    def delete(self, request, uer_id, musiclist_id):
        try:
            # 找到id为的用户
            user = User.objects.get(account=uer_id)
            # 找到id为musiclist_id的音乐
            music = MusicList.objects.get(name=musiclist_id)
            # 解除关系
            user.music_id.remove(music)
            data = {
                "success": True,
                "error": None
            }
            return JsonResponse(data)
        except Exception as e:
            data = {
                "success": False,
                "error": e
            }
            return JsonResponse(data)


class AddCheck(View):

    def post(self, request):
        try:
            account = request.POST.get("account")
            musicName = request.POST.get("musicName")
            cards = int(request.POST.get("piao"))
            print("---------------", account, musicName, cards)
            user = User.objects.get(account=account)
            user.cardNum -= cards
            music = MusicList.objects.get(name=musicName)
            music.callNum += cards

            user.save()
            music.save()
            data = {
                "success": True,
                "info": music.callNum,
                "error": None
            }
            return JsonResponse(data)
        except Exception as e:
            print("-----------e", e)
            data = {
                "success": True,
                "error": e
            }
            return JsonResponse(data)
