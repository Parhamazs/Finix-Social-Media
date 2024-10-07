from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Like, Friendship, Message
from .forms import PostForm, CommentForm, MessageForm

# Create your views here.

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'social_media/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'social_media/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'social_media/post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'social_media/post_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'social_media/post_confirm_delete.html'
    success_url = '/social_media/'

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'social_media/comment_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

class LikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        Like.objects.get_or_create(user=request.user, post=post)
        return redirect('post_detail', pk=pk)

class UnLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        Like.objects.filter(user=request.user, post=post).delete()
        return redirect('post_detail', pk=pk)

class FriendshipView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user2 = User.objects.get(pk=pk)
        Friendship.objects.get_or_create(user1=request.user, user2=user2)
        return redirect('profile', pk=pk)

class UnFriendshipView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user2 = User.objects.get(pk=pk)
        Friendship.objects.filter(user1=request.user, user2=user2).delete()
        return redirect('profile', pk=pk)

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'social_media/message_form.html'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver_id = self.kwargs['pk']
        return super().form_valid(form)

@login_required
def profile(request, pk):
    user = User.objects.get(pk=pk)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    friends = user.friendship_set.all()
    return render(request, 'social_media/profile.html', {'user': user, 'posts': posts, 'friends': friends})

@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'social_media/inbox.html', {'messages': messages})

# Create your views here.
