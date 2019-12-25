from django.shortcuts import render
from .models import UserBlog
from django.shortcuts import HttpResponseRedirect, get_object_or_404, HttpResponse
from .forms import CreateNewBlog
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from rest_framework.response import Response

from .serializers import UserBlogListSerializer, UserBlogDetailSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# def blog_list(request):
#     blogs = UserBlog.objects.all()
#
#     paginator = Paginator(blogs,3)  # here we divide our BULK blogs list to pages using Paginator, For demo, will display only 3 blogs per page.
#     print(request.GET)
#     page = request.GET.get("page")  # we are reading the extra parameter that will be passed on to the url like ` ?page=2 `
#     blogs = paginator.get_page(page)  # then we return only the sall chunk of blogs that will be on a specific page number instead of BULK blogs
#
#     context = {"blogs": blogs, "title": "Posted Blogs"}
#     return render(request, "blog/list.html", context=context)

# def blog_detail(request, slug):
#     blog = UserBlog.objects.get(slug=slug)
#     context = {"Blog": blog, "title": "BloG detail"}
#     return render(request, "blog/detail.html", context)

# @login_required(login_url="/login/")
# def blog_delete(request, slug):
#     selectedblog = UserBlog.objects.get(slug=slug)
#
#     context = {"blog": selectedblog}
#
#     if request.method == "GET":
#         return render(request, "blog/userblog_confirm_delete.html", context=context)
#     elif request.method == "POST":
#         if request.user.is_superuser and request.user == selectedblog.user:
#             selectedblog.delete()
#             messages.warning(request, "Blog `{}` has been successfully deleted.".format(selectedblog.title))
#             return HttpResponseRedirect("/blogs/")
#         else:
#             context["error"] = "`Blog may not belong to you` or `you are not a superuser.`"
#             return render(request, "blog/error.html", context=context)

class BlogListView(ListView):
    paginate_by = 3
    queryset = UserBlog.objects.values("title", "user", "timestamp", "slug", "image")


class BlogDetailView(DetailView):
    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(UserBlog, slug=slug)
        return obj


class BlogDelete(LoginRequiredMixin, DeleteView):
    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(UserBlog, slug=slug)
        return obj

    def get_success_url(self):
        return reverse("blogapp:blog_list")

    def delete(self, request, *args, **kwargs):
        self.selectedblog = self.get_object()
        if request.user.is_superuser and request.user == self.selectedblog.user:
            self.selectedblog.delete()
            messages.warning(request, "Blog `{}` has been successfully deleted.".format(self.selectedblog.title))
            return HttpResponseRedirect(self.get_success_url())
        else:
            context = {"error": "`Blog may not belong to you` or `you are not a superuser.`"}
            return render(request, "blog/error.html", context=context)


@login_required(login_url="/login/")
def blog_create(request):
    form = CreateNewBlog(request.POST or None, request.FILES or None)
    title = "Add Blog"
    context = {"form": form, "title": title}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Blog has been create successfully.")
        return HttpResponseRedirect("/blogs/")

    return render(request, "blog/form.html", context)


# class BlogCreateView(CreateView):
#     form_class = CreateNewBlog
#     template_name = "blog/form.html"
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             if request.user.is_authenticated:
#                 instance = form.save(commit=False)
#                 instance.user = request.user
#                 instance.save()
#                 messages.success(request,"Blog has been created successfully.")
#             else:
#                 return HttpResponseRedirect(reverse("blogapp:blog_create"))
#             form = CreateNewBlog()
#         else:
#             messages.warning(request,"Invalid Blog")
#         context = {"form":form, "title":"Add Blog"}
#         return render(request, "blog/form.html", context)

@csrf_exempt
@api_view(["GET", "POST"])
def blogapilist(request):
    if request.method == "GET":
        queryset = UserBlog.objects.all()
        serializer = UserBlogListSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserBlogListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(["GET", "PUT", "DELETE"])
def blogapidetail(request, id):
    try:
        instance = UserBlog.objects.get(id=id)
    except UserBlog.DoesNotExist as E:
        return JsonResponse({"error": "No data found for the given ID."}, status=404)

    if request.method == "GET":
        serializer = UserBlogDetailSerializer(instance)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = UserBlogDetailSerializer(instance=instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        instance.delete()
        return JsonResponse({"info": "Blog has been deleted."}, status=204)


class BlogClassApiView(APIView):

    def get(self, request):
        blogs = UserBlog.objects.all()
        serializer = UserBlogListSerializer(blogs, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = request.data
        serializer = UserBlogListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class BlogDetailUpdateDeleteClassView(APIView):

    def get_object(self, id):
        try:
            instance = UserBlog.objects.get(id=id)
            return instance
        except UserBlog.DoesNotExist:
            return JsonResponse({"error": "No object found "}, status=404)

    def get(self, request, id=None): # for detail view of a object
        instance = self.get_object(id)
        serializer = UserBlogDetailSerializer(instance)
        return JsonResponse(serializer.data)

    def put(self, request, id=None): # to update an object
        instance = self.get_object(id)
        serializer = UserBlogDetailSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, id=None): # to delete and object
        instance = self.get_object(id)
        instance.delete()
        return JsonResponse({"info": "Blog has been deleted."}, status=204)


class BlogGenericListApiView(generics.ListCreateAPIView):
    queryset = UserBlog.objects.all()
    serializer_class = UserBlogListSerializer

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminUser]




class BlogGenericUpdateDeleteDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserBlog.objects.all()
    serializer_class = UserBlogDetailSerializer

    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated, IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user == self.request.user:
            self.perform_destroy(instance)
        else:
            return Response(
                {"msg": "Delete action is unauthorized for this blog",
                 "status": status.HTTP_401_UNAUTHORIZED},
                status=status.HTTP_401_UNAUTHORIZED)
