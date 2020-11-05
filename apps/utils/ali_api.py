from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from MxOnline import settings
import json


def send_single_sms(code, mobile):
    dict_param = {"code": code}
    client = AcsClient(settings.AccessKeyId, settings.AccessKeySecret, settings.RegionId)

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version("2017-05-25")
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', mobile)
    request.add_query_param('SignName', settings.SignName)
    request.add_query_param('TemplateCode', settings.TemplateCode)
    request.add_query_param('TemplateParam', str(dict_param))

    response = client.do_action_with_exception(request)
    re_json = json.loads(str(response, encoding="utf-8"))
    # python2:  print(response)
    return re_json


if __name__ == "__main__":
    mobile = ""
    print(send_single_sms("123445", mobile))
