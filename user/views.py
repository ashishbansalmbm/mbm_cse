from django.shortcuts import render, redirect
from .forms import RegistrationForm,  UpdateUserForm, UpdateProfileFormNotVerified, UpdateProfileFormVerified
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils import six


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegistrationForm()
        for i in form:
            print(i)
    return render(request, 'registration/registration_form.html', {'form': form})


def home(request):
        return render(request, 'home/homepage.html')


def dashboard(request):
    return render(request, 'user/base.html')


def view_profile(request):
    context = {'user': request.user, 'profile': request.user.profile}
    return render(request, 'user/profile.html', context)


def update_profile(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if request.user.profile.verified:
            profile_form = UpdateProfileFormVerified(request.POST, request.FILES, instance=request.user.profile)
        else:
            profile_form = UpdateProfileFormNotVerified(request.POST, request.FILES, instance=request.user.profile)
        print(user_form.errors.as_data())
        print(profile_form.errors.as_data())
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


@group_required('Faculty')
def index_view(request):
        users = User.objects.raw(' select * from auth_user where id in (select user_id from user_profile where type="s")')
        return render(request, 'user/index.html', {'all_users': users})




