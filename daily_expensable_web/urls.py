from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("core.urls")),
    path("daily-expensable/", include("calculator.urls")),
    path("fixed-costs/", include("fixed_costs.urls")),
    path("admin/", admin.site.urls),
]
