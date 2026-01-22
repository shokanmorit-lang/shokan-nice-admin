from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

from .models import StoreModel, Product
from .forms import StoreForm, ProductForm, RegisterForm


# -------- Authorization Helper --------
def is_admin(user):
    return user.is_staff


# ---------------- Dashboard ----------------
@login_required
def home(request):
    return render(request, "store/dashboard.html")


# ---------------- Authentication ----------------
def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    next_url = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)

            # Secure Redirect (Prevent Open Redirect)
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)

            return redirect("dashboard")

        messages.error(request, "اسم المستخدم أو كلمة المرور غير صحيحة.")

    return render(request, "store/pages-login.html", {"next": next_url})


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "تم إنشاء الحساب بنجاح. سجل دخولك الآن.")
            return redirect("login")
        messages.error(request, "تأكد من البيانات المدخلة.")

    return render(request, "store/pages-register.html", {"form": form})


# ---------------- Template Pages ----------------
@login_required
def profile(request):
    return render(request, "store/users-profile.html")


@login_required
def tables_data(request):
    return render(request, "store/tables-data.html")


@login_required
def charts_apexcharts(request):
    return render(request, "store/charts-apexcharts.html")


@login_required
def charts_chartjs(request):
    return render(request, "store/charts-chartjs.html")


@login_required
def forms_elements(request):
    return render(request, "store/forms-elements.html")


@login_required
def forms_validation(request):
    return render(request, "store/forms-validation.html")


# ---------------- Store CRUD ----------------
@login_required
@user_passes_test(is_admin)
def add_store(request):
    form = StoreForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "تمت إضافة المتجر بنجاح.")
        return redirect("store_list")
    return render(request, "store/add_store.html", {"form": form})


@login_required
def store_list(request):
    stores = StoreModel.objects.all()
    return render(request, "store/store_list.html", {"stores": stores})


@login_required
@user_passes_test(is_admin)
def store_edit(request, id):
    store = get_object_or_404(StoreModel, id=id)
    form = StoreForm(request.POST or None, request.FILES or None, instance=store)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "تم تعديل المتجر.")
        return redirect("store_list")
    return render(request, "store/store_form.html", {
        "form": form,
        "title": "Edit Store"
    })


@login_required
@user_passes_test(is_admin)
def store_delete(request, id):
    store = get_object_or_404(StoreModel, id=id)

    if request.method == "POST":
        store.delete()
        messages.success(request, "تم حذف المتجر.")
        return redirect("store_list")

    return render(request, "store/confirm_delete.html", {
        "obj": store,
        "cancel_url": "store_list"
    })


# ---------------- Product CRUD ----------------
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "store/product_list.html", {"products": products})


@login_required
@user_passes_test(is_admin)
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "تمت إضافة المنتج.")
        return redirect("product_list")
    return render(request, "store/add_product.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "تم تعديل المنتج.")
        return redirect("product_list")
    return render(request, "store/add_product.html", {
        "form": form,
        "is_edit": True
    })


@login_required
@user_passes_test(is_admin)
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        product.delete()
        messages.success(request, "تم حذف المنتج.")
        return redirect("product_list")
    return render(request, "store/confirm_delete.html", {
        "obj": product,
        "cancel_url": "product_list"
    })