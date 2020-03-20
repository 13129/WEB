from django.shortcuts import render

from apps.blog.models import Tag, Blog
from .models import Ligthapp, Touristfp, Link


# Create your views here.
def sumall (request):  # 标签

	return render (request, "tags.html", locals ())
