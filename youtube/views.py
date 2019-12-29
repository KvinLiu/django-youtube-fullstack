from django.shortcuts import render
from django.views.generic.base import View, HttpResponse, HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User

# Create your views here.
class HomeView(View):
    template = "index.html"
    def get(self, request):
        variable = "Hello World"
        return render(request, self.template, {'variable': variable})
        
class NewVideo(View):
    template = "video.html"
    def get(self, request):
        variable = "this is awesome"
        return render(request, self.template, {'variable': variable})

class LoginView(View):
    template = "youtube/login.html"
    def get(self, request):
        form = LoginForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        print('Hello This is a Post')
        return HttpResponse("This is a login post response")

class RegisterView(View):
    template = "youtube/register.html"
    def get(self, request):
        form = RegisterForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        # pass filled out Html-Form to RegisterForm()
        form = RegisterForm(request.POST)
        if form.is_valid():
            # create a User account
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            check_email = User.objects.get(email=email)
            if not check_email:
                return "That email is already taken"
            password = form.cleaned_data['password']
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            return HttpResponseRedirect('login')
        return HttpResponse("This is a register post response")
