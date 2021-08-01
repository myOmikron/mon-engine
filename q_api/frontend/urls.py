from django.urls import path

import api.views
from description import models
from frontend.views import *

urlpatterns = [
    path("login", Login.as_view()),
    path("logout", Logout.as_view()),
    path("", DashboardView.as_view()),

    # Model specific views that can use the API are added with the function below
]


def generate_url_paths(api_class, model_class):
    name = model_class.__name__.lower()
    params = {"api_class": api_class, "model_class": model_class}
    [urlpatterns.append(x) for x in [
        path(f"declaration/{name}/", DeclarationTemplateIndex.as_view(), params),
        path(f"declaration/{name}/create", DeclarationTemplateCreate.as_view(), params),
        path(f"declaration/{name}/update/<str:sid>", DeclarationTemplateUpdate.as_view(), params),
        path(f"declaration/{name}/delete/<str:sid>", DeclarationTemplateDelete.as_view(), params),
    ]]


generate_url_paths(api.views.GlobalVariableView, models.GlobalVariable)
generate_url_paths(api.views.CheckView, models.Check)
