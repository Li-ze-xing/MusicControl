from django.db import models


# Create your models here.

class MyManager(models.Manager):
    def get_queryset(self):
        # super()   Student.objects.all()
        return super().get_queryset().filter(isDelete=False)


# 音乐类型 ----------------------------------------------------------------------------------------
class MusicTypeManager(MyManager):
    # 重写create
    def create(self, name):
        # self.model ==  Student
        obj = self.model(name=name)
        obj.save()

        return obj


# 音乐类型
class MusicType(models.Model):
    objects = MusicTypeManager()
    name = models.CharField(max_length=10, unique=True)  # 类型名

    class Meta:
        db_table = "music_type"


# 音乐评论 ------------------------------------------------------------------------------------------
class MusicCommentsManager(MyManager):
    # 重写create
    def create(self, comments, user_id, music_comments):
        # self.model ==  Student
        obj = self.model(comments=comments, user_id=user_id, music_comments=music_comments)
        obj.save()

        return obj


class MusicComments(models.Model):
    objects = MusicCommentsManager()

    comments = models.CharField(max_length=100)

    user_id = models.ForeignKey("User",on_delete=models.CASCADE)
    music_comments = models.ForeignKey("MusicList", on_delete=models.CASCADE)

    class Meta:
        db_table = "comments"


# 音乐列表 ------------------------------------------------------------------------------------------
class MusicListManager(MyManager):
    # 重写create
    def create(self, name, context, callNum, music_type):
        # self.model ==  Student
        obj = self.model(name=name, context=context, callNum=callNum, music_type=music_type)
        obj.save()

        return obj


class MusicList(models.Model):
    objects = MusicListManager()

    name = models.CharField(max_length=50, unique=True)  # 音乐名
    context = models.CharField(max_length=100)  # 简介
    callNum = models.IntegerField()  # 总票数

    isDelete = models.BooleanField(default=False)  # 默认值
    music_type = models.ForeignKey("MusicType", on_delete=models.CASCADE)

    class Meta:
        db_table = "music_list"


# 用户数据 -------------------------------------------------------------------------------------------
class UserManager(MyManager):
    # 重写create
    def create(self, account, password, nickname, cardNum):
        # self.model ==  Student
        obj = self.model(account=account, password=password, nickname=nickname, cardNum=cardNum)
        obj.save()

        return obj


class User(models.Model):
    objects = UserManager()

    account = models.CharField(max_length=20, unique=True)  # 账号
    password = models.CharField(max_length=20)  # 密码
    nickname = models.CharField(max_length=10, unique=True)  # 昵称
    cardNum = models.IntegerField()  # 打榜票数

    isDelete = models.BooleanField(default=False)  # 默认值
    music_id = models.ManyToManyField("MusicList")

    class Meta:
        db_table = "user"
