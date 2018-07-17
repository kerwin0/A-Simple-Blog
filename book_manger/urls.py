"""book_manger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from book import views
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path("^$", views.home, name="Home"),  # 首页


    re_path("^addpublish/$", views.add_publish, name="AddPublish"),  # 添加出版社
    re_path("^publish/$", views.info_publish, name="InfoPublish"),  # 出版社管理
    re_path("changepub/(?P<change_id>\d+)", views.change_publish),  # 修改出版社
    re_path("deletepub/(?P<delete_id>\d+)", views.delete_publish),  # 删除出版社

    re_path("^addauthor/$", views.add_author, name="AddAuthor"),  # 添加作者
    re_path("^author/$", views.info_author, name="InfoAuthor"),  # 作者管理
    re_path("changeauthor/(?P<change_id>\d+)", views.change_author),  # 修改作者
    re_path("deleteauthor/(?P<delete_id>\d+)", views.delete_author),  # 删除作者

    re_path("^addbook/$", views.add_book, name="AddBook"),  # 添加书籍
    re_path("^book/$", views.info_book, name="InfoBook"),  # 查看书籍
    re_path("changebook/(?P<change_id>\d+)", views.change_book),  # 修改书籍
    re_path("deletebook/(?P<delete_id>\d+)", views.delete_book),  # 删除书籍

    re_path("^login/$", views.login, name="Login"),
    re_path("^logout/$", views.logout),
    re_path("^register/$", views.register),

    ################################
    re_path("^ajax$", views.my_ajax),
    re_path("^a/$", views.a),
    re_path("^b/", views.b),
    re_path("^c/", views.c),

]
