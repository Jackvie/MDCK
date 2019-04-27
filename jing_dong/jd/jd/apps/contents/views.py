from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
# Create your views here.

class IndexView(View):
    """首页"""
    def get(self, request):
        """返回首页"""
        return render(request, "index.html")