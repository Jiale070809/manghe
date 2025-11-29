from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import  ProfileForm



@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    # 显示匹配记录
    matches = request.user.matches.all().order_by('-match_score')[:5]
    return render(request, 'users/profile.html', {
        'form': form,
        'matches': matches
    })