import pandas as pd
import numpy as np
import os

# 存在する列のみを削除する関数
def base_drop(df_name):
    columns_to_drop = ["Benefit", "Tax", "Total ticket price", "Wix service fee", "Ticket revenue", "Payment status", "Checked in","Ticket number"]
    existing_columns_to_drop = [col for col in columns_to_drop if col in df_name.columns]
    df_name.drop(columns=existing_columns_to_drop, inplace=True)
    
def P_drop(df_name):
    if "Ticket number" in df_name.columns:
        df_name.drop(df_name[~df_name['Ticket number'].str.endswith('P')].index, inplace=True) # チケット番号がP以外で終わる行を削除
    columns_to_drop = ["Benefit", "Tax", "Total ticket price", "Wix service fee", "Ticket revenue", "Payment status", "Checked in","Ticket number"]
    existing_columns_to_drop = [col for col in columns_to_drop if col in df_name.columns]
    df_name.drop(columns=existing_columns_to_drop, inplace=True)
    
def optional_drop(df_name):
    columns_to_drop = [
        "会場の様子を主催者等による広報で使用する場合があります/All photo will be used on SNS",
        "会場には駐車場がないので、近隣の有料駐車場を利用していただくか公共交通機関でお越しください/There is no parking available at the venue, so please use nearby paid parking facilities or consider using public transportation to get there。",
        "備考",
        "会場には駐車場がないので、近隣の有料駐車場を利用していただくか公共交通機関でお越しください/There is no parking available at the venue, so please use nearby paid parking facilities or consider using public transportation to get there.",
        "会場には駐車場がないので、公共交通機関でお越しください/No parking available",
        "居住地",
        "会場の様子は主催者等による広報で使用する場合があります/All photo will be used on SNS"
    ]
    existing_columns_to_drop = [col for col in columns_to_drop if col in df_name.columns]
    df_name.drop(columns=existing_columns_to_drop, inplace=True)
    
def full_drop(df_name):
    base_drop(df_name)
    optional_drop(df_name)

# 必要な列名を変更する関数
def base_rename(df_name):
    df_name.rename(columns={"Ticket type": "チケット種類", "Seat Information": "座席種", "Ticket price": "チケット価格", "カテゴリー/Category": "カテゴリー", "国籍/Country": "国籍", "学年/Grade": "学年","学年/Grade *筑波大生のみ必須/UT student MUST answer":"学年","学年/Grade※筑波大生のみ必須/UT student Must Answer":"学年","Order date":"購入日","所属（学群生）/Affiliation *筑波大生のみ必須/UT student MUST answer":"所属","所属（学群生）/Affilliation※筑波大生のみ必須/UT student Must Answer":"所属","年代/Age":"年代"}, inplace=True)
    
def optional_rename(df_name):
    df_name.rename(columns={"Coupon":"クーポン有無","普段のスポーツ実施頻度/How often do you play sports?": "スポーツ実施頻度", "今回のTSUKUBA LIVE!を知ったきっかけ？/Where did you know about this TSUKUBA LIVE! ?": "知ったきっかけ","本イベントを知ったきっかけ？/Where did you learn about us?":"知ったきっかけ","本イベントを知ったきっかけ/Where did you learn about us?":"知ったきっかけ", "普段のスポーツ観戦頻度/How often do you watch sports?": "スポーツ観戦頻度","TSUKUBA LIVE!にこれまで何回来場したことがありますか？/How many times have you attended TSUKUBA LIVE! so far?":"来場回数","TSUKUBA LIVE!の参加回数/This is my 〇〇 arrival at TSUKUBA LIVE!":"来場回数"}, inplace=True)

def full_rename(df_name):
    base_rename(df_name)
    optional_rename(df_name)
    
# データ名の修正
def revise_price_data(df_name):
    # データを文字列に変換してから文字列操作を行う
    df_name["チケット価格"] = df_name["チケット価格"].astype(str)
    df_name["チケット価格"] = df_name["チケット価格"].str.replace("¥", "").str.replace(",", "").astype(int)
    
def revise_coupon_data(df_name):
    df_name["クーポン有無"] = df_name["クーポン有無"].astype(str)  # 非文字列データを文字列に変換
    df_name["クーポン有無"] = df_name["クーポン有無"].str.replace("¥500 - COSMICUN", "クーポンあり")
    df_name["クーポン有無"] = df_name["クーポン有無"].str.replace("¥500 - HANDBALL", "クーポンあり")
    df_name["クーポン有無"] = df_name["クーポン有無"].str.replace("nan", "クーポンなし")
    df_name.loc[df_name["クーポン有無"].isna(), "クーポン有無"] = "クーポンなし"

def revise_Category_data(df_name):
    if "カテゴリー" in df_name.columns:
        df_name["カテゴリー"] = df_name["カテゴリー"].str.replace("筑波大学学生/Univ. of Tsukuba Student", "筑波大生")
        df_name["カテゴリー"] = df_name["カテゴリー"].str.replace("その他/Others", "その他")
        df_name["カテゴリー"] = df_name["カテゴリー"].str.replace("筑波大学教職員/Univ. of Tsukuba Faculty and Staff", "筑波大教職員")
        df_name["カテゴリー"] = df_name["カテゴリー"].str.replace("つくば市在住/ Residents of Tsukuba City", "つくば市在住")
        df_name["カテゴリー"] = df_name["カテゴリー"].str.replace("つくば市在勤/ Commute to Work in Tsukuba City", "つくば市在勤")
        df_name["カテゴリー"] = df_name["カテゴリー"].str.replace("アルバータ大学関係者/University of Alberta associate", "アウェーチーム関係者")
    
def revise_Grade_data(df_name):
    df_name["学年"] = df_name["学年"].str.replace("修士課程/Master's Course", "Master")
    df_name["学年"] = df_name["学年"].str.replace("博士課程/Ph.D", "Ph.D")
    df_name["学年"] = df_name["学年"].str.replace("筑波大生ではない/Not UT student", "筑波大生でない")
    df_name["学年"] = df_name["学年"].str.replace("-", "筑波大生でない")
    
def revise_reasons_data(df_name):
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("前回のTSUKUBA LIVE!から知っていた/I knew it from the last TSUKUBA LIVE!", "前回から知っていた")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("前回のTSUKUBA LIVE!で知った/I knew it at the last TSUKUBA LIVE!", "前回のTL!で知った")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace(" 前回のTSUKUBA LIVE!の時から知っていた/knew from the last Home Game", "前回のTL!で知った")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("前回のTSUKUBA LIVE!の時から知っていた/knew from the last Home Game", "前回のTL!で知った")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("家族・友人の紹介/from a friend・family", "家族・友人の紹介")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace(" 家族・友人の紹介/from a friend", "家族・友人の紹介")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("家族・友人の紹介/from a friend", "家族・友人の紹介")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("家族・友人の紹介/ from a friend・family", "家族・友人の紹介")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("選手の知り合い/friend of player", "選手の知人")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("女子バレーボール部員の紹介/Introduction from the women's volleyball team", "選手の知人")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("TSUKUBA LIVE! 運営スタッフの紹介/Introduction from the TSUKUBA LIVE! organizing staff", "クリエイターからの紹介")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("メディアの記事を読んだ/from media", "メディアの記事")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("ポスター/poster", "ポスター")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("チラシ/Flyer", "チラシ")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("コズミくん/cosmicun", "コズミくん")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace(" SNS（コズミくん）/Cosmi-cun", "コズミくんSNS")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("SNS（コズミくん）/Cosmi-cun", "コズミくんSNS")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("SNS (TSUKUBA LIVE!)", "TL!SNS")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace(" SNS（体育スポーツ局）/UT BPES", "スポーツ局SNS")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("SNS（体育スポーツ局）/UT BPES", "スポーツ局SNS")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("SNS (体育スポーツ局）/UT BPES", "スポーツ局SNS")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("コズミくんと会った/Met with Cosmicun.", "コズミくんと会った")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("今日オープンキャンパスで知った/Learned at today's Open Campus.", "オープンキャンパス")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace(" Twitter", "X")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("Twitter", "X")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("X (TSUKUBA LIVE! 公式)", "X")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("Instagram (TSUKUBA LIVE! 公式)", "Instagram")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("LINE (TSUKUBA LIVE! 公式)", "LINE")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("筑波大学女子バレボール部 公式SNS/Univ. of Tsukuba Women's Volleyball Team Official SNS", "チームSNS")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("つくばユナイテッドSun GAIA 公式SNS/Tsukuba United Sun GAIA Official SNS", "スポンサー企業SNS")
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].str.replace("つくばユナイテッドSun GAIA関係者の紹介/Introduction from Tsukuba United Sun GAIA", "スポンサー企業からの紹介")
    
    
    
def revise_sports_watch_data(df_name):
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("月に2~3回程度/few/month", "24~36回/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("月に2-3回程度/ few/month", "24~36回/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("月に1回/1/month", "12回/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("月に1回程度/ 1/month", "12回/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("2~3ヶ月に1回程度/1/few months", "4~6回/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("2-3か月に1回程度/ 1/few months", "4~6回/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("半年に1回程度/1/6months", "2回/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("半年に1回程度/ 1/ 6months", "2回/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("1年に1回程度/1/year", "1回/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("1年に一回程度/ 1/year", "1回/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("それ未満/less than 1/year", "1-/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("それ未満/ less than 1/year", "1-/年")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("週に1回以上/1+/week", "1+/週")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("週に1回以上/ 1+/week", "1+/週")
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].str.replace("月に1回/1/month", "1+/月")
    
    
def revise_sports_play_data(df_name):
    if "スポーツ実施頻度" in df_name.columns:
        df_name["スポーツ実施頻度"] = df_name["スポーツ実施頻度"].str.replace("週に3回以上/more than 3/week", "3回+/週")
        df_name["スポーツ実施頻度"] = df_name["スポーツ実施頻度"].str.replace("週に1~2回/few/week", "1~2回/週")
        df_name["スポーツ実施頻度"] = df_name["スポーツ実施頻度"].str.replace("月に1回/1/month", "1回/月")
        df_name["スポーツ実施頻度"] = df_name["スポーツ実施頻度"].str.replace("2~3ヶ月に1回程度/1/few months", "1回/2~3カ月")
        df_name["スポーツ実施頻度"] = df_name["スポーツ実施頻度"].str.replace("それ未満/less than 1/few months", "1回-/2~3カ月")#一番初めのデータを参照
    
def revise_OrderDate_data(df_name):
    df_name['購入日'] = pd.to_datetime(df_name['購入日']).dt.strftime('%Y/%m/%d')
    
def additional_revise(df_name):
    if "性別" in df_name.columns:
        df_name["性別"] = df_name["性別"].str.replace("男性, 女性", "その他")
        df_name["性別"] = df_name["性別"].str.replace("女性, 男性", "その他")
    if "カテゴリー" in df_name.columns:
        df_name["カテゴリー"] = df_name["カテゴリー"].astype(str)
        df_name["カテゴリー"] = df_name["カテゴリー"].apply(lambda x: "筑波大生" if "筑波大生" in x else x)
        df_name["カテゴリー"] = df_name["カテゴリー"].apply(lambda x: "筑波大教職員" if "筑波大教職員" in x else x)
        df_name["カテゴリー"] = df_name["カテゴリー"].apply(lambda x: "つくば市在住" if "つくば市在住" in x else x)
        df_name["カテゴリー"] = df_name["カテゴリー"].apply(lambda x: "つくば市在勤" if "つくば市在勤務" in x else x)
    df_name["座席種"] = df_name["座席種"].str.replace("Area: ", "")
    #筑波大生＞筑波大教職員＞つくば市在住＞つくば市在勤＞その他
    df_name["学年"] = df_name["学年"].str.replace("1年, 筑波大生でない", "他大生")
    df_name["学年"] = df_name["学年"].str.replace("2年, 筑波大生でない", "他大生")
    df_name["学年"] = df_name["学年"].str.replace("3年, 筑波大生でない", "他大生")
    df_name["学年"] = df_name["学年"].str.replace("4年, 筑波大生でない", "他大生")
    df_name["学年"] = df_name["学年"].str.replace("U1", "1年")
    df_name["学年"] = df_name["学年"].str.replace("U2", "2年")
    df_name["学年"] = df_name["学年"].str.replace("U3", "3年")
    df_name["学年"] = df_name["学年"].str.replace("U4", "4年")
    df_name["学年"] = df_name["学年"].str.replace("M1", "Master")
    df_name["学年"] = df_name["学年"].str.replace("M2", "Master")
    df_name["学年"] = df_name["学年"].str.replace("D(博士課程）", "Ph.D")
    df_name["学年"] = df_name["学年"].str.replace("D1", "Ph.D")
    df_name["学年"] = df_name["学年"].str.replace("D2", "Ph.D")
    df_name["学年"] = df_name["学年"].apply(lambda x: "Master" if "Master" in x else x)
    if "カテゴリー" in df_name.columns:
        df_name['学年'] = df_name.apply(lambda row: "筑波大生でない" if (row['カテゴリー'] != "筑波大生") else row['学年'],axis=1)
    
    if "所属" in df_name.columns:
        df_name["所属"] = df_name["所属"].str.replace("-", "筑波大生でない")
    # スポーツ観戦頻度の列で、コンマで区切られた最初の選択肢のみを取得
    if "スポーツ観戦頻度" in df_name.columns:
        df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].apply(lambda x: x.split(',')[0])
    # スポーツ実施頻度の列で、コンマで区切られた最初の選択肢のみを取得
    if "スポーツ実施頻度" in df_name.columns:
        df_name["スポーツ実施頻度"] = df_name["スポーツ実施頻度"].apply(lambda x: x.split(',')[0])
    if "来場回数" in df_name.columns:
        df_name["来場回数"] = df_name["来場回数"].str.replace("1月2日","1~2回")
        df_name["来場回数"] = df_name["来場回数"].str.replace("3月4日","3~4回")
        df_name["来場回数"] = df_name["来場回数"].str.replace("5月6日","5~6回")
    
def revise_age_data(df_name):
    if "年代" in df_name.columns:
        df_name["年代"] = df_name["年代"].str.replace("10 - 19歳", "18歳以下")
        df_name["年代"] = df_name["年代"].str.replace("10代", "18歳以下")
        df_name["年代"] = df_name["年代"].str.replace("18歳以下/Under18", "18歳以下")
        df_name["年代"] = df_name["年代"].str.replace("20 - 29歳", "19&20代")
        df_name["年代"] = df_name["年代"].str.replace("20代", "19&20代")
        df_name["年代"] = df_name["年代"].str.replace("19歳・20代/19 - 20s", "19&20代")
        df_name["年代"] = df_name["年代"].str.replace("30 - 39歳", "30代")
        df_name["年代"] = df_name["年代"].str.replace("30代/30s", "30代")
        df_name["年代"] = df_name["年代"].str.replace("40 - 49歳", "40代")
        df_name["年代"] = df_name["年代"].str.replace("40代/40s", "40代")
        df_name["年代"] = df_name["年代"].str.replace("50 - 59歳", "50代")
        df_name["年代"] = df_name["年代"].str.replace("50代/50s", "50代")
        df_name["年代"] = df_name["年代"].str.replace("60 - 69歳", "60代")
        df_name["年代"] = df_name["年代"].str.replace("60代/60s", "60代")
        df_name["年代"] = df_name["年代"].str.replace("70 歳以上", "60代以上")
        df_name["年代"] = df_name["年代"].str.replace("70代以上/70 and over", "60代以上")

def full_revise(df_name):
    revise_price_data(df_name)
    revise_coupon_data(df_name)
    revise_Category_data(df_name)
    revise_Grade_data(df_name)
    if "購入日" in df_name.columns:
        revise_OrderDate_data(df_name)
    revise_reasons_data(df_name)
    revise_sports_watch_data(df_name)
    revise_sports_play_data(df_name)
    revise_age_data(df_name)

# データフレームの操作
def allpreprocessing(df_name,csv_path):
    full_drop(df_name)
    full_rename(df_name)
    full_revise(df_name)
    additional_revise(df_name)
    df_name.to_csv(csv_path, index=False)

def allpreprocessing_dropP(df_name,csv_path):
    P_drop(df_name)
    full_drop(df_name)
    full_rename(df_name)
    full_revise(df_name)
    additional_revise(df_name)
    df_name.to_csv(csv_path, index=False)
# CSVファイルの読み込み
#以下のcsv_Pathのみを変更

def preprocessing_for_app(csv_Path):
    created_csv_Path = csv_Path.replace("original.csv","full.csv")
    onlyP_csv_Path = csv_Path.replace("original.csv","onlyP.csv")
    # CSVファイルの保存
    df = pd.read_csv(csv_Path)
    allpreprocessing(df,created_csv_Path)
    df = pd.read_csv(csv_Path)
    allpreprocessing_dropP(df,onlyP_csv_Path)
    return created_csv_Path,onlyP_csv_Path
