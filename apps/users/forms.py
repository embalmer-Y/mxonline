from django import forms

from MxOnline.settings import REDIS_HOST, REDIS_PORT
from captcha.fields import CaptchaField
import redis
from apps.users.models import UserProfile


class UpdateMobileForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, max_length=6, min_length=6)

    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))

        if redis_code != code:
            raise forms.ValidationError("验证码不正确")
        else:
            return self.cleaned_data



class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

    def clean(self):
        # pwd1 = self.cleaned_data['password1']
        # pwd2 = self.cleaned_data['password2']
        pwd1 = self.cleaned_data["password1"]
        pwd2 = self.cleaned_data["password2"]
        if pwd1 != pwd2:
            raise forms.ValidationError('密码不一致')
        return self.cleaned_data


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nick_name", 'gender', 'birthday', 'address']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]


# 表单验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=4)


class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, max_length=6, min_length=6)
    password = forms.CharField(required=True)

    def clean_mobile(self):
        mobile = self.data.get("mobile")
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError("该手机号已注册")
        else:
            return mobile

    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))

        if redis_code != code:
            raise forms.ValidationError("验证码不正确")
        else:
            return code


class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, max_length=6, min_length=6)

    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))

        if redis_code != code:
            raise forms.ValidationError("验证码不正确")
        else:
            return self.cleaned_data

    # def clean(self):
    #     mobile = self.cleaned_data["mobile"]
    #     code = self.cleaned_data["code"]
    #
    #     r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
    #     redis_code = r.get(str(mobile))
    #
    #     if redis_code == code:
    #         raise forms.ValidationError("验证码不正确")
    #     else:
    #         return self.cleaned_data
