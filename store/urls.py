from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path("", views.home, name="dashboard"),
    path("home/", views.home, name="home"),

    # Auth
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register, name="register"),
    

    # Pages from template
    path("profile/", views.profile, name="profile"),
    path("tables-data/", views.tables_data, name="tables-data"),

    path("charts/apexcharts/", views.charts_apexcharts, name="charts-apexcharts"),
    path("charts/chartjs/", views.charts_chartjs, name="charts-chartjs"),

    path("forms/elements/", views.forms_elements, name="forms-elements"),
    path("forms/validation/", views.forms_validation, name="forms-validation"),

    # Store CRUD
    path("stores/add/", views.add_store, name="add_store"),
    path("stores/", views.store_list, name="store_list"),
    path("stores/edit/<int:id>/", views.store_edit, name="store_edit"),
    path("stores/delete/<int:id>/", views.store_delete, name="store_delete"),

    # Product CRUD
    path("products/", views.product_list, name="product_list"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/edit/<int:id>/", views.edit_product, name="product_edit"),
    path("products/delete/<int:id>/", views.delete_product, name="product_delete"),
]
    