from django.shortcuts import render, redirect

from .forms import RegistrationForm,  UpdateUserForm, UpdateProfileFormNotVerified, UpdateProfileFormVerified
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils import six
from communication.models import Notification
from django.contrib.auth.models import Group
from . models import NewsLetterSubscription
from django.http import HttpResponse
from django.contrib import messages


def group_required(group, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a group permission,
    redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group, )
        else:
            groups = group
        # First check if the user has the permission (even anon users)

        if user.groups.filter(name__in=groups).exists():
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            display = 1
            title = 'Thank You!!'
            message = 'Your registration was Successful Please Login to continue!!'
            context = {'display': display, 'message': message, 'title': title}
            return render(request, 'home/homepage.html', context)
        '''display = 1
        title = 'OOPS!!'
        message = 'THERE WAS AN ERROR!!
        context = {'display': display, 'message': message, 'title': title}'''
        return render(request, 'registration/registration_form.html', {'form': form})

    else:
        form = RegistrationForm()
    return render(request, 'registration/registration_form.html', {'form': form})



def home(request):
        notice = Notification.objects.raw('select * from communication_notification order by created_on desc ')
        return render(request, 'home/homepage.html', {'notice': notice})


def dashboard(request):
    user_group = Group.objects.get(name='User')
    user_group.user_set.add(request.user)
    if request.user.profile.verified is True:
        if request.user.profile.type is 'F':
            my_group = Group.objects.get(name='Faculty')
            my_group.user_set.add(request.user)
        elif request.user.profile.type is 'S':
            my_group = Group.objects.get(name='Student')
            my_group.user_set.add(request.user)
    return render(request, 'user/dashboard.html')


@permission_required('user.can_view_profile', login_url='user:register')
def view_profile(request):
    context = {'user': request.user, 'profile': request.user.profile}
    return render(request, 'user/profile.html', context)


@permission_required('user.can_update_profile', login_url="user:register")
def update_profile(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if request.user.profile.verified:
            profile_form = UpdateProfileFormVerified(request.POST, request.FILES, instance=request.user.profile)
        else:
            profile_form = UpdateProfileFormNotVerified(request.POST, request.FILES, instance=request.user.profile)
        #print(user_form.errors.as_data())
       # print(profile_form.errors.as_data())
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user:view_profile')

    else:
        if request.user.profile.verified:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileFormVerified(instance=request.user.profile)
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileFormNotVerified(instance=request.user.profile)
    profile = request.user.profile
    user = request.user
    context = {'user_form': user_form, 'profile_form': profile_form, 'profile': profile, 'user': user}
    return render(request, 'user/update_profile.html', context)


def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST['EMAIL']
        entry = NewsLetterSubscription()
        try:
            entry.email = email
            entry.save()
            display = 1
            title = 'Thank You!!'
            message = 'Your Subscription Was Successful!!'
            context = {'display': display, 'message': message, 'title': title}
            return render(request, 'home/homepage.html', context)
        except:
            display = 1
            title = 'Thank You For Your Keen Interest!!'
            message = 'You have already been subscribed!!'
            context = {'display':display, 'message':message, 'title':title}
            return render(request, 'home/homepage.html', context)















