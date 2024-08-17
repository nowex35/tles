from accounts.models import CustomUser
from django.db import models

# Create your models here.
class Existing_Data(models.Model):
    """存在データパターンモデル"""
    pattern_id = models.AutoField('存在データパターンID', primary_key=True)
    category = models.BooleanField('カテゴリー', default=False)
    grade = models.BooleanField('学年', default=False)
    price = models.BooleanField('チケット価格', default=False)
    seat_type = models.BooleanField('座席種', default=False)
    reasons = models.BooleanField('知ったきっかけ', default=False)
    coupon = models.BooleanField('クーポン有無', default=False)
    ticket_sale_date = models.BooleanField('購入日', default=False)
    past_visits = models.BooleanField('来場回数', default=False)
    play_sports = models.BooleanField('スポーツ実施頻度', default=False)
    watch_sports = models.BooleanField('スポーツ観戦頻度', default=False)
    country = models.BooleanField('国籍', default=False)
    age = models.BooleanField('年代', default=False)
    affiliation = models.BooleanField('所属', default=False)
    gender = models.BooleanField('性別', default=False)
    occupation = models.BooleanField('職業', default=False)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    
    class Meta:
        verbose_name_plural = "Existing_Data"
    
    def __str__(self):
        return str(self.pattern_id)

class Event(models.Model):
    """イベントモデル"""
    event_id = models.AutoField('イベントID', primary_key=True)#Djangoでは自動でIDが作成されるため、IDを指定する必要はないが、ここではevent_idを設定してprimary_key=Trueで主キーに設定している
    name = models.CharField('イベント名', max_length=255,default='TSUKUBA LIVE!')
    team_name = models.CharField('チーム名', max_length=255, blank=True, null=True)
    opponent_team = models.CharField('対戦相手', max_length=255, blank=True, null=True)
    game_date = models.DateField('試合日', blank=True, null=True)
    opening_time = models.TimeField('開演時間', blank=True, null=True)
    event_place = models.CharField('開催場所', max_length=255, blank=True, null=True)
    release_date = models.DateField('チケット発売日', blank=True, null=True)
    data_version_date = models.DateField('データバージョン日', blank=True, null=True)
    number_of_spectators = models.IntegerField('観客数', blank=True, null=True)
    existing_data_id = models.ForeignKey(Existing_Data, on_delete=models.CASCADE, blank=True, null=True, verbose_name='存在データID')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='ユーザー')
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)
    event_image = models.ImageField('イベント画像', upload_to='static/images/', blank=True, null=True, default='static/images/アイコン.png')
    description = models.TextField('イベント詳細', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Event"
    
    def __str__(self):
        return self.name
    
