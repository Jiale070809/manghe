from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages
from django.db.models import Q

from . import models
from .models import BlindBox, Category, OpenRecord
from .forms import BlindBoxForm
from .services import match_users


def blindbox_list(request):
    categories = Category.objects.all()
    # 按分类筛选
    category_id = request.GET.get('category')
    current_user = request.user


    if category_id:
        # 关键：筛选分类ID匹配且未开盒的盲盒（根据业务需求调整）
        blindboxes = BlindBox.objects.filter(
        creator__isnull = False&Q(category_id=category_id)
        ).exclude(creator=request.user).select_related('creator', 'category')
    else:
        # 默认显示所有未开盒的盲盒
        blindboxes = BlindBox.objects.filter(
            creator__isnull=False
        ).exclude(creator=request.user).select_related('creator', 'category')
    user_open_records = OpenRecord.objects.filter(user=current_user).values_list('blindbox_id', flat=True)
    for box in blindboxes:
        # 在视图中用Python代码判断，避免模板中调用带参filter
        box.user_has_opened = box.id in user_open_records
    return render(request, 'blindbox/list.html', {
        'categories': categories,
        'blindboxes': blindboxes,
        'selected_category': category_id,
        'user_open_records': user_open_records
    })


@login_required
def create_blindbox(request):
    if request.method == 'POST':
        form = BlindBoxForm(request.POST)
        if form.is_valid():
            blindbox = form.save(commit=False)
            blindbox.creator = request.user
            blindbox.save()
            return render(request, 'blindbox/created.html', {'blindbox': blindbox})
    else:
        form = BlindBoxForm()
    return render(request, 'blindbox/create.html', {'form': form})


@login_required
def open_blindbox(request, pk):
    current_user = request.user
    blindbox = get_object_or_404(BlindBox, pk=pk)

    if OpenRecord.objects.filter(user=current_user, blindbox=blindbox).exists():
        return render(request, 'blindbox/already_opened.html', {'blindbox': blindbox})

    # 创建开盒记录
    OpenRecord.objects.create(user=current_user, blindbox=blindbox)
    # 匹配用户
    matched_user, score = match_users(current_user, blindbox)

    blindbox.is_active = False
    blindbox.save()

    matched_user = blindbox.creator

    return render(request, 'blindbox/opened.html', {
        'blindbox': blindbox,
        'matched_user': matched_user,
        'match_score': score
    })


from django.shortcuts import render

# Create your views here.
