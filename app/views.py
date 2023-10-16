from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app.models import User, MusicList, MusicType
from django.views.generic import View


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
    def get(self, request, tid, pid):
        page_num = pid
        print(page_num)
        one_page_num = 10
        start_index = (int(page_num) - 1) * one_page_num
        end_index = start_index + one_page_num
        assign_type = list(MusicList.objects.filter(name=tid))
        print(assign_type)
        assign_typedict = {
            "assign_type": assign_type
        }
        return JsonResponse(assign_typedict)


class LookView(View):
    def post(self, request,musicName,page):
        query_content = musicName #request.POST.get("name")
        page_num = page  #request.POST.get("pid")  # 获取页数信息
        print("--------------------",musicName,page)
        one_page_num = 10
        start_index = (page_num - 1) * one_page_num
        end_index = start_index + one_page_num
        query_music = list(MusicList.objects.raw(f"select * from music_list where name like '%{query_content}%'")
                           [start_index:end_index])
        print("-------------------2",query_music)
        query_music_dict = {
            "query_music": query_music
        }
        return JsonResponse(query_music_dict)


class CollectView(View):
    def get(self, request, uid):
        # 现在用的传参确定用户,后续改成根据当前登录用户确定
        # user_num = request.GET.get(uid)
        user = User.objects.get(id=uid)
        page_num = request.POST.get("pid")  # 获取页数信息
        one_page_num = 10
        start_index = (page_num - 1) * one_page_num
        end_index = start_index + one_page_num
        user_music = list(user.music_id.all()[start_index:end_index])
        music_list = {
            "user_music": user_music
        }
        return JsonResponse(music_list)


class DetailView(View):
    def get(self, request):
        music_name = request.GET.get("name")
        page_num = request.POST.get("pid")  # 获取页数信息
        one_page_num = 10
        start_index = (page_num - 1) * one_page_num
        end_index = start_index + one_page_num
        music_detail = list(MusicList.objects.raw(
            f"select * from music_list as ml join comments as mc on ml.id=mc.music_comments_id where ml.name='{music_name}'")
                            [start_index:end_index])
        music_detail_dict = {
            "music_detail": music_detail
        }
        return JsonResponse(music_detail_dict)


#  YanZhenHao -------------------------------------------------------------------------------------
class Charts(View):
    """类视图：处理排行榜"""

    def get(self, request):
        """处理GET请求，返回票数页面"""
        info = list(MusicList.objects.all().order_by('-callNum').values())
        data = {'c': info}
        # return render(request, 'charts.html', data)
        return JsonResponse(data)

    def post(self, request):
        """处理POST请求"""
        pass
        return HttpResponse("POST")
