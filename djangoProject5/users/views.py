from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from blindbox.models import BlindBox, OpenRecord
from .forms import RegisterForm, ProfileForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

        # 2. 获取当前用户创建的盲盒（我的盲盒）
    my_blindboxes = BlindBox.objects.filter(
        creator=request.user
    ).select_related('category').order_by('-created_at')  # 按创建时间倒序

    # 3. 获取当前用户打开的盲盒记录（你提供的my_records查询）
    my_records = OpenRecord.objects.filter(
        user=request.user
    ).select_related('blindbox', 'blindbox__creator')

    # 显示匹配记录
    matches = request.user.matches.all().order_by('-match_score')[:5]
    return render(request, 'users/profile.html', {
        'form': form,
        'matches': matches
    })


from django.shortcuts import render

# Create your views here.
