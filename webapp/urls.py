from django.urls import path

from . import views

app_name = "webapp"
urlpatterns = [
    path("",views.index,name="index"),
    path("day_sales/",views.day_sales,name="day_sales"),
    path("grade/",views.grade,name="grade"),
    path("category/",views.category,name="category"),
    path("past_visits/",views.past_visits,name="past_visits"),
    path("play_sports/",views.play_sports,name="play_sports"),
    path("watch_sports/",views.watch_sports,name="watch_sports"),
    path("coupon/",views.coupon,name="coupon"),
    path("reasons/",views.reasons,name="reasons"),
    path("past_events/",views.past_events,name="past_events"),
    path("new_event/",views.new_event,name="new_event"),
]