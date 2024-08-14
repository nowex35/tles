from django.shortcuts import render

# Create your views here.
def index(request):
    message = {
        'title':'webapp',
        'text':'Hello',
    }
    return render(request, 'webapp/index.html', message)

def day_sales(request):
    message = {
        'title':'webapp',
        'text':'day_sales',
    }
    return render(request, 'webapp/day_sales.html', message)

def grade(request):
    message = {
        'title':'webapp',
        'text':'grade',
    }
    return render(request, 'webapp/grade.html', message)

def category(request):
    message = {
        'title':'webapp',
        'text':'category',
    }
    return render(request, 'webapp/category.html', message)

def past_visits(request):
    message = {
        'title':'webapp',
        'text':'past_visits',
    }
    return render(request, 'webapp/past_visits.html', message)

def play_sports(request):
    message = {
        'title':'webapp',
        'text':'play_sports',
    }
    return render(request, 'webapp/play_sports.html', message)

def watch_sports(request):
    message = {
        'title':'webapp',
        'text':'watch_sports',
    }
    return render(request, 'webapp/watch_sports.html', message)

def coupon(request):
    message = {
        'title':'webapp',
        'text':'coupon',
    }
    return render(request, 'webapp/coupon.html', message)

def reasons(request):
    message = {
        'title':'webapp',
        'text':'reasons',
    }
    return render(request, 'webapp/reasons.html', message)

def past_events(request):
    message = {
        'title':'webapp',
        'text':'past_events',
    }
    return render(request, 'webapp/past_events.html', message)

def new_event(request):
    message = {
        'title':'webapp',
        'text':'new_event',
    }
    return render(request, 'webapp/new_event.html', message)