from django.db import models


# Create your models here.
class class_student(models.Model):
    sid = models.CharField(max_length=12, verbose_name='学生id')
    name = models.CharField(max_length=10, verbose_name='学生名称')
    class_room = models.CharField(max_length=50, verbose_name='教室')
    isroom = models.BooleanField(verbose_name="是否已经验证", default=False)

    def __str__(self):
        return self.name + "---" + self.class_room

    class Meat:
        db_table = 'class_student'


class query_log(models.Model):
    date = models.DateTimeField(verbose_name="查询时间", blank=True)
    class_room = models.CharField(max_length=30, verbose_name='班级')
    picture = models.ImageField(verbose_name='班级图片', null=True, upload_to='class_img/', blank=True)
    log = models.CharField(max_length=3000, verbose_name='查询结果')




    class Meat:
        db_table = 'query_log'
