from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app.models import User, MusicList, MusicType, MusicComments
from django.views.generic import View
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage


# Create your views here.

# def func(request):
#     info = User.objects.get(pk="1")
#
#     data ={
#         "info": info
#     }
#
#     return HttpResponse(info.password)


class TypeView(View):
    def get(self, request):
        types = list(MusicType.objects.all().values())
        typedict = {
            "pg_con": types
        }
        return JsonResponse(typedict)


class AssignView(View):
    def get(self, request, mid, pid, cid):
        # page_num = pid
        # one_page_num = 10
        # start_index = (int(page_num) - 1) * one_page_num
        # end_index = start_index + one_page_num
        page_num = pid
        per_page = cid
        assign_type = list(MusicList.objects.all().filter(music_type=MusicType.objects.get(name=mid)).values())   #
        paginator = Paginator(assign_type, per_page)
        pg = paginator.page(page_num)


        assign_typedict = {
            "pg_con": list(pg),
            "page_lift": pg.has_previous(),
            "page_right": pg.has_next(),
        }
        return JsonResponse(assign_typedict)


class LookView(View):
    def post(self, request, q_con, pid, cid):
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
    def get(self, request, uid, pid, cid):
        # 现在用的传参确定用户,后续改成根据当前登录用户确定
        # user_num = request.GET.get(uid)
        user = User.objects.get(id=uid)
        page_num = pid # 获取页数信息
        per_page = cid
        user_music = list(user.music_id.all().values())
        paginator = Paginator(user_music, per_page)
        pg = paginator.page(page_num)
        music_list = {
            "pg_con": list(pg),
            "page_left": pg.has_previous(),
            "page_right": pg.has_next()
        }
        return JsonResponse(music_list)


class DetailView(View):
    def get(self, request, m_name, pid, cid):
        music_name = m_name
        page_num = pid  # 获取页数信息
        per_page = cid
        music = MusicList.objects.get(name=m_name)
        music_detail = list(MusicComments.objects.filter(music_comments=int(music.id)).values())
        # music_detail = list(
        #     MusicComments.objects.filter(music_comments_id=music))

        print(music_detail)
        paginator = Paginator(music_detail, per_page)
        pg = paginator.page(page_num)
        music_detail_dict = {
            "pg_con": list(pg),
            "page_left": pg.has_previous(),
            "page_right": pg.has_next()
        }
        return JsonResponse(music_detail_dict)


class AddComView(View):
    def post(self, request, comment, m_name):
        user_acc = request.session.get("account")  # 写评论的用户是谁
        # user_acc = "asdas"
        # 根据session账号在用户表里找到该用户的id  直接orm查询
        user_id = User.objects.get(account=user_acc)
        print(user_id.id)
        # 根据音乐名在音乐列表里找到该音乐的id   用外键找,上边有例子
        music_num = MusicList.objects.get(name=m_name)
        print(music_num.id)
        print(comment)
        # 添加到评论表中
        add_com = MusicComments.objects.create(comments=comment, music_comments=music_num, user_id=user_id)
        add_com.save()
        data = {
            "success": True,
            "massage": "添加成功"
        }
        # data = {
        #   "success": False
        #   "reason": "报错原因"
        # }
        return JsonResponse(data)









# # 添加数据，等下删除
# class relation(View):
#     def get(self, request, wid, cid):
#         # 找到id为wid的工人
#         user = User.objects.get(id=wid)
#         # 找到id位cid的计算机
#         music = MusicList.objects.get(id=cid)
#         # 将两个对象形成关系
#         user.music_id.add(music)
#         # 将关系数据存到第三张表中
#         music.save()
#         return HttpResponse(f"{wid}和{cid}形成关系")


