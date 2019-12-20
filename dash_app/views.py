from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import User, Post, Comment
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def sign_in_page(request):
    return render(request, 'sign_in.html')

def logoff(request):
    request.session.clear()
    return redirect('/signin/page')

def sign_in(request):
    users_with_same_email = User.objects.filter(email=request.POST['email'])

    if len(users_with_same_email) == 0:
        messages.error(request, 'Invalid credentials')
        return redirect('/signin/page')
    else:
        found_user_db = users_with_same_email[0]

        is_pw_correct = bcrypt.checkpw(request.POST['password'].encode(), found_user_db.password.encode())

        if is_pw_correct == True:
            request.session['logged_uid'] = found_user_db.id
            return redirect('/dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('/signin/page')

def register_page(request):
    return render(request, 'register.html')

def register(request):
    if User.objects.user_validator(request) is False:
        return redirect('/register/page')
    else:
        users_with_same_email = User.objects.filter(email=request.POST['email'])

        if len(users_with_same_email) > 0:
            messages.error(request, 'Invalid credentials')
            return redirect('/register/page')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

            new_user = User.objects.create(email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=hashed_pw)

            # first_user = User.objects.first()
            # first_user.admin = True
            # first_user.save()

            request.session['logged_uid'] = new_user.id
            return redirect('/dashboard')

def dashboard(request):
    uid = request.session.get('logged_uid')
    user_level = ''

    if uid is None:
        return redirect('/signin/page')
    else:
        all_users = User.objects.all()
        if User.objects.filter(admin=False):
            user_level = 'normal'
        else:
            user_level = 'admin'

            context = {
                'all_users': all_users,
                'user_level': user_level,
            }
            return render(request, 'user_dash.html', context)

def user_info(request, user_id):
    uid = request.session.get('logged_uid')

    if uid is None:
        return redirect('/signin/page')
    else:
        logged_user = User.objects.get(id=user_id)
        all_users_post = Post.objects.all()
        # all_users_comments = Comment.objects.all()

        context = {
            'user': logged_user,
            'all_posts': all_users_post,
            # 'all_comments': all_users_comments,
        }
        return render(request, 'user_info.html', context)

def new_post(request, user_id):
    uid = request.session.get('logged_uid')
    logged_user = User.objects.get(id=user_id)

    if uid is None:
        return redirect('/signin/page')
    else:
        if Post.objects.post_validator(request) is False:
            return redirect(f'/users/show/{user_id}')
        else:
            new_post = Post.objects.create(post=request.POST['post'], created_by=logged_user)
            return redirect(f'/users/show/{user_id}')

def new_post_comment(request, post_id):
    uid = request.session.get('logged_uid')
    logged_user = User.objects.get(id=uid)

    if uid is None:
        return redirect('/signin/page')
    else:
        if Comment.objects.comment_validator(request) is False:
            return redirect(f'/users/show/{uid}')
        else:
            found_post = Post.objects.filter(id=post_id)

            if len(found_post) > 0:
                this_post = found_post[0]
                new_comment = Comment.objects.create(comment=request.POST['comment'], post=this_post, created_by=logged_user)
                return redirect(f'/users/show/{uid}')