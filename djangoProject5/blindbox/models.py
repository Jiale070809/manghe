from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)  # 如:男生盲盒/女生盲盒/身高170+等
    description = models.TextField(blank=True)


    def __str__(self):
        return self.name


class BlindBox(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_boxes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class OpenRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opened_boxes')
    blindbox = models.ForeignKey(BlindBox, on_delete=models.CASCADE)
    opened_at = models.DateTimeField(auto_now_add=True)
    matched_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='matched_boxes')

    class Meta:
        unique_together = ('user', 'blindbox')  # 每个用户只能开一次同一个盲盒


from django.db import models

# Create your models here.
