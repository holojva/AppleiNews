from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from news.models import User, Likes

# from .forms import NewsForm
from .forms import NewsModelForm, CommentaryModelForm, Commentaries
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
@login_required
@permission_required("user.is_staff", login_url="")
def create_view(request, *args, **kwargs) :
    # if request.method == "POST" and request.POST["article"] :
    form = NewsModelForm(request.POST or None)

    if form.is_valid() :
        data = form.save(commit=False)
        data.author = request.user
        print(data)
        data.save()
        form = NewsModelForm()
    # print(request.GET)
    # print(request.POST)
    return render(request, "forms.html", {"form": form})
@login_required
@permission_required("user.is_staff")
def edit_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    if request.method == "POST" :
        form = NewsModelForm(request.POST, instance=obj)
        if form.is_valid():
            edited_obj = form.save(commit=False)
            edited_obj.save()
            return HttpResponseRedirect(reverse("detail-news", args=[pk]))
    else:
        form = NewsModelForm(instance=obj)
    return render(request, "edit_news_form.html", {"single_object": obj, "form": form})

@login_required
@permission_required("user.is_staff")
def delete_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    obj.delete()
    return HttpResponseRedirect(reverse("index"))
@login_required
def commentary_view(request, pk):
    form = CommentaryModelForm(request.POST or None)
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404

    if form.is_valid():
        text = form.cleaned_data.get("text")
        user = request.user
        commentary_obj = Commentaries(user=user, text=text, date=timezone.now())
        commentary_obj.save()
        obj.commentary.add(commentary_obj)
        obj.save()
        return redirect(f"/news/{pk}")

    return render(request, "news/commentary.html", {"single_object": obj, "form": form})
@login_required
@permission_required("user.is_staff")
def commentary_edit_view(request, pk, pk2):
    try:
        obj = News.objects.get(id=pk)
        comm = Commentaries.objects.get(id=pk2)
    except News.DoesNotExist:
        raise Http404
    if request.method == "POST" :
        form = CommentaryModelForm(request.POST, instance=comm)
        if form.is_valid():
            edited_obj = form.save(commit=False)
            edited_obj.date = timezone.now()
            edited_obj.save()
            return redirect(f"/news/{pk}")
    else:
        form = CommentaryModelForm(instance=comm)
    return render(request, "edit_commentary_form.html", {"single_object": obj, "form": form})

@login_required
@permission_required("user.is_staff")
def commentary_delete_view(request, pk, pk2):
    try:
        obj = News.objects.get(id=pk)
        comm = Commentaries.objects.get(id=pk2)
    except News.DoesNotExist:
        raise Http404
    print("aifon")
    comm.delete()
    return redirect(f"/news/{pk}")
@login_required
def likes_view(request, pk):
    try:
        obj = News.objects.get(id=pk)
    except News.DoesNotExist:
        raise Http404
    if request.method == "POST":
        user = request.user
        like_obj = Likes(user=user, like=True)
        like_obj.save()
        obj.likes.add(like_obj)
        obj.save()
    return HttpResponseRedirect(reverse("detail-news", args=[pk]))