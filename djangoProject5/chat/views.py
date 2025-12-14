from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatRoom, Message


@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.users.all():
        return redirect('blindbox_list')

    messages = room.messages.all()
    return render(request, 'chat/room.html', {
        'room': room,
        'chat_messages': messages,
        'other_user': room.users.exclude(id=request.user.id).first()
    })


@login_required
def create_room(request, user_id):
    from users.models import User
    other_user = get_object_or_404(User, id=user_id)
    # 检查是否已有共同房间
    room = ChatRoom.objects.filter(users=request.user).filter(users=other_user).first()
    if not room:
        room = ChatRoom.objects.create()
        room.users.add(request.user, other_user)
    return redirect('chat_room', room_id=room.id)


@login_required
def send_message(request, room_id):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        room = get_object_or_404(ChatRoom, id=room_id)
        if request.user in room.users.all():
            message = Message.objects.create(
                room=room,
                sender=request.user,
                content=content
            )
            return JsonResponse({
                'status': 'success',
                'content': message.content,
                'sender': message.sender.username,
                'time': message.sent_at.strftime('%H:%M')
            })
    return JsonResponse({'status': 'error'})


@login_required
def unread_count(request):
    """返回当前用户的未读消息总数和对应房间ID"""
    # 获取所有包含未读消息的房间
    unread_rooms = ChatRoom.objects.filter(
        users=request.user,
        messages__is_read=False
    ).exclude(messages__sender=request.user).distinct()  # 排除自己发送的消息

    # 统计每个房间的未读消息数
    unread_data = []
    for room in unread_rooms:
        count = room.messages.filter(is_read=False).exclude(sender=request.user).count()
        other_user = room.users.exclude(id=request.user.id).first()
        unread_data.append({
            'room_id': room.id,
            'other_user': other_user.username if other_user else '未知用户',
            'count': count
        })

    return JsonResponse({
        'has_unread': len(unread_data) > 0,
        'unread_rooms': unread_data
    })

@login_required
def mark_read(request, room_id):
    """标记房间内的所有未读消息为已读"""
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user in room.users.all():
        # 只标记非自己发送的消息
        room.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    return JsonResponse({'status': 'success'})




# Create your views here.
