from django.shortcuts import render, HttpResponse, redirect, reverse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from book import models
from book.my_form import Myform
import json


def judge(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get("is_login")
        if is_login:
            # name = request.session.get("name")
            # time_now = request.session.get("time_now")
            ret = func(request, *args, **kwargs)
            return ret
        else:
            return redirect("/login/")

    return inner


def index(request):
    """
    首页
    """
    # 一对多
    # 查询主键为1的书籍的出版社所在的城市
    # ret = models.Book.objects.get(id=1)
    # print(ret.publish.name)

    # ret = models.Book.objects.filter(id=1).values("publish__city")
    # ret = models.Publish.objects.filter(book__id=1).values("city")

    # 查询出版社出版过的书籍
    # ret = models.Publish.objects.filter(name="红袖出版社").first()
    # for i in ret.book_set.all():
    #     print(i.name)

    # ret = models.Book.objects.filter(publish__name="红袖出版社").values("name")
    # ret = models.Publish.objects.filter(name="红袖出版社").values("book__name")
    # print(ret)

    # 一对一
    # 查询作者的手机号
    # ret = models.Author.objects.filter(name="吴起").first()
    # print(ret.detail.address)
    # ret = models.Author.objects.filter(name="吴起").values("detail__address")
    # ret1 = models.AuthorDetail.objects.filter(author__name="吴起").values("address")
    # print(ret, "\n", ret1)

    # 查询春秋魏国的作者
    # ret = models.AuthorDetail.objects.filter(address="战国魏国")
    # for i in ret:
    #     print(i.author.name)

    # ret = models.Author.objects.filter(detail__address="战国魏国").values("name")
    # ret1 = models.AuthorDetail.objects.filter(address="战国魏国").values("author__book__name")
    # print(ret, ret1)

    # 多对多
    # 孙子所有作者的名字以及地址
    # ret = models.Book.objects.filter(name="孙子").first()
    # ret1 = ret.authors.all()
    # for i in ret1:
    #     print(i.name, i.detail.address)

    # ret = models.Book.objects.filter(name="孙子").values("authors__detail__address", "authors__name")
    # print(ret)

    # 查询吴起出过的所有书籍的名字
    # ret = models.Author.objects.get(name="姜太公")
    # ret1 = ret.book_set.all()
    # for i in ret1:
    #     print(i.name)

    #######################聚合与分组###############################
    from django.db.models import Max, Min, Count, Avg
    # print(models.Book.objects.all().aggregate(Avg("price")))

    # 分组
    # 查询每个出版社出版的书籍总数
    # 单表
    # ret = models.Book.objects.values("publish__id").annotate(Count("name"))
    # print(ret)

    # 查询每个出版社名称和出版的书籍总数
    # ret = models.Publish.objects.values("name").annotate(a=Count("book__name")).values("name", "a")
    # print(ret)
    return render(request, "../../blogs/templates/base.html")


@csrf_exempt
def login(request):
    # if request.body:
    #     data = json.loads(request.body.decode("utf8"))
    #     print(data)
    #     login_obj = models.Login.objects.filter(name=data["name"], pwd=data["pwd"])
    #     if login_obj:
    #         print(1)
    #         return HttpResponse("1")
    #     else:
    #         print(0)
    #         return HttpResponse("0")

    import datetime
    if request.method == "POST":
        name = request.POST.get("user")
        pwd = request.POST.get("pwd")
        if models.Login.objects.filter(name=name, pwd=pwd):
            request.session["is_login"] = True
            request.session["name"] = name
            request.session["time_now"] = datetime.datetime.now().strftime("%Y-%m-%d %X")
        return redirect("/")

    # import datetime
    # if request.method == "POST":
    #     name = request.POST.get("user")
    #     pwd = request.POST.get("pwd")
    #     if models.Login.objects.filter(name=name, pwd=pwd):
    #         request.session["is_login"] = True
    #         request.session["name"] = name
    #         login_obj = models.Login.objects.filter(name=name, pwd=pwd)
    #         login_obj.time = datetime.datetime.now()
    #         login_obj.save()
    #         return redirect("/")
    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        form = Myform(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            models.Login.objects.create(name=name, pwd=pwd, email=email)
            return redirect("/login/")
        else:
            g_error = form.errors.get("__all__")
            if g_error:
                g_error = g_error[0]
            return render(request, "register.html", locals())
    form = Myform()
    return render(request, "register.html", {"form": form})


@judge
def home(request, *args):
    # name, time_now = args
    return render(request, "home.html")


def logout(request):
    request.session.flush()
    return redirect("/login/")


@judge
def info_publish(request, *args):
    """
    出版社信息页面
    """
    ret = models.Publish.objects.all()
    # name, time_now = args
    return render(request, "info_publish.html", {"ret": ret})


def add_publish(request):
    """
    添加出版社
    :return:添加出版社页面
    """
    if request.method == "POST":
        new_name = request.POST.get("new_name")
        new_city = request.POST.get("new_city")
        models.Publish.objects.create(name=new_name, city=new_city)
        return redirect("InfoPublish")
    return render(request, "add_publish.html")


def change_publish(request, change_id):
    """
    修改出版社
    :param request:
    :param change_id: 出版社id
    :return: 出版社信息页面
    """
    if request.method == "POST":
        new_name = request.POST.get("new_name")
        new_city = request.POST.get("new_city")
        models.Publish.objects.filter(id=change_id).update(name=new_name, city=new_city)
        return redirect("InfoPublish")
    ret = models.Publish.objects.get(id=change_id)
    return render(request, "change_publish.html", {"ret": ret})


def delete_publish(request, delete_id):
    """
    删除出版社
    :return: 出版社信息页面
    """
    models.Publish.objects.filter(id=delete_id).delete()
    return redirect("InfoPublish")


def add_author(request):
    """
    添加作者
    :return: 添加作者页面
    """
    if request.method == "POST":
        new_name = request.POST.get("new_name")
        new_age = request.POST.get("new_age")
        new_phone = request.POST.get("new_phone")
        new_address = request.POST.get("new_address")
        new_email = request.POST.get("new_email")
        det_obj = models.AuthorDetail.objects.create(address=new_address, author_email=new_email)
        models.Author.objects.create(name=new_name, age=new_age, phone=new_phone, detail_id=det_obj.id)
        return redirect("InfoAuthor")
    return render(request, "add_author.html")


@judge
def info_author(request, *args):
    """
    作者管理
    """
    ret = models.Author.objects.all()
    # name, time_now = args
    return render(request, "info_author.html", {'author_list': ret})


def change_author(request, change_id):
    """
    修改作者信息
    :return: 作者管理页面
    """
    if request.method == "POST":
        new_name = request.POST.get("new_name")
        new_age = request.POST.get("new_age")
        new_phone = request.POST.get("new_phone")
        new_address = request.POST.get("new_address")
        new_email = request.POST.get("new_email")

        ret = models.Author.objects.filter(id=change_id)  # 作者queryset
        de_id = ret.first().detail_id  # 作者详情id

        ret.update(name=new_name, age=new_age, phone=new_phone)
        models.AuthorDetail.objects.filter(id=de_id).update(address=new_address, author_email=new_email)

        return redirect("InfoAuthor")
    ret = models.Author.objects.get(id=change_id)
    return render(request, "change_author.html", {"ret": ret})


def delete_author(request, delete_id):
    """
    删除作者与作者信息
    :param delete_id: 作者id
    :return: 作者管理页面
    """
    dic = {"result": None}
    try:
        # ret = models.Author.objects.get(id=delete_id)
        # models.AuthorDetail.objects.filter(id=ret.detail_id).delete()
        # ret.delete()
        dic["result"] = "删除成功"
    except Exception as e:
        pass
    # return redirect("InfoAuthor")
    return HttpResponse(json.dumps(dic))


def add_book(request):
    """
    添加书籍
    :return: 书籍信息页面
    """
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        new_price = request.POST.get('new_price')
        new_date = request.POST.get('new_date')
        new_publish_id = request.POST.get('publish')
        author_list = request.POST.getlist('author_list')
        new_book_obj = models.Book.objects.create(name=new_name,
                                                  publish_date=new_date,
                                                  price=new_price,
                                                  publish_id=new_publish_id)
        new_book_obj.authors.set(author_list)
        return redirect('InfoBook')
    publish_list = models.Publish.objects.all()
    author_list = models.Author.objects.all()

    return render(request, "add_book.html", {"publish_list": publish_list, "author_list": author_list})


@judge
def info_book(request, *args):
    book_list = models.Book.objects.all()
    # name, time_now = args
    return render(request, "info_book.html", {"book_list": book_list})


def change_book(request, change_id):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        new_price = request.POST.get('new_price')
        new_author_list = request.POST.getlist('new_author')
        new_publish_date = request.POST.get('new_publish_date')
        new_publish = request.POST.get('new_publish')
        new_book_obj = models.Book.objects.filter(id=change_id).first()  # 多对多表obj
        models.Book.objects.filter(id=change_id).update(name=new_name,
                                                        price=new_price,
                                                        publish_date=new_publish_date,
                                                        publish_id=new_publish)
        new_book_obj.authors.set(new_author_list)
        return redirect('InfoBook')
    book_obj = models.Book.objects.get(id=change_id)
    author_list = models.Author.objects.all()
    publish_list = models.Publish.objects.all()
    return render(request, "change_book.html", {"book_obj": book_obj,
                                                "author_list": author_list, "publish_list": publish_list})


def delete_book(request, delete_id):
    models.Book.objects.get(id=delete_id).delete()
    return redirect("InfoBook")


#######################  ajax  ####################################


def my_ajax(request):
    return render(request, "my_ajax.html")


def a(request):
    return HttpResponse("666")


def b(request):
    q = request.POST.get("a")
    w = request.POST.get("b")
    res = int(q) + int(w)
    return HttpResponse(str(res))


def c(request):
    import json
    name = request.POST.get("name")
    pwd = request.POST.get("pwd")

    user_obj = models.Login.objects.filter(name=name, pwd=pwd).first()

    ret = {"user": None, "msg": None}
    if user_obj:
        ret["user"] = user_obj.name
    else:
        ret["msg"] = "有误"
    return HttpResponse(json.dumps(ret, ensure_ascii=False))
