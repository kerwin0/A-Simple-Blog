from django import forms
from book import models
from django.forms import widgets
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


class Myform(forms.Form):
    name = forms.CharField(min_length=4, max_length=12, label="用户名",
                           widget=widgets.TextInput(attrs={"class": "form-control"}),
                           error_messages={"required": "请正确输入用户名"})
    pwd = forms.CharField(label="密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                          error_messages={"required": "密码不能为空"})
    r_pwd = forms.CharField(label="确认密码", widget=widgets.PasswordInput(attrs={"class": "form-control"}),
                            error_messages={"required": "密码不能为空"})
    email = forms.EmailField(label="邮箱", widget=widgets.EmailInput(attrs={"class": "form-control"}),
                             error_messages={"required": "请正确输入邮箱"})

    def clean_name(self):
        val = self.cleaned_data.get("name")
        if val.isdigit():
            raise ValidationError("用户名不能是纯数字")
        elif models.Login.objects.filter(name=val):
            raise ValidationError("用户名已存在")
        else:
            return val

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        r_pwd = self.cleaned_data.get("r_pwd")
        if pwd and r_pwd and pwd != r_pwd:
            raise ValidationError("密码不一致")
        else:
            return self.cleaned_data
