from django.shortcuts import render
from django.views.generic.base import View, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, RegisterForm, NewVideoForm
from .models import Video, Comment

import string, random

# Create your views here.
class HomeView(View):
    template = "index.html"
    def get(self, request):
        most_recent_videos = Video.objects.order_by('-datetime')[:10]
        return render(request, self.template, {'most_recent_videos': most_recent_videos})
        
class NewVideo(View):
    template = "youtube/newvideo.html"
    def get(self, request):
        if request.user.is_authenticated == False:
            # return HttpResponse("You have to be logged in, in order to add viedos")
            return HttpResponseRedirect('/')
            
        form = NewVideoForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = NewVideoForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']

            random_char = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            path = random_char + file.name
            new_video = Video(title=title,
                              description=description,
                              path=path,
                              user=request.user)
            new_video.save()
            # Redirect to detail view page
            return HttpResponseRedirect('/video/{}'.format(new_video.id))
        else:
            return HttpResponse("Your Form is not valid. Go back and try again")

class VideoView(View):
    template = "youtube/videodetail.html"
    def get(self, request, id):
        video_by_id = Video.objects.get(id=id)
        context = {'video': video_by_id}
        return render(request, self.template, context)
class LoginView(View):
    template = "youtube/login.html"
    def get(self, request):
        if request.user.is_authenticated:
            print("Already Logged in, Redirecting")
            # logout(request)
            return HttpResponseRedirect('/')
        else:
            form = LoginForm()
            return render(request, self.template, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            # create a User account
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # create a new entry in table 'logs'
                login(request, user)
                print("Success Login!")
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('login')
        return HttpResponse("Something is going wrong")

class RegisterView(View):
    template = "youtube/register.html"
    def get(self, request):
        if request.user.is_authenticated:
            print("Already Logged In, Redirecting....")
            return HttpResponseRedirect('/')
        form = RegisterForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        # pass filled out Html-Form to RegisterForm()
        form = RegisterForm(request.POST)
        if form.is_valid():
            # create a User account
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            new_user.save()
            return HttpResponseRedirect('login')
        return HttpResponse("This is a register post response")
