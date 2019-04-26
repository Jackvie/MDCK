from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


def generate_eccess_token(openid):
    # serializer = Serializer(秘钥, 有效期秒)
    serializer = Serializer(settings.SECRET_KEY, 300)
    data = {"openid": openid}

    token = serializer.dumps(data)
    return token.decode()

def check_access_token(openid):
    serializer = Serializer(settings.SECRET_KEY, 300)
    return serializer.loads(openid).get("openid")
