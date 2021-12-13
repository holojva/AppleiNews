from django.shortcuts import render
from django.http import HttpResponse, Http404

# from .forms import NewsForm
from .forms import NewsModelForm
from news.models import News

# Create your views here.
def index(request, *args, **kwargs) :
    qs = News.objects.all()
    context = {"news_list": qs}
    return render(request, "index.html", context)

def detail_view(request, *args, **kwargs) :
    try:
        obj = News.objects.get(id=kwargs["pk"])
    except News.DoesNotExist :
        raise Http404
        
    print(request.POST)
    print(request.GET)
    print(request.method == "POST")
    print(request.method == "GET")
    return render(request, "news/detail.html", {"single_object": obj})
def create_view(request, *args, **kwargs) :
    # if request.method == "POST" and request.POST["article"] :
    form = NewsModelForm(request.POST or None)

    if form.is_valid() :
        print(form.cleaned_data)
        data = form.cleaned_data
        News.objects.create(**data)
    # print(request.GET)
    # print(request.POST)
    return render(request, "forms.html", {"form": form})