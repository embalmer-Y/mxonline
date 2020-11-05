import json
import requests


def send_single_sms(apikey, code, mobile):
    # 发送单条短信
    url = "https://sms.yunpian.com/v2/sms/single_send.json"
    text = f"【重墨无痕】您的验证码是{code}。如非本人操作，请忽略本短信"

    r = requests.post(url, data={
        "apikey": apikey,
        "mobile": mobile,
        "text": text,
    })
    re_json = json.loads(r.text)
    return re_json


if __name__ == "__main__":
    res = send_single_sms('4e5ed86f6e52dd4663d4111e11f37a23', '123456', "19858120112")
    print(res.text)
    res_json = json.loads(res.text)
    code = res_json["code"]
    msg = res_json["msg"]
    if code == 0:
        print("发送成功")
    else:
        print(f"发送失败:{msg}")
