from django.db import models


# Create your models here.

# 音乐类型
class MusicType(models.Model):
    name = models.CharField(max_length=10, unique=True)  # 类型名

    class Meta:
        db_table = "music_type"


# 音乐评论
class MusicComments(models.Model):
    comments = models.CharField(max_length=100)
    user_id = models.IntegerField()

    class Meta:
        db_table = "comments"


# 音乐列表
class MusicList(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 音乐名
    context = models.CharField(max_length=100)  # 简介
    callNum = models.IntegerField()  # 总票数

    isDelete = models.BooleanField(default=False)  # 默认值
    music_type = models.ForeignKey("MusicType", on_delete=models.CASCADE)
    music_comments = models.ManyToManyField("MusicComments")

    class Meta:
        db_table = "music_list"


# 用户数据
class User(models.Model):
    account = models.CharField(max_length=20, unique=True)  # 账号
    password = models.CharField(max_length=20)  # 密码
    nickname = models.CharField(max_length=10, unique=True)  # 昵称
    cardNum = models.IntegerField()  # 打榜票数

    isDelete = models.BooleanField(default=False)  # 默认值
    music_id = models.ManyToManyField("MusicList")

    class Meta:
        db_table = "user"
