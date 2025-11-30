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
        'messages': messages,
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
        room = get_object_or_404(ChatRoom, id=room_id)
        if request.user in room.users.all():
            message = Message.objects.create(
                room=room,
                sender=request.user,
                content=request.POST['content']
            )
            return JsonResponse({
                'status': 'success',
                'content': message.content,
                'sender': message.sender.username,
                'time': message.sent_at.strftime('%H:%M')
            })
    return JsonResponse({'status': 'error'})


from django.shortcuts import render

# Create your views here.
