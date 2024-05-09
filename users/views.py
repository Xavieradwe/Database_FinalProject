
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .models import User, Locations,Hoods,Blocks
from django.db.models import Q
from django.http import JsonResponse
import json
from django.db import transaction
from django.views.decorators.http import require_http_methods
import os
from django.views.decorators.http import require_POST


User = get_user_model()

def home_view(request):
    # if request.method == 'POST':
    return render(request,'registration/home.html')

def login_view(request):
    if request.method == 'POST':
        # 处理用户提交的登录表单
        email = request.POST.get('username')
        password = request.POST.get('password')
        user = None
        try:
            user = User.objects.get(email=email)  # Retrieve user by email
        except User.DoesNotExist:
            return render(request, 'registration/login.html', {'error_message': 'Invalid email or password.'})
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            # 用户认证成功，登录用户
            login(request, user)
            user.last_access_date = timezone.now()
            
            user.save()

            return redirect('homeInterface') # return render(request,'registration/home.html')  # 重定向到用户主页或其他页面
        else:
            # 用户认证失败，显示登录页面并提示错误信息
            return render(request, 'registration/login.html', {'error_message': 'Invalid username or password.'})
    else:
        # 显示登录页面
        return render(request, 'registration/login.html')

def register_view(request):
    if request.method == 'POST':
        # 处理用户提交的注册表单

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        description = request.POST.get('profile_description')
        picture = request.FILES.get('profile_picture')
        

        # address = request.POST.get('address', 'Default Address')
        # latitude = request.POST.get('latitude', 0.0)  # 默认值为0.0
        # longitude = request.POST.get('longitude', 0.0)  # 默认值为0.0
        # 创建新用户账户
        user = User.objects.create_user(username=username, email=email, 
                                        password=password, first_name=first_name,
                                        last_name=last_name, profile_description=description,
                                        profile_picture = picture,
                                        registration_date = timezone.now())
        user.save()
        # location = Locations.objects.create(
        #     address=address,
        #     latitude=latitude,
        #     longitude=longitude
        # )
        # location.save()
        return redirect('login')  # 注册成功后重定向到登录页面
    else:
        # 显示注册页面
        return render(request, 'registration/registra.html')

def homeInterface_view(request):
    return render(request,'registration/HomeInterface.html')

def logout_view(request):
    # 注销用户并重定向到注销成功页面
    logout(request)
    return render(request, 'registration/logout.html')

@login_required
def user_profile(request):
    """ API to fetch user profile details """
    if request.method == 'GET':
        data = {
            'username': request.user.username,
            'profile_description': request.user.profile_description,
            'profile_picture': request.user.profile_picture.url if request.user.profile_picture else None,
            'registration_date': request.user.registration_date,
            'last_access_date': request.user.last_access_date,
            'user_id': request.user.    user_id
        }
        return JsonResponse(data)

# @login_required
# def user_friends(request):
#     """ API to fetch friends and neighbors """
#     if request.method == 'GET':
#         friends = Friendships.objects.filter(user1=request.user).select_related('user2').order_by('-creation_date')
#         friends_list = [
#             {
#                 'username': friend.user2.username,
#                 'profile_description': friend.user2.profile_description,
#                 'profile_picture': friend.user2.profile_picture.url if friend.user2.profile_picture else None,
#                 'status': friend.status,
#                 'creation_date': friend.creation_date
#             }
#             for friend in friends
#         ]
#         neighbors = Neighbors.objects.filter(user=request.user).select_related('neighbor_user').order_by('-creation_date')
#         neighbors_list = [
#             {
#                 'username': neighbor.neighbor_user.username,
#                 'profile_description': neighbor.neighbor_user.profile_description,
#                 'profile_picture': neighbor.neighbor_user.profile_picture.url if neighbor.neighbor_user.profile_picture else None,
#                 # 'creation_date': neighbor.neighbor_user.date_joined.isoformat()  # Assuming you have a date_joined field or similar
#             }
#             for neighbor in neighbors
#         ]

#         # Return combined data
#         return JsonResponse({'friends': friends_list, 'neighbors': neighbors_list}, safe=False)
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Friendships, Neighbors

@login_required
def user_friends(request):
    if request.method == 'GET':
        # Fetching friends where the current user is either user1 or user2 and status is 'Accepted'
        friends = Friendships.objects.filter(
            (Q(user1=request.user) | Q(user2=request.user)),
            status='Accepted'
        ).prefetch_related('user1', 'user2').order_by('-creation_date')
        
        # List comprehension to prepare friends data excluding the current user
        friends_list = [
            {
                'username': friend.user2.username if friend.user1 == request.user else friend.user1.username,
                'profile_description': friend.user2.profile_description if friend.user1 == request.user else friend.user1.profile_description,
                'profile_picture': friend.user2.profile_picture.url if friend.user1 == request.user else friend.user1.profile_picture.url,
                'status': friend.status,
                'creation_date': friend.creation_date,
                'user_id':friend.user2.user_id if friend.user1 == request.user else friend.user1.user_id,
            }
            for friend in friends if (friend.user1 != request.user or friend.user2 != request.user)
        ]


        # 获取邻居关系，类似地避免重复
        neighbors = Neighbors.objects.filter(
            Q(user=request.user) | Q(neighbor_user=request.user)
        ).select_related('user', 'neighbor_user').order_by('-creation_date')

        neighbors_list = [
            {
                'username': neighbor.neighbor_user.username if neighbor.user == request.user else neighbor.user.username,
                'profile_description': neighbor.neighbor_user.profile_description if neighbor.user == request.user else neighbor.user.profile_description,
                'profile_picture': neighbor.neighbor_user.profile_picture.url if neighbor.user == request.user else neighbor.user.profile_picture.url,
                'creation_date': neighbor.neighbor_user.date_joined.isoformat() if neighbor.user == request.user else neighbor.user.date_joined.isoformat(),
                'user_id': neighbor.neighbor_user.user_id if neighbor.user == request.user else neighbor.user.user_id,
            }
            for neighbor in neighbors
        ]
        # Return combined data
        return JsonResponse({'friends': friends_list, 'neighbors': neighbors_list}, safe=False)
    
@login_required
def user_details(request, user_id):
    user_info = get_object_or_404(User, pk=user_id)
    if(user_id == request.user.user_id):
        return render(request, 'registration/user_details.html', {'user': user_info})
    else:
        return render(request, 'registration/friend-neighbor-profiles.html', {'user': user_info})
    

@login_required
def user_hoods(request):
    # 获取当前用户关注的所有Blocks
    followed_blocks = Follows.objects.filter(user=request.user).select_related('block')
    
    # 从关注的Blocks中提取所有不重复的Hood信息
    hoodList = set()
    for follow in followed_blocks:
        if follow.block and follow.block.hood:
            hoodList.add(follow.block.hood)
    
    # 准备返回的Hood数据
    hoods_data = [{
        'hood_id': hood.hood_id,
        'name': hood.name,
        'description': hood.description
    } for hood in hoodList]
    
    return JsonResponse(list(hoods_data), safe=False)

@login_required
def threads_in_hood(request, hood_id):
    message_ids = Recipients.objects.filter(hood_id=hood_id).values_list('message_id', flat=True).distinct()
    threads = Threads.objects.filter(initial_message_id__in=message_ids).distinct()
    # print("Initial message IDs for block", hood_id, ":", list(threads))
    # Prepare the JSON data for threads
    threads_data = [{
        'thread_id': thread.thread_id,
        'topic': thread.topic,
        'initial_message_id': thread.initial_message_id if thread.initial_message else None
    } for thread in threads]

    return JsonResponse(list(threads_data), safe=False)

@login_required
def messages_in_thread(request, thread_id):
    # Fetching messages from a specific thread
    messages = Messages.objects.filter(thread_id=thread_id).order_by('timestamp')

    # Preparing messages data to return
    messages_data = [{
        'message_id': message.message_id,
        'body': message.body,
        'user_id': message.user_id,
        'username': message.user.username,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for message in messages]

    return JsonResponse(list(messages_data), safe=False)

import logging
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
logger = logging.getLogger(__name__)  # Set up a logger

@login_required
@method_decorator(csrf_exempt, name='dispatch')
@require_http_methods(["POST"])  # This ensures that only POST requests are handled
def reply_to_message(request, thread_id):
    try:
        data = json.loads(request.body)
        message_body = data.get('body')
        # print("reply_to_message, thread_id: ", thread_id,)
        if not message_body:
            return JsonResponse({'status': 'error', 'message': 'Message body cannot be empty'}, status=400)
        
        new_message = Messages.objects.create(
            body=message_body,
            user=request.user,
            thread_id=thread_id,
            timestamp=timezone.now(),
        )

        return JsonResponse({'status': 'success', 'message_id': new_message.message_id}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)    

@login_required
def user_blocks(request):
    # Try to get the user's followed block
    followed_block = Follows.objects.filter(user=request.user).select_related('block').first()
    if followed_block and followed_block.block:
        # Fetch all blocks within the same hood as the followed block
        blocks_in_hood = Blocks.objects.filter(hood=followed_block.block.hood).distinct()
    else:
        # If no block is followed, return an empty list
        blocks_in_hood = []

    blocks_data = [{
        'block_id': block.block_id,
        'name': block.name,
        'description': block.description,
        'is_followed': (block == followed_block.block) if followed_block else False
    } for block in blocks_in_hood]

    return JsonResponse(list(blocks_data), safe=False)

@login_required
def threads_in_block(request, block_id):
    message_ids = Recipients.objects.filter(block_id=block_id).values_list('message_id', flat=True).distinct()
    threads = Threads.objects.filter(initial_message_id__in=message_ids).distinct()
    threads_data = [{
        'thread_id': thread.thread_id,
        'topic': thread.topic,
        'initial_message_id': thread.initial_message_id
    } for thread in threads]

    return JsonResponse(list(threads_data), safe=False)


@login_required
def friends_threads(request):
    try:
        # Fetch all unique initial_message_ids linked to the current user in the Recipients model
        # initial_message_ids = Recipients.objects.filter(
        #     user_id=request.user.user_id  # Assume 'user_id' is the field linking to the Users model
        # ).values_list('message__initial_message_of', flat=True).distinct()

        initial_message_ids = Recipients.objects.filter(user_id=request.user.user_id).values_list('message_id', flat=True).distinct()

        print("friends_threads, initial_message_ids: ", initial_message_ids)

        # Fetch all threads where the initial_message_id is in the list of ids collected above
        threads = Threads.objects.filter(
            initial_message_id__in=initial_message_ids
        )
        print("friends_threads, thread_id: ", threads)

        # Prepare and return the data for the response
        threads_data = [{
            'id': thread.thread_id,
            'topic': thread.topic
        } for thread in threads]

        return JsonResponse(list(threads_data), safe=False)
    except Exception as e:
        # Log the error to console
        print(f"Error retrieving friends' threads: {str(e)}")
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)



@login_required
def neighbors_threads(request):
    try:
        # Fetch all unique initial_message_ids linked to the current user in the Recipients model
        # initial_message_ids = Recipients.objects.filter(
        #     user_id=request.user.user_id  # Assume 'user_id' is the field linking to the Users model
        # ).values_list('message__initial_message_of', flat=True).distinct()

        initial_message_ids = Recipients.objects.filter(neighbor_id=request.user.user_id).values_list('message_id', flat=True).distinct()

        print("friends_threads, initial_message_ids: ", initial_message_ids)

        # Fetch all threads where the initial_message_id is in the list of ids collected above
        threads = Threads.objects.filter(
            initial_message_id__in=initial_message_ids
        )
        print("friends_threads, thread_id: ", threads)

        # Prepare and return the data for the response
        threads_data = [{
            'id': thread.thread_id,
            'topic': thread.topic
        } for thread in threads]

        return JsonResponse(list(threads_data), safe=False)
    except Exception as e:
        # Log the error to console
        print(f"Error retrieving friends' threads: {str(e)}")
        return JsonResponse({'error': 'Failed to fetch data'}, status=500)


@login_required
@method_decorator(csrf_exempt, name='dispatch')
@require_http_methods(["POST"])  # This ensures that only POST requests are handled
def create_thread(request):
    data = json.loads(request.body)  # Use json.loads to parse the JSON request body
    topic = data.get('topic')
    message_body = data.get('message')
    recipient_type = data.get('recipient_type')  # "friends", "neighbors", "block", "hood"
    recipient_ids = data.get('recipient_ids')  # IDs of friends, neighbors, block or hood
    print('topic:',topic)
    print('message_body:',message_body)
    print('recipient_type:',recipient_type)
    print('recipient_ids:',recipient_ids)
    try:
        with transaction.atomic():
            # Create the thread
            thread = Threads.objects.create(
                topic=topic,
                created_time=timezone.now()
            )

            # Create the initial message
            message = Messages.objects.create(
                subject=topic,
                body=message_body,
                user=request.user,
                thread=thread,
                timestamp=timezone.now()
            )

            # Update initial message in thread
            thread.initial_message = message
            thread.save()

            # Handle recipients
            if recipient_type in ['friends', 'neighbors']:
                recipient_field = 'neighbor_id' if recipient_type == 'neighbors' else 'user_id'
                for recipient_id in recipient_ids.split(','):
                    Recipients.objects.create(
                        message=message,
                        **{recipient_field: recipient_id}
                    )
                    Recipients.objects.create(
                        message=message,
                        **{recipient_field: request.user.user_id}
                    )
            elif recipient_type == 'block':
                followed_block = Follows.objects.filter(user=request.user).select_related('block').first()

                Recipients.objects.create(
                    message=message,
                    block_id=followed_block.block.block_id
                )
            elif recipient_type == 'hood':
                followed_block = Follows.objects.filter(user=request.user).select_related('block').first()
                # hoodtemp = Hoods.objects.filter(block=blocktemp2.block).select_related('hood').first()
                Recipients.objects.create(
                    message=message,
                    hood_id=followed_block.block.hood_id
                )

            return JsonResponse({'status': 'success', 'message': 'Thread created successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    
@login_required
@require_POST
def update_profile(request):
    user = request.user
    username = request.POST.get('username')
    email = request.POST.get('email')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    description = request.POST.get('description')
    profile_picture = request.FILES.get('profile_picture')
    print('user.profilesdiption: ',email)

    # print("sd")
    if username:
        user.username = username

    if email:
        user.email = email
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if description:
        print('user.profile_description: ',user.profile_description)
        print('user.pn: ',user.profile_description)

        user.profile_description = description
        print('profile_description: ',user.profile_description)

    if profile_picture:
        if user.profile_picture:
            old_path = user.profile_picture.path
            if os.path.isfile(old_path):
                os.remove(old_path)
        user.profile_picture = profile_picture
    
    user.save()
    return JsonResponse({"success": True, "message": "Profile updated successfully."})

@login_required
def search_messages(request):
    query = request.GET.get('query', '').strip()
    if query:
        q_objects = Q()
        for term in query.split():
            q_objects &= Q(body__icontains=term)
        messages = Messages.objects.filter(q_objects).select_related('user')
        messages_data = [
            {'body': m.body, 'username': m.user.username if m.user else "Unknown"} 
            for m in messages
        ]
        return JsonResponse({'messages': messages_data})
    else:
        return JsonResponse({'messages': []})
