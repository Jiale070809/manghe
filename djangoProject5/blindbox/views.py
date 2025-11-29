from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlindBox, Category, OpenRecord
from .forms import BlindBoxForm
from .services import match_users


def blindbox_list(request):
    categories = Category.objects.all()
    # 按分类筛选
    category_id = request.GET.get('category')
    if category_id:
        blindboxes = BlindBox.objects.filter(category_id=category_id)
    else:
        blindboxes = BlindBox.objects.all()
    return render(request, 'blindbox/list.html', {
        'categories': categories,
        'blindboxes': blindboxes
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
    blindbox = get_object_or_404(BlindBox, pk=pk)

    if OpenRecord.objects.filter(user=request.user, blindbox=blindbox).exists():
        return render(request, 'blindbox/already_opened.html', {'blindbox': blindbox})

    # 创建开盒记录
    record = OpenRecord.objects.create(user=request.user, blindbox=blindbox)
    # 匹配用户
    matched_user, score = match_users(request.user, blindbox)

    return render(request, 'blindbox/opened.html', {
        'blindbox': blindbox,
        'matched_user': matched_user,
        'match_score': score
    })


from django.shortcuts import render

# Create your views here.
