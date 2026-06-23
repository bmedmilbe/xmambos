from django.db import connection
from django.shortcuts import render
from django.http import HttpResponse


def api_home(request):
    return HttpResponse("CMS is working! Gateway connection established.")
    # """
    # Renders the technical landing page for the each Tenant API.
    # """

    # # connection.schema_name is automatically set by django-tenants middleware
    # schema = connection.schema_name
    # print("print:", schema)
    # if schema == "public":
    #     return render(request, "public/index.html")

    # # Try to find a template for the specific tenant, fallback to a default
    # template_name = f"tenants/{schema}/index.html"

    # return render(request, template_name, {"tenant_name": schema.upper()})
