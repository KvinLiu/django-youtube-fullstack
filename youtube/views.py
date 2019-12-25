from django.shortcuts import render
from django.views.generic.base import View, HttpResponse

# Create your views here.
class Index(View):
    template = "index.html"
    def get(self, request):
        variable = "Hello World"
        return render(request, self.template, {'variable': variable})
        
class NewVideo(View):
    def get(self, request):
        pass
