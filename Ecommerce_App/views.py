from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from . import models
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.


def admin_login_view(request):
    return render(request, "admin_template/admin_login.html", {})


def admin_logout_process(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return HttpResponseRedirect(reverse('admin_login'))


@login_required(login_url="/admin_login/")
def admin_dashboard_view(request):
    return render(request, "admin_template/admin_dashboard.html")


def admin_login_process(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request=request, username=username, password=password)
    if user is not None:
        login(request=request, user=user)
        return HttpResponseRedirect(reverse("admin_dashboard"))
    else:
        messages.error(request, "Error in Login! Invalid Login Details!")
        return HttpResponseRedirect(reverse("admin_login"))

# Category Views


class categories_list_view(ListView):
    model = models.Categories
    template_name = "admin_template/category_list.html"


class category_create_view(SuccessMessageMixin, CreateView):
    model = models.Categories
    success_message = "Category added successfully!!!"
    fields = "__all__"
    template_name = "admin_template/category_create.html"


class category_update_view(SuccessMessageMixin, UpdateView):
    model = models.Categories
    success_message = "Category Updated successfully!!!"
    fields = "__all__"
    template_name = "admin_template/category_update.html"

# Subcategory Views


class sub_categories_list_view(ListView):
    model = models.SubCategories
    template_name = "admin_template/subcategory_list.html"


class sub_category_create_view(SuccessMessageMixin, CreateView):
    model = models.SubCategories
    success_message = "Sub Category added successfully!!!"
    fields = "__all__"
    template_name = "admin_template/subcategory_create.html"


class sub_category_update_view(SuccessMessageMixin, UpdateView):
    model = models.SubCategories
    success_message = "Sub Category Updated successfully!!!"
    fields = "__all__"
    template_name = "admin_template/subcategory_update.html"


class merchant_user_create_view(SuccessMessageMixin, CreateView):
    template_name = "admin_template/merchant_create.html"
    model = models.CustomUser
    fields = ["first_name", "last_name", "email", "username", "password"]

    def form_valid(self, form):
        # saving Custom user object for merchant user
        user = form.save(commit=False)
        user.is_active = True
        user.user_type = 3
        user.set_password(form.cleaned_data["password"])
        user.save()

        # saving merchant user
        profile_pic = self.request.FILES["profile_pic"]
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        user.merchantuser.profile_pic = profile_pic_url
        user.merchantuser.company_name = self.request.POST.get("company_name")
        user.merchantuser.gst_details = self.request.POST.get("gst_details")
        user.merchantuser.address = self.request.POST.get("address")
        user.save()
        messages.success(self.request, "Merchant user Added successfully")
        return HttpResponseRedirect(reverse("merchant_list"))


class merchant_user_list_view(ListView):
    model = models.MerchantUser
    template_name = "admin_template/merchant_list.html"


class merchant_user_update_view(SuccessMessageMixin, UpdateView):
    model = models.CustomUser
    template_name = "admin_template/merchant_update.html"
    fields = ["first_name", "last_name", "email", "username", "password"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model = models.MerchantUser.objects.get(auth_user_id=self.object.pk)
        context["merchantuser"] = model
        return context

    def form_valid(self, form):
        # saving Custom user object for merchant user
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()

        # saving merchant user update
        merchantuser = models.MerchantUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic", False):
            profile_pic = self.request.FILES["profile_pic"]
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            merchantuser.profile_pic = profile_pic_url

        merchantuser.company_name = self.request.POST.get("company_name")
        merchantuser.gst_details = self.request.POST.get("gst_details")
        merchantuser.address = self.request.POST.get("address")
        merchantuser.save()
        messages.success(self.request, "Merchant user updated successfully")
        return HttpResponseRedirect(reverse("merchant_list"))
