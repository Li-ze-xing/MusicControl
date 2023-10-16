from django.urls import path, re_path
from app import views

urlpatterns = [
    #  ChenYiMing -------------------------------------------------------------------------------------
    # 音乐分类管理
    path("hostInfo/type/", views.TypeView.as_view(), name='type'),
    re_path("hostInfo/type/(\w+)/(\d+)", views.AssignView.as_view(), name="assign"),
    # 音乐搜索功能
    re_path("hostInfo/lookup/(\w+)/(\d+)", views.LookView.as_view(), name="lookup"),
    # 音乐详情 (收藏的歌曲中 选择显示打榜信息，评论，)
    # collect可以不用正则,后续可以根据登录用户确定id
    re_path("hostInfo/collect/(\d)+", views.CollectView.as_view(), name="collect"),
    re_path("hostInfo/detail/(\w+)", views.DetailView.as_view(), name="detail"),

    # YangZhenHao ----------------------------------------------------------------------
    path('hostInfo/charts/', views.Charts.as_view(), name='charts'),
]
