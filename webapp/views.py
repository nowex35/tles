import os
from django.conf import settings
from django.shortcuts import render,get_object_or_404,redirect
import pandas as pd
from .forms import UploadCSVForm,EventForm
from .services import preprocessing, makeGraph
from django.contrib.auth.decorators import login_required
from .models import models
from django.core.paginator import Paginator
import datetime
from django.contrib.auth import login as auth_login
from allauth.account.forms import LoginForm
from django.urls import reverse
import chardet

from .models import Event,Existing_Data
# Create your views here.
import logging

logger = logging.getLogger(__name__)

import logging

logger = logging.getLogger(__name__)

def custom_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            logger.debug(f'User {user.username} authenticated successfully')
            auth_login(request, user)
            return redirect('webapp:index')
        else:
            logger.debug(f'Form errors: {form.errors}')  # エラーメッセージを出力
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def index(request):
    message = {
        'title':'webapp',
        'text':'Hello',
    }
    return render(request, 'webapp/index.html', message)

@login_required
def day_sales(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'same_dates':
        events = Event.objects.filter(game_date=models.F('data_version_date'))
    else:
        events = Event.objects.all()
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    day_sales_graph_paths = []
    
    for root, dirs, files in os.walk(media_root):
        for version_date in events.values_list('data_version_date', flat=True):
            formatted_date = version_date.strftime('%y%m%d')
            if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
                for filename in files:
                    if "day_sales" in filename:  # "day_sales" を含むファイルを探す
                        file_path = os.path.relpath(os.path.join(root, filename), media_root)
                        day_sales_graph_paths.append(os.path.join(media_url, file_path))

    if not day_sales_graph_paths:
        print("No day sales graphs found.")

    return render(request, 'webapp/day_sales.html', {'graph_paths': day_sales_graph_paths})

@login_required
def grade(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'same_dates':
        events = Event.objects.filter(game_date=models.F('data_version_date'))
    else:
        events = Event.objects.all()
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    grade_graph_paths = []
    
    for root, dirs, files in os.walk(media_root):
        for version_date in events.values_list('data_version_date', flat=True):
            formatted_date = version_date.strftime('%y%m%d')
            if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
                for filename in files:
                    if "grade" in filename:  # "grade" を含むファイルを探す
                        file_path = os.path.relpath(os.path.join(root, filename), media_root)
                        grade_graph_paths.append(os.path.join(media_url, file_path))

    if not grade_graph_paths:
        print("No grade graphs found.")

    return render(request, 'webapp/grade.html', {'graph_paths': grade_graph_paths})

@login_required
def category(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'same_dates':
        events = Event.objects.filter(game_date=models.F('data_version_date'))
    else:
        events = Event.objects.all()
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    category_graph_paths = []
    
    for root, dirs, files in os.walk(media_root):
        for version_date in events.values_list('data_version_date', flat=True):
            formatted_date = version_date.strftime('%y%m%d')
            if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
                for filename in files:
                    if "category" in filename:  # "category" を含むファイルを探す
                        file_path = os.path.relpath(os.path.join(root, filename), media_root)
                        category_graph_paths.append(os.path.join(media_url, file_path))

    if not category_graph_paths:
        print("No category graphs found.")

    return render(request, 'webapp/category.html', {'graph_paths': category_graph_paths,"filter_option":filter_option})

@login_required
def age(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'same_dates':
        events = Event.objects.filter(game_date=models.F('data_version_date'))
    else:
        events = Event.objects.all()
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    age_graph_paths = []
    
    for root, dirs, files in os.walk(media_root):
        for version_date in events.values_list('data_version_date', flat=True):
            formatted_date = version_date.strftime('%y%m%d')
            if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
                for filename in files:
                    if "Age" in filename:
                        file_path = os.path.relpath(os.path.join(root, filename), media_root)
                        age_graph_paths.append(os.path.join(media_url, file_path))

    if not age_graph_paths:
        print("No age graphs found.")

    return render(request, 'webapp/age.html', {'graph_paths': age_graph_paths,"filter_option":filter_option})

@login_required
def gender(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'same_dates':
        events = Event.objects.filter(game_date=models.F('data_version_date'))
    else:
        events = Event.objects.all()
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    gender_graph_paths = []
    
    for root, dirs, files in os.walk(media_root):
        for version_date in events.values_list('data_version_date', flat=True):
            formatted_date = version_date.strftime('%y%m%d')
            if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
                for filename in files:
                    if "gender" in filename:
                        file_path = os.path.relpath(os.path.join(root, filename), media_root)
                        gender_graph_paths.append(os.path.join(media_url, file_path))

    if not gender_graph_paths:
        print("No gender graphs found.")

    return render(request, 'webapp/gender.html', {'graph_paths': gender_graph_paths,"filter_option":filter_option})

@login_required
def past_visits(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'same_dates':
        events = events.filter(game_date=models.F('data_version_date'))
    else:
        events = Event.objects.all()
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    past_visits_graph_paths = []
    
    for root, dirs, files in os.walk(media_root):
        for version_date in Event.objects.values_list('data_version_date', flat=True):
            formatted_date = version_date.strftime('%y%m%d')
            if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
                for filename in files:
                    if "PastVisits" in filename:  # "past_visits" を含むファイルを探す
                        file_path = os.path.relpath(os.path.join(root, filename), media_root)
                        past_visits_graph_paths.append(os.path.join(media_url, file_path))

    if not past_visits_graph_paths:
        print("No past_visits graphs found.")

    return render(request, 'webapp/past_visits.html', {'graph_paths': past_visits_graph_paths})

@login_required
def play_sports(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'same_dates':
        events = Event.objects.filter(game_date=models.F('data_version_date'))
    else:
        events = Event.objects.all()
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    play_sports_graph_paths = []
    
    for root, dirs, files in os.walk(media_root):
        for version_date in events.values_list('data_version_date', flat=True):
            formatted_date = version_date.strftime('%y%m%d')
            if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
                for filename in files:
                    if ("playSports" in filename) and ("OnlyTU" not in filename):  # "play_sports" を含むファイルを探す
                        file_path = os.path.relpath(os.path.join(root, filename), media_root)
                        play_sports_graph_paths.append(os.path.join(media_url, file_path))

    if not play_sports_graph_paths:
        print("No play_sports graphs found.")

    return render(request, 'webapp/play_sports.html', {'graph_paths': play_sports_graph_paths})

@login_required
def watch_sports(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'same_dates':
        events = Event.objects.filter(game_date=models.F('data_version_date'))
    else:
        events = Event.objects.all()
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    watch_sports_graph_paths = []
    
    for root, dirs, files in os.walk(media_root):
        for version_date in events.values_list('data_version_date', flat=True):
            formatted_date = version_date.strftime('%y%m%d')
            if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
                for filename in files:
                    if ("watchSports" in filename) and ("OnlyTU" not in filename):  # "watch_sports" を含むファイルを探す
                        file_path = os.path.relpath(os.path.join(root, filename), media_root)
                        watch_sports_graph_paths.append(os.path.join(media_url, file_path))

    if not watch_sports_graph_paths:
        print("No watch_sports graphs found.")

    return render(request, 'webapp/watch_sports.html', {'graph_paths': watch_sports_graph_paths})

@login_required
def coupon(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'same_dates':
        events = Event.objects.filter(game_date=models.F('data_version_date'))
    else:
        events = Event.objects.all()
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    coupon_graph_paths = []
    
    for root, dirs, files in os.walk(media_root):
        for version_date in events.values_list('data_version_date', flat=True):
            formatted_date = version_date.strftime('%y%m%d')
            if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
                for filename in files:
                    if "coupon" in filename:  # "day_sales" を含むファイルを探す
                        file_path = os.path.relpath(os.path.join(root, filename), media_root)
                        coupon_graph_paths.append(os.path.join(media_url, file_path))

    if not coupon_graph_paths:
        print("No coupon graphs found.")
    return render(request, 'webapp/coupon.html', {'graph_paths': coupon_graph_paths})

@login_required
def reasons(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'same_dates':
        events = Event.objects.filter(game_date=models.F('data_version_date'))
    else:
        events = Event.objects.all()
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    reasons_graph_paths = []
    
    for root, dirs, files in os.walk(media_root):
        for version_date in events.values_list('data_version_date', flat=True):
            formatted_date = version_date.strftime('%y%m%d')
            if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
                for filename in files:
                    if ("reasons" in filename) and ("OnlyTU" not in filename) and ("percentage" not in filename):  # "reasons" を含むファイルを探す
                        file_path = os.path.relpath(os.path.join(root, filename), media_root)
                        reasons_graph_paths.append(os.path.join(media_url, file_path))

    if not reasons_graph_paths:
        print("No reasons graphs found.")

    return render(request, 'webapp/reasons.html', {'graph_paths': reasons_graph_paths})

@login_required
def reasons_percent(request):
    filter_option = request.GET.get('filter', 'all')
    if filter_option == 'same_dates':
        events = Event.objects.filter(game_date=models.F('data_version_date'))
    else:
        events = Event.objects.all()
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    reasons_percent_graph_paths = []
    # game_dateが存在する場合、日付を'240606'形式に変換
    
    for root, dirs, files in os.walk(media_root):
        for version_date in events.values_list('data_version_date', flat=True):
            formatted_date = version_date.strftime('%y%m%d')
            if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
                for filename in files:
                    if ("reasons" in filename) and ("OnlyTU" not in filename) and ("percentage" in filename):  # "reasons" を含むファイルを探す
                        file_path = os.path.relpath(os.path.join(root, filename), media_root)
                        reasons_percent_graph_paths.append(os.path.join(media_url, file_path))

    if not reasons_percent_graph_paths:
        print("No reasons graphs found.")

    return render(request, 'webapp/reasons_percent.html', {'graph_paths': reasons_percent_graph_paths})

@login_required
def new_event(request):
    if request.method == "POST":
        form = UploadCSVForm(request.POST, request.FILES)
        event_form = EventForm(request.POST)
        if form.is_valid() and event_form.is_valid():
            try:
                csv_file = request.FILES['file']
        
                # 一時ファイルに保存してから読み込む
                temp_file_path = os.path.join(settings.MEDIA_ROOT, "temp", csv_file.name)
                save_dir = os.path.dirname(temp_file_path)
                os.makedirs(save_dir, exist_ok=True)

                with open(temp_file_path, 'wb+') as destination:
                    for chunk in csv_file.chunks():
                        destination.write(chunk)

                # エンコーディングを推測
                with open(temp_file_path, 'rb') as f:
                    raw_data = f.read(1024 * 1024)  # 最初の1MBをサンプルとして使用
                    result = chardet.detect(raw_data)

                if result['encoding'] and 'shift_jis' in result['encoding'].lower():
                    # CSVファイルを読み込む (エンコーディングを指定)
                    df = pd.read_csv(temp_file_path, encoding='shift_jis')

                    # utf-8-sigでCSVファイルとして保存
                    file_path = os.path.join(settings.MEDIA_ROOT, "ticket_csv/", csv_file.name)
                    is_exist = os.path.exists(file_path)
                    df.to_csv(file_path, encoding='utf-8-sig', index=False)

                else:
                    # そのままファイルを保存
                    file_path = os.path.join(settings.MEDIA_ROOT, "ticket_csv/", csv_file.name)
                    is_exist = os.path.exists(file_path)
                    os.rename(temp_file_path, file_path)

                # 不要になった一時ファイルを削除
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)


                preprocessing.preprocessing_for_app(file_path)
                makeGraph.GraphForApp(file_path)
                
                file_path_processed = file_path.replace("original", "full")
                df = pd.read_csv(file_path_processed)
                data_preview = df.head()
                
                # ファイルが既に存在するか確認
                if is_exist:
                    return render(request, 'webapp/new_event.html', {
                        'form': form,
                        'event_form': event_form,
                        'data_preview': data_preview.to_html(),
                        'file_path': file_path,
                        'success_message': 'ファイルは既に存在します。Eventデータ作成処理をスキップしました。'
                    })
                
                # データパターンの確認と既存データの作成
                data_pattern = [field.name for field in Existing_Data._meta.get_fields()][1:-2]
                new_data_pattern = [column in df.columns for column in data_pattern]
                
                existing_data, created = Existing_Data.objects.get_or_create(
                    category=new_data_pattern[0],
                    grade=new_data_pattern[1],
                    price=new_data_pattern[2],
                    seat_type=new_data_pattern[3],
                    reasons=new_data_pattern[4],
                    coupon=new_data_pattern[5],
                    ticket_sale_date=new_data_pattern[6],
                    past_visits=new_data_pattern[7],
                    play_sports=new_data_pattern[8],
                    watch_sports=new_data_pattern[9],
                    country=new_data_pattern[10],
                    age=new_data_pattern[11],
                    affiliation=new_data_pattern[12],
                    gender=new_data_pattern[13],
                    occupation=new_data_pattern[14],
                )
                
                # イベントの作成
                filename = os.path.basename(file_path)
                date_str = filename[:6]
                date_obj = datetime.datetime.strptime(date_str, "%y%m%d")
                
                new_event = Event(
                    team_name=event_form.cleaned_data["team_name"],
                    opponent_team=event_form.cleaned_data["opponent_team"],
                    game_date=event_form.cleaned_data["game_date"],
                    opening_time=event_form.cleaned_data["opening_time"],
                    event_place=event_form.cleaned_data["event_place"],
                    release_date=event_form.cleaned_data["release_date"],
                    data_version_date=date_obj.date(),
                    number_of_spectators=event_form.cleaned_data["number_of_spectators"],
                    existing_data_id=existing_data,
                    user=request.user,
                    event_image=event_form.cleaned_data["event_image"],
                    description=event_form.cleaned_data["description"]
                )
                new_event.save()
                
                return render(request, 'webapp/new_event.html', {
                    'form': form,
                    'event_form': event_form,
                    'data_preview': data_preview.to_html(),
                    'file_path': file_path,
                    'success_message': 'イベントが正常に作成されました。'
                })
            
            except Exception as e:
                return render(request, 'webapp/new_event.html', {
                    'form': form,
                    'event_form': event_form,
                    'error_message': f"ファイルの処理中にエラーが発生しました: {str(e)}"
                })
    else:
        form = UploadCSVForm()
        event_form = EventForm()

    return render(request, 'webapp/new_event.html', {'form': form, 'event_form': event_form})

@login_required
def past_events(request):
    # 現在のユーザーに関連するイベントを取得し、作成日の降順で並べ替える
    events = Event.objects.filter(user=request.user).order_by("-game_date")
    
    # ページネーション
    paginator = Paginator(events, 10)  # 1ページに10個のイベントを表示
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # テンプレートに渡すコンテキストデータを作成
    context = {
        'title': 'webapp',
        'text': 'past_events',
        'page_obj': page_obj,  # ページネーションされたオブジェクトをテンプレートに渡す
    }
    return render(request, 'webapp/past_events.html', context)

@login_required
def event_detail(request, event_id):
    # イベントをIDで取得し、存在しない場合は404エラーを返す
    event = get_object_or_404(Event, pk=event_id)
    
    media_root = settings.MEDIA_ROOT
    media_url = settings.MEDIA_URL
    graph_paths = []
    # game_dateが存在する場合、日付を'240606'形式に変換
    
    for root, dirs, files in os.walk(media_root):
        version_date = event.data_version_date
        formatted_date = version_date.strftime('%y%m%d')
        if ("result" in os.path.basename(root)) and (formatted_date in os.path.basename(root)):
            for filename in files:
                file_path = os.path.relpath(os.path.join(root, filename), media_root)
                graph_paths.append(os.path.join(media_url, file_path))

    if not graph_paths:
        print("No graphs found.")
        
    has_day_sales = any("day_sales"in path for path in graph_paths)
    has_grade = any("grade"in path for path in graph_paths)
    has_category = any("category"in path for path in graph_paths)
    has_past_visits = any("PastVisits"in path for path in graph_paths)
    has_play_sports = any("playSports"in path for path in graph_paths)
    has_watch_sports = any("watchSports"in path for path in graph_paths)
    has_reasons = any("reasons"in path for path in graph_paths)
    has_ticket = any("Ticket"in path for path in graph_paths)
    
    # コンテキストにイベントを渡す
    context = {
        'event': event,
        'graph_paths': graph_paths,
        'has_day_sales': has_day_sales,
        'has_grade': has_grade,
        'has_category': has_category,
        'has_past_visits': has_past_visits,
        'has_play_sports': has_play_sports,
        'has_watch_sports': has_watch_sports,
        'has_reasons': has_reasons,
        'has_ticket': has_ticket,
    }
    
    return render(request, 'webapp/event_detail.html', context)