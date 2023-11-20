from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Profile,Meep
from .forms import MeepForm,SignUpForm,ProfilePicForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash


def home(request):
    meeps = None
    if request.user.is_authenticated:
        form=MeepForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep=form.save(commit=False)
                meep.user=request.user
                meep.save()
                messages.success(request,("You meep has been posted!"))
                return redirect('home') 

        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {'meeps': meeps,"form":form})
    else:
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {'meeps': meeps})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request,'profile_list.html',{"profiles":profiles})
    else:
        messages.success(request,("You must log in"))
        return redirect('home')
    
def unfollow(request, pk):
    if request.user.is_authenticated:
        try:
            # Get the profile to unfollow
            profile = get_object_or_404(Profile, user_id=pk)
            
            # Unfollow the user
            request.user.profile.follows.remove(profile)
            
            # Save our profile
            request.user.profile.save()

            # Return message
            messages.success(request, f"You have successfully unfollowed {profile.user.username}")
            return redirect(request.META.get("HTTP_REFERER"))
        except Profile.DoesNotExist:
            messages.success(request, "Profile not found")
            return redirect('home')
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')
def follow(request, pk):
    if request.user.is_authenticated:
        try:
            # Get the profile to unfollow
            profile = get_object_or_404(Profile, user_id=pk)
            
            # Unfollow the user
            request.user.profile.follows.add(profile)
            
            # Save our profile
            request.user.profile.save()

            # Return message
            messages.success(request, f"You have successfully Followed {profile.user.username}")
            return redirect(request.META.get("HTTP_REFERER"))
        
        except Profile.DoesNotExist:
            messages.success(request, "Profile not found")
            return redirect('home')
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')


def profile(request,pk):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user_id=pk)
        meeps=Meep.objects.filter(user_id=pk).order_by("-created_at")
        #Post form logic
        if request.method == "POST":
            #Get current user id
            current_user_profile=request.user.profile
            #Get form data
            action=request.POST['follow']
            if action =="unfollow":
                current_user_profile.follows.remove(profile)
            elif action=="follow":
                current_user_profile.follows.add(profile)
            #Save the profile
            current_user_profile.save()

        return render(request,"profile.html",{"profile":profile,"meeps":meeps})
    else:
        messages.success(request,("You must log in"))
        return redirect('home')
    
def followers(request,pk):
    if request.user.is_authenticated:
        if request.user.id==pk:

            profiles = Profile.objects.get(user_id=pk)
            return render(request,'followers.html',{"profiles":profiles})
        else:
            messages.success(request,("That is not your profile page..."))
            return redirect('home')

    else:
        messages.success(request,("You must log in"))
        return redirect('home')
    
def follows(request,pk):
    if request.user.is_authenticated:
        if request.user.id==pk:

            profiles = Profile.objects.get(user_id=pk)
            return render(request,'follows.html',{"profiles":profiles})
        else:
            messages.success(request,("That is not your profile page..."))
            return redirect('home')

    else:
        messages.success(request,("You must log in"))
        return redirect('home')

def login_user(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("Logged in!"))
            return redirect('home')
        else:
            messages.success(request,("Wrong name or password..!"))
            return render(request,"login.html",{})
    else:
        return render(request,"login.html",{})

def logout_user(request):
    logout(request)
    messages.success(request,("You have been log out."))
    return redirect('home')

def register_user(request):
    form = SignUpForm() 
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            #first_name=form.cleaned_data['first_name']
            #last_name=form.cleaned_data['last_name']
            #email=form.cleaned_data['email']
            
            #Login user
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You have succesfully register."))
            return redirect('home')
    
    return render(request,"register.html",{'form':form})

def update_user(request):
    current_user = request.user
    user_form = SignUpForm(request.POST or None, instance=current_user)
    profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=current_user.profile)

    if request.method == 'POST' and user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()

        update_session_auth_hash(request, current_user)
        messages.success(request, "Your profile has been updated.")
        return redirect('home')

    return render(request, "update_user.html", {"user_form": user_form, "profile_form": profile_form})
    

def meep_like(request,pk):
    if request.user.is_authenticated:
        meep=get_object_or_404(Meep, id=pk)
        if meep.likes.filter(id=request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    
    else:
        messages.success(request,("You Must Be Logged In To View That Page."))
        return redirect('home')
    
def meep_show(request,pk):
    meep=get_object_or_404(Meep, id=pk)
    if meep:
        return render(request,"show_meep.html",{"meep":meep})
    else:
        messages.success(request,("That Meep Does Not Exist..."))
        return redirect('home')
    

def delete_meep(request,pk):
    if request.user.is_authenticated:
        meep=get_object_or_404(Meep, id=pk)
        #Check if you own the meep
        if request.user.username==meep.user.username:
            #Delete the meep
            meep.delete()
            messages.success(request,("The Meep Has Been Deleted..."))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request,("You dont own that meep..."))
            return redirect('home')
    else:
        messages.success(request,("Please Log In To Continue..."))
        return redirect(request.META.get("HTTP_REFERER"))
    
def edit_meep(request,pk):
    if request.user.is_authenticated:
        meep=get_object_or_404(Meep, id=pk)
        #check if you own the meep
        if request.user.username==meep.user.username:
            form=MeepForm(request.POST or None,instance=meep)
            if request.method == "POST":
                if form.is_valid():
                    meep=form.save(commit=False)
                    meep.user=request.user
                    meep.save()
                    messages.success(request,("You meep has been Updated!"))
                    return redirect('home') 
            else:
                return render(request, "edit_meep.html", {"form":form, "meep": meep })
        else:
            messages.success(request,("You dont own that meep..."))
            return redirect('home')
    else:
        messages.success(request,("Please Log In To Continue..."))
        return redirect('home')
    


def search(request):
    if request.method=="POST":
        #grab the word
        search=request.POST['search']
        #search the database
        searched=Meep.objects.filter(body__contains=search)
        return render(request,'search.html',{'search':search,'searched':searched})
    else:
        return render(request,'search.html',{})
    
def search_user(request):
    if request.method=="POST":
        #grab the word
        search=request.POST['search']
        #search the database
        searched=User.objects.filter(username__contains=search)
        return render(request,'search_user.html',{'search':search,'searched':searched})
    else:
        return render(request,'search_user.html',{})