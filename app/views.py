from django.shortcuts import render
from .models import User,MusicList
from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


class Charts(View):
    """类视图：处理排行榜"""
    def get(self, request):
        """处理GET请求，返回票数页面"""
        data = {'c': MusicList.objects.all().order_by('-callNum')}
        print(data)
        return render(request, 'charts.html', data)

    def post(self, request):
        """处理POST请求"""
        pass
        return HttpResponse("POST")


