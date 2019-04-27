from jd.utils.response_code import RETCODE
from django.utils.decorators import wraps
from django import http
from django.contrib.auth.decorators import login_required
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from users.models import User

class LoginRequiredMixin(object):
    """验证用户是否登录扩展"""

    @classmethod
    def as_view(cls, **initkwargs):
        # 自定义的as_view(), 调用继承链中下一个类的as_view()方法
        view = super().as_view(**initkwargs)
        # 判断用户是否登录
        return login_required(view)


def login_required_json(view_func):
    """
    判断用户是否登录的装饰器,并返回json
    :param view_func: 被装饰的视图函数
    :return: json 或 view_func
    """

    # 恢复view_func的名字和文档
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # 如果用户未登录,返回的json数据
        if not request.user.is_authenticated():
            return http.JsonResponse({'code': RETCODE.SESSIONERR, 'errmsg': '用户未登录'})
        else:
            # 如果用户登录,进入到view_func中
            return view_func(request, *args, **kwargs)

    return wrapper


class LoginRequiredJSONMixin(object):
    """验证用户是否登录并返回json的扩展类"""

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required_json(view)


def generate_verify_email_url(user):
    """
    生成邮箱验证链接
    :param user: 当前登录用户
    :return: verify_url
    """
    serializer = Serializer(settings.SECRET_KEY, expires_in=100)
    data = {"user_id": user.id, "email": user.email}
    token = serializer.dumps(data).decode()
    return token

def check_verify_email_token(token):
    """
    验证token并提取user
    :param token: 用户信息签名后的结果
    :return: user, None
    """
    serializer = Serializer(settings.SECRET_KEY, expires_in=100)
    data = serializer.loads(token)
    user_id = data.get("user_id")
    email = data.get("email")

    try:
        user = User.objects.get(id=user_id, email=email)
    except User.DoesNotExist:
        return None
    else:
        return user



