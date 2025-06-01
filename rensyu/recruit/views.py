from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Recruit
from .forms import RecruitForm

def index(request):
    # 検索パラメータを取得
    name = request.GET.get('name', '')
    status = request.GET.get('status', '')
    entry_day = request.GET.get('entry_day', '')
    documents_status = request.GET.get('documents_status', '')

    # 並び替えパラメータを取得
    sort = request.GET.get('sort', 'entry_day')  # デフォルトは応募日
    order = request.GET.get('order', 'desc')     # デフォルトは降順

    # クエリセットを初期化
    recruits = Recruit.objects.all()

    # 検索条件を適用
    if name:
        recruits = recruits.filter(name__icontains=name)
    if status:
        recruits = recruits.filter(status=status)
    if entry_day:
        recruits = recruits.filter(entry_day=entry_day)
    if documents_status:
        recruits = recruits.filter(documents_status=documents_status)

    # 並び替えを適用
    if order == 'asc':
        recruits = recruits.order_by(sort)
    else:
        recruits = recruits.order_by(f'-{sort}')

    # 検索条件をコンテキストに追加
    context = {
        'recruits': recruits,
        'search_params': {
            'name': name,
            'status': status,
            'entry_day': entry_day,
            'documents_status': documents_status,
        }
    }
    
    return render(request, 'recruit/index.html', context)

def recruit_create(request):
    if request.method == 'POST':
        form = RecruitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recruit_list')  # 一覧ページにリダイレクト
    else:
        form = RecruitForm()
    
    return render(request, 'recruit/recruit_form.html', {'form': form})

def recruit_edit(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    if request.method == 'POST':
        form = RecruitForm(request.POST, instance=recruit)
        if form.is_valid():
            form.save()
            return redirect('recruit_list')
    else:
        form = RecruitForm(instance=recruit)
    
    return render(request, 'recruit/recruit_form.html', {
        'form': form,
        'recruit': recruit,
        'is_edit': True
    })

def recruit_delete(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    if request.method == 'POST':
        recruit.delete()
        messages.success(request, '応募者情報を削除しました。')
        return redirect('recruit_list')
    
    return render(request, 'recruit/recruit_confirm_delete.html', {
        'recruit': recruit
    })
