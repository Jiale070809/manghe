from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    gender = models.CharField(max_length=10, choices=[('male', '男'), ('female', '女')], null=True, blank=True)
    body_type = models.CharField(max_length=20, choices=[('thin', '瘦'), ('normal', '正常'), ('fat', '胖')], null=True,
                                 blank=True)
    height = models.IntegerField(null=True, blank=True)  # 身高(cm)
    interests = models.TextField(null=True, blank=True)  # 兴趣标签,用逗号分隔
    profile_image = models.ImageField(upload_to='profiles/', default='default.png')
    privacy = models.BooleanField(default=True)  # True:公开资料,False:私密
    is_active = models.BooleanField(default=True)


class UserMatch(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE)
    match_score = models.IntegerField()  # 匹配度(0-100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')


from django.db import models

# Create your models here.
