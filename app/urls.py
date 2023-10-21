from django.urls import path, re_path
from app import views

urlpatterns = [
    #  ChenYiMing -------------------------------------------------------------------------------------
    # 音乐分类管理
    path("hostInfo/type/", views.TypeView.as_view(), name='type'),
    re_path("hostInfo/typeInner/(\w+)/(\d+)/(\d+)", views.AssignView.as_view(), name="assign"),
    # 音乐搜索功能
    re_path("hostInfo/lookup/(\w+)/(\d+)/(\d+)", views.LookView.as_view(), name="lookup"),
    # 音乐详情 (收藏的歌曲中 选择显示打榜信息，评论，)
    # collect可以不用正则,后续可以根据登录用户确定id
    # 用户歌单
    re_path("personHost/collect/(\d+)/(\d+)", views.CollectView.as_view(), name="collect"),
    # 评论
    re_path("MusicInfo/detail/(\w+)/(\d+)/(\d+)", views.DetailView.as_view(), name="detail"),

    # YangZhenHao ----------------------------------------------------------------------
    path('hostInfo/charts/', views.Charts.as_view(), name='charts'),

    # YangFengYuan --------------------------------------------------------------------------------
    path("login/", views.Index1.as_view(), name="login"),
    path("register/", views.Index2.as_view(), name="register"),
    path("code/", views.Index3.as_view(), name="code"),

    # GaoZeXu ------------------------------------------------------------------------------------------
    # 退出登录
    path('logout/', views.LogoutAccount.as_view(), name='logout'),
    # 签到
    path('check-in/', views.CheckIn.as_view(), name='check_in'),
    # 收藏歌曲
    re_path('relation/(\d+)/(\d+)', views.Relation.as_view(), name="relation"),

]
