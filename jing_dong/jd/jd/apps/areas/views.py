from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from areas.models import Area
from jd.utils.response_code import RETCODE
import logging

logger = logging.getLogger("django")
# Create your views here.

class AreasView(View):
    """返回省市区数据"""
    def get(self, request):
        area_id = request.GET.get("area_id")
        if not area_id:
            # 返回所有省数据
            try:
                province_model_list = Area.objects.filter(parent_id__isnull=True)
                # 序列化省级数据
                province_list = list()
                for province in  province_model_list:
                    province_list.append({"id": province.id, "name": province.name})

            except Exception as e:
                logger.error(e)
                return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '省份数据错误'})
            else:
                # 响应省份数据
                return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'province_list': province_list})

        else:
            try:
                # 某个省/市返回所有市/区
                parent = Area.objects.get(id=area_id)
                son_model = parent.subs.all()
                subs = list()
                for son in son_model:
                    subs.append({"id":son.id, "name": son.name})
                sub_data = {"id": parent.id, "name": parent.name, "subs": subs}
            except Exception as e:
                logger.error(e)
                return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '市数据错误'})
            else:
                return JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'sub_data': sub_data})









