from django.urls import path, re_path
from app import views

urlpatterns = [
    # 音乐分类管理
    path("type/", views.TypeView.as_view(), name='type'),
    re_path("kind/(\w+)/(\d+)/(\d+)", views.AssignView.as_view(), name="assign"),
    # 音乐搜索功能
    re_path("lookup/(\w+)/(\d+)/(\d+)", views.LookView.as_view(), name="lookup"),
    # 音乐详情 (收藏的歌曲中 选择显示打榜信息，评论，)
    # collect可以不用正则,后续可以根据登录用户确定id
    re_path("collect/(\d+)/(\d+)/(\d+)", views.CollectView.as_view(), name="collect"),
    re_path("detail/(\w+)/(\d+)/(\d+)", views.DetailView.as_view(), name="detail"),
    re_path("add_com/(\w+)/(\w+)", views.AddComView.as_view(), name="addcom")
]
                                