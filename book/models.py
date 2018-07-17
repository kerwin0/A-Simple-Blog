from django.db import models
import datetime
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
# Create your models here.


class Book(models.Model):
    """
    name:书名
    price:价格
    publish_date:出版日期
    publish:出版社id
    """
    name = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    publish_date = models.DateField(auto_now_add=True)
    # 创建外键，关联publish
    publish = models.ForeignKey(to="Publish", to_field="id", on_delete=models.CASCADE)
    # 创建多对多关联author
    authors = models.ManyToManyField(to="Author")

    def __str__(self):
        return self.name


class Publish(models.Model):
    """
    name:出版社名称
    city:出版社城市
    """
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Author(models.Model):
    """
    name:作者名
    age:年龄
    phone:手机
    """
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    phone = models.IntegerField(max_length=11)
    # 创建一对一关联AuthorDetail
    detail = models.OneToOneField(to="AuthorDetail", to_field="id", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AuthorDetail(models.Model):
    """
    address:地址
    author_email:邮箱
    """
    address = models.CharField(max_length=32)
    author_email = models.EmailField()


class Login(models.Model):
    name = models.CharField(max_length=12)
    pwd = models.CharField(max_length=12)
    email = models.EmailField()


class Userinfo(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    tel = models.IntegerField()
    e_mail = models.EmailField()
