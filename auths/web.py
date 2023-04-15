from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,HttpResponse
from django.urls import reverse,reverse_lazy
from datetime import datetime
from django.views.generic import CreateView,ListView,UpdateView,View,FormView,DeleteView,DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views import View
from auths import models
from auths.forms import PasswordForm, RoleForm, StaffForm,UserForm
import bcrypt
from auths.models import DefaultPassword, LoginLog, Role, User
from auths.models import Staff as Staffob
from ninja.errors import HttpError
from auths.auth_token import User as auth_user
from django.core.paginator import Paginator
from django.db.models import  Q


###class based view # second developer

class UpdateUserCvB(LoginRequiredMixin,UpdateView):
    redirect_next_name='next'
    login_url=reverse_lazy('auths:login')
    model=User
    form_class=UserForm
    template_name='auths/add_user.html'
    context_object_name='form'
    success_url=reverse_lazy('auths:staff-members')

    def post(self, request, **kwargs):
        request.POST = request.POST.copy()
        full_name=request.POST.get('full_name')
        role = request.POST.get('role')
        phone_number = request.POST.get('phone_number')
        Staffob.objects.filter(user_id=self.kwargs['pk']).update(phone_number=phone_number,role_id=role,full_name=full_name)
        return super(UpdateUserCvB, self).post(request, **kwargs)

class Auths:
    def __init__(self):
        pass

    def login(request):
        """Authenticate the user to the system, by checking given credentials"""
        if request.user.is_authenticated:
            if User.objects.filter(id=request.user.id).exists():
                login_log = LoginLog.objects.create(created_by=request.user)
                login_log.save()
                if "next_page" in request.session:
                    path = request.session["next_page"]
                    return redirect(path)
                return redirect("/dashboard")
            if "next_page" in request.session:
                path = request.session["next_page"]
                return redirect(path)
            return redirect("index")

        elif request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = auth_user.get_user_by_username(request, username=username)
            if user:
                is_valid = bcrypt.checkpw(
                    password.encode("utf-8"), user.password.encode("utf-8")
                )
                if is_valid:
                    authenticate(username=username, password=password)
                    if user.is_active:
                        if user.is_staff:
                            auth_login(request, user)
                            login_log = LoginLog.objects.create(created_by=request.user)
                            login_log.save()
                            if request.GET.get("path"):
                                return redirect(request.GET.get("path"))
                            return redirect("/")
                        message = "sorry your account is not an Admin Account, communicate with your Admin"
                        return render(request, "auths/login.html", {"message": message})

                    message = (
                        "sorry your account is inactive communicate with your Admin"
                    )
                    return render(request, "auths/login.html", {"message": message})
                message = "Incorrect Username or Password"
                return render(request, "auths/login.html", {"message": message})
            message = "Incorrect Username or Password"
            return render(request, "auths/login.html", {"message": message})
        if request.GET.get("next") != None:
            request.session["next_page"] = request.GET.get("next")
            return render(
                request, "auths/login.html", {"path": request.GET.get("next")}
            )
        return render(request, "auths/login.html")

    def logout(request):
        """logout the user destroy user session"""
        log = LoginLog.objects.filter(created_by=request.user).order_by("-created_on")[
            0
        ]
        logout_log = LoginLog.objects.filter(created_by=request.user, id=log.id).update(
            logout_time=datetime.now()
        )
        # builtin function for session destroy
        auth_logout(request)
        if "next_page" in request.session:
            del request.session["next_page"]
        return redirect("/")

    def set_default_password(request):
        """set default password to be used as default for all added staffs"""
        template_name = "auths/add_password.html"
        if request.method == "POST":
            password_form = PasswordForm(request.POST or None)
            if password_form.is_valid():
                password = DefaultPassword.objects.create(
                    password=password_form.cleaned_data["password"]
                )
                password.save()
                return render(
                    request,
                    template_name,
                    {"password": Auths.get_default_password(request)},
                )
        return render(
            request, template_name, {"password": Auths.get_default_password(request)}
        )

    def get_default_password(request):
        """Get (default) password"""
        password = DefaultPassword.objects.filter(is_active=True).order_by(
            "-created_on"
        )
        if password:
            return password[0].password
        else:
            return "There was no Default Password"


class Staff:
    def __init__(self):
        pass

    def create_user(request):
        """Add user to the system"""
        template_name = "auths/add_user.html"
        header = 'Add Staff'
        if request.method == "POST":
            user_form = UserForm(request.POST or None)
            if user_form.is_valid():
                password = Auths.get_default_password(request)
                hash_password = bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()
                )
                role_id=request.POST.get('role')

                hashed_password = hash_password.decode("utf8")
                if models.Staff.objects.filter(phone_number=request.POST.get('phone_number')).exists():
                    message = "User with Entered username Exists"
                    return render(
                        request, template_name, {"roles": roles, "message": message,'header':header}
                    )

                user = models.User.objects.create(
                    password=hashed_password,
                    username=staff_form.cleaned_data["username"],
                    is_staff=request.POST.get('is_staff'),
                    is_superuser=request.POST.get('is_superuser'),
                    is_active=request.POST.get('is_active'),
                    email=request.POST.get('email'),
                )
                user.save()
                staff = models.Staff.objects.create(
                    user=user,
                    full_name=staff_form.cleaned_data["full_name"],
                    role=role,
                    phone_number=staff_form.cleaned_data["phone_number"],
                )
                staff.save()
                if staff:
                    return Staff.get_staffs(request)
        user_form = UserForm()
        return render(request, template_name, {"form": user_form,'header':header})


    def create_staff(request):
        """Add staff to the system"""
        template_name = "auths/add_staff.html"

        if request.method == "POST":
            staff_form = StaffForm(request.POST or None)
            if staff_form.is_valid():
                password = Auths.get_default_password(request)
                hash_password = bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()
                )
                role = models.Role.objects.filter(
                    role_name=staff_form.cleaned_data["role"]
                )
                if role:
                    role = role[0]
                else:
                    role = None
                #is_staff = False
                if role.role_name in [
                    "Admin",
                    "admin",
                    "Administrator",
                    "administrator",
                ]:
                    is_staff = True
                hashed_password = hash_password.decode("utf8")
                existing_user = models.User.objects.filter(
                    username=staff_form.cleaned_data["phone_number"]
                )
                if existing_user:
                    roles = models.Role.objects.filter(is_active=True).order_by(
                        "role_name"
                    )
                    message = "User with Entered username Exists"
                    return render(
                        request, template_name, {"roles": roles, "message": message}
                    )
                user = models.User.objects.create(
                    password=hashed_password,
                    username=staff_form.cleaned_data["phone_number"],
                    is_staff=is_staff,
                )
                user.save()
                staff = models.Staff.objects.create(
                    user=user,
                    full_name=staff_form.cleaned_data["full_name"],
                    role=role,
                    phone_number=staff_form.cleaned_data["phone_number"],
                )
                staff.save()
                if staff:
                    return Staff.get_staffs(request)
        roles = models.Role.objects.filter(is_active=True).order_by("role_name")
        return render(request, template_name, {"roles": roles})

    def edit_staff(request, staff_id):
        """edit staff to the system"""
        template_name = "auths/add_staff.html"
        if request.method == "POST":
            staff_form = StaffForm(request.POST or None)
            if staff_form.is_valid():
                role = models.Role.objects.filter(
                    role_name=staff_form.cleaned_data["role"]
                )
                models.Staff.objects.filter(id=staff_id).update(
                    full_name=staff_form.cleaned_data["full_name"],
                    role=role[0],
                    phone_number=staff_form.cleaned_data["phone_number"],
                )
                return redirect("/staff-members")
        form = models.Staff.objects.get(id=staff_id)
        roles = models.Role.objects.filter(is_active=True).order_by("role_name")
        return render(request, template_name, {"roles": roles, "form": form})

    def get_staffs(request):
        """get (display) all staffs"""
        template_name = "auths/staffs.html"
        header = ' Staff/User'
        #try:
        staffs = models.Staff.objects.filter(is_active=True).order_by("-created_on")
        paginated_staffs = Paginator(staffs, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_staffs.get_page(page_number)
        return render(request, template_name, {"page_obj": staffs,'header':header})
        #except:
        raise HttpError(500, "Internal Server Error")

    def get_staffs_inactive(request):
        """get (display) all staffs"""
        template_name = "auths/staffs.html"
        header='Inactive Staff'
        #try:
        staffs = models.Staff.objects.filter(is_active=False).order_by("-created_on")
        paginated_staffs = Paginator(staffs, 10)
        page_number = request.GET.get("page")
        page_obj = paginated_staffs.get_page(page_number)
        return render(request, template_name, {"page_obj": staffs,'header':header})
        #except:
        raise HttpError(500, "Internal Server Error")



    def delete_staff(request, staff_id):
        """delete staff member by staff id"""
        template_name = "auths/staffs.html"
        staff = models.Staff.objects.filter(~Q(user=request.user)&Q(id=staff_id))
        if not staff.exists():
            staffs = models.Staff.objects.filter(is_active=True).order_by("-created_on")
            paginated_staffs = Paginator(staffs, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_staffs.get_page(page_number)
            message = "Staff was already deleted"
            return render(
                request, template_name, {"page_obj": staffs, "message": message}
            )
        user=staff.first()
        if user.is_active:
            user.is_active=False
            user.save()
        else:
            user.is_active=True
            user.save()
        models.User.objects.filter(id=staff[0].user.id).update(is_active=False)
        return redirect("/staff-members")


class Role:
    def __init__(self):
        pass

    def add_role(request):
        """Add role to be assigned to staffs"""
        template_name = "auths/add_role.html"
        try:
            if request.method == "POST":
                role_form = RoleForm(request.POST or None)
                if role_form.is_valid():
                    if not  models.Role.objects.filter(role_name__iexact=request.POST.get('role_name')).exists():
                        role = models.Role.objects.create(
                            role_name=role_form.cleaned_data["role_name"]
                        )
                        role.save()
                    return redirect("/roles")

            return render(request, template_name)
        except:
            raise HttpError(500, "Internal Server Error")

    def get_roles(request):
        """get (display) all roles"""
        template_name = "auths/roles.html"
        header = 'Roles'
        try:
            roles = models.Role.objects.filter(is_active=True).order_by("role_name")
            paginated_roles = Paginator(roles, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_roles.get_page(page_number)
            return render(request, template_name, {"page_obj": page_obj,'header':header})
        except:
            raise HttpError(500, "internal Server Error")
    def get_roles_inactive(request):
        """get (display) all roles"""
        template_name = "auths/roles.html"
        header='Inactive Roles'
        try:
            roles = models.Role.objects.filter(is_active=False).order_by("role_name")
            paginated_roles = Paginator(roles, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_roles.get_page(page_number)
            return render(request, template_name, {"page_obj": page_obj,'header':header})
        except:
            raise HttpError(500, "internal Server Error")

    def edit_role(request, role_id):
        template_name = "auths/add_role.html"
        try:
            if request.method == "POST":
                role_form = RoleForm(request.POST or None)
                if role_form.is_valid():
                    role = models.Role.objects.filter(id=role_id).update(
                        role_name=role_form.cleaned_data["role_name"]
                    )
                    return redirect("/roles")
            form = models.Role.objects.get(id=role_id)
            return render(request, template_name, {"form": form})
        except:
            raise HttpError(500, "Internal Server Error")

    def delete_role(request, role_id):
        """Delete Roles from the database"""
        template_name = "auths/roles.html"
        role = models.Role.objects.filter(id=role_id)
        if not role.exists():
            roles = models.Role.objects.filter(is_active=True).order_by("role_name")
            paginated_roles = Paginator(roles, 10)
            page_number = request.GET.get("page")
            page_obj = paginated_roles.get_page(page_number)
            message = "Role was already Deleted"
            return render(
                request, template_name, {"page_obj": page_obj, "message": message}
            )
        role.update(is_active=False)
        return redirect("/roles")
