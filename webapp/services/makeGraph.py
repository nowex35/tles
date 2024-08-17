import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 'Agg'は描画を行わないバックエンド
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from django.conf import settings

# 日本語フォントのパスを指定（システムに応じて変更が必要かもしれません）
font_path = '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'  # この行は環境によって変更が必要です
font_prop = fm.FontProperties(fname=font_path)

# matplotlibのデフォルトフォントを設定
plt.rcParams['font.family'] = 'TakaoPGothic'
import os




def make_reasonsGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].fillna("").astype(str)
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"]
    reasons_pattern = ["選手の知人","Instagram","家族・友人の紹介","X","LINE","前回のTL!で知った","ポスター","メディアの記事","コズミくん","通りすがり","前回から知っていた","コズミくんSNS","TL!SNS","スポーツ局SNS","コズミくんと会った","オープンキャンパス","クリエイターからの紹介","チラシ","チームSNS","スポンサー企業SNS","スポンサー企業からの紹介"]
    reasons = []
    reasons_count = []
    total_responses = 0  # 全体の回答数を格納する変数
    for pattern in reasons_pattern:
        if pattern in df_name["知ったきっかけ"].unique():
                reasons.append(pattern)
                reasons_count.append(0)
    for reason in reasons:
        count=0
        for i in range(len(df_name)):
            if reason in df_name["知ったきっかけ"][i]:
                count+=1
                total_responses += 1  # 回答が見つかるたびに全体の回答数をインクリメント
        reasons_count[reasons.index(reason)] = count
    
    for reason in reasons:
        count=0
        for i in range(len(df_name)):
            if reason in df_name["知ったきっかけ"][i]:
                count+=1
        reasons_count[reasons.index(reason)] = count
    df_reasons = pd.DataFrame({"reasons":reasons,"reasons_count":reasons_count})
    plt.figure(figsize=(12,5))
    plt.ylabel("人数[人]")
    plt.title(head+":TLを知ったきっかけの人数")
    plt.bar(df_reasons["reasons"], df_reasons["reasons_count"])
    plt.savefig(os.path.join(result_path, head + "reasons.png"),bbox_inches="tight")
    plt.close()
    
def make_reasonsPercentageGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"].fillna("").astype(str)
    df_name["知ったきっかけ"] = df_name["知ったきっかけ"]
    reasons_pattern = ["選手の知人","Instagram","家族・友人の紹介","X","LINE","前回のTL!で知った","ポスター","メディアの記事","コズミくん","通りすがり","前回から知っていた","コズミくんSNS","TL!SNS","スポーツ局SNS","コズミくんと会った","オープンキャンパス","クリエイターからの紹介","チラシ","チームSNS","スポンサー企業SNS","スポンサー企業からの紹介"]
    reasons = []
    reasons_count = []
    total_responses = 0  # 全体の回答数を格納する変数
    for pattern in reasons_pattern:
        if pattern in df_name["知ったきっかけ"].unique():
                reasons.append(pattern)
                reasons_count.append(0)
    for reason in reasons:
        count=0
        for i in range(len(df_name)):
            if reason in df_name["知ったきっかけ"][i]:
                count+=1
                total_responses += 1  # 回答が見つかるたびに全体の回答数をインクリメント
        reasons_count[reasons.index(reason)] = count
    # 全体に占める割合を計算
    reasons_percentage = [count / total_responses * 100 for count in reasons_count]  # 割合を計算してリストに格納
    df_reasons = pd.DataFrame({"reasons":reasons, "reasons_percentage":reasons_percentage})
    plt.figure(figsize=(12,5))
    plt.ylabel("割合[%]")  # Y軸のラベルを人数から割合に変更
    plt.title(head+":TLを知ったきっかけの割合")
    plt.bar(df_reasons["reasons"], df_reasons["reasons_percentage"])  # 割合をプロット
    plt.ylim(0, 35)  # Y軸の範囲を0~35%に設定
    plt.savefig(os.path.join(result_path, head + "reasons_percentage.png"),bbox_inches="tight")
    plt.close()

def make_genderGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    # カテゴリの出現回数を数える
    category_counts = df_name["性別"].value_counts()

    # 円グラフを描画
    plt.figure(figsize=(9,9))
    plt.title(head+":性別の割合")
    plt.pie(x=category_counts, labels=category_counts.index,startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,colors=["#ED7D31","#4472C4","#FFFFCE"],textprops={'fontsize': 18})
    plt.savefig(os.path.join(result_path, head + "gender.png"),bbox_inches="tight")
    plt.close()
    
def make_categoryGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    # カテゴリの出現回数を数える
    category_counts = df_name["カテゴリー"].value_counts()
    # カテゴリーと色のマッピング
    color_mapping = {
        '筑波大生': '#1978B5',
        'つくば市在住': '#FF8006',
        'つくば市在勤': '#9567BE',
        '筑波大教職員': '#D72223',
        'その他': '#28A128'
    }
    colors = [color_mapping.get(category, 'white') for category in category_counts.index]

    # 円グラフを描画
    plt.figure(figsize=(9,9))
    plt.title(head+":カテゴリーごとの割合")
    plt.pie(x=category_counts, labels=category_counts.index,startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,textprops={'fontsize': 18},colors=colors)
    plt.savefig(os.path.join(result_path, head + "category.png"),bbox_inches="tight")
    plt.close()

def make_gradeGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    # カテゴリの出現回数を数える
    category_counts = df_name.drop(df_name[df_name['学年'] == '筑波大生でない'].index)["学年"].value_counts()
    # カテゴリーと色のマッピング
    color_mapping = {
        'Master': '#1978B5',
        '4年': '#FF8006',
        '3年': '#9567BE',
        '2年': '#D72223',
        '1年': '#28A128',
        'Ph.D': '#FFD700',
        '他大生': '#FF69B4'
    }
    colors = [color_mapping.get(category, 'white') for category in category_counts.index]


    # 円グラフを描画
    plt.figure(figsize=(9,9))
    plt.title(head+":学年ごとの割合")
    plt.pie(x=category_counts, labels=category_counts.index,startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,textprops={'fontsize': 18},colors=colors)
    plt.savefig(os.path.join(result_path, head + "grade.png"),bbox_inches="tight")
    plt.close()
    
def make_watchSportsGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    # スポーツ観戦頻度の列で、コンマで区切られた最初の選択肢のみを取得
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].apply(lambda x: x.split(',')[0])
    # カテゴリの出現回数を数える
    category_counts = df_name["スポーツ観戦頻度"].value_counts()

    # 円グラフを描画
    plt.figure(figsize=(9,9))
    plt.title(head+":スポーツ観戦頻度の割合")
    plt.pie(x=category_counts, labels=category_counts.index,startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,textprops={'fontsize': 18})
    plt.savefig(os.path.join(result_path, head + "watchSports.png"),bbox_inches="tight")
    plt.close()

def make_watchSportsGraph_onlyTU(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df = df_name.copy()
    df = df[df['カテゴリー'] == '筑波大生']  # '筑波大生' のみを抽出
    # スポーツ観戦頻度の列で、コンマで区切られた最初の選択肢のみを取得
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].apply(lambda x: x.split(',')[0])
    # カテゴリの出現回数を数える
    category_counts = df["スポーツ観戦頻度"].value_counts()

    # 円グラフを描画
    plt.figure(figsize=(9,9))
    plt.title(head+":TLに来た筑波大生のスポーツ観戦頻度の割合")
    plt.pie(x=category_counts, labels=category_counts.index,startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,textprops={'fontsize': 18})
    plt.savefig(os.path.join(result_path, head + "watchSportsOnlyTU.png"),bbox_inches="tight")
    plt.close()

def make_watchSportsGraph_onlyBachelor(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df = df_name.copy()
    df['学年'] = df['学年'].apply(lambda x: '学群生' if x in ['1年', '2年', '3年', '4年'] else x)
    df = df.drop(df[df['学年'] != '学群生'].index)
    # スポーツ観戦頻度の列で、コンマで区切られた最初の選択肢のみを取得
    df_name["スポーツ観戦頻度"] = df_name["スポーツ観戦頻度"].apply(lambda x: x.split(',')[0])
    # カテゴリの出現回数を数える
    category_counts = df["スポーツ観戦頻度"].value_counts()

    # 円グラフを描画
    plt.figure(figsize=(9,9))
    plt.title(head+":TLに来た学群生のスポーツ観戦頻度の割合")
    plt.pie(x=category_counts, labels=category_counts.index,startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,textprops={'fontsize': 18})
    plt.savefig(os.path.join(result_path, head + "watchSportsOnlyBachelor.png"),bbox_inches="tight")
    plt.close()
    
def make_playSportsGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    # スポーツ実施頻度の列で、コンマで区切られた最初の選択肢のみを取得
    df_name["スポーツ実施頻度"] = df_name["スポーツ実施頻度"].apply(lambda x: x.split(',')[0])
    # カテゴリの出現回数を数える
    category_counts = df_name["スポーツ実施頻度"].value_counts()

    # 円グラフを描画
    plt.figure(figsize=(9,9))
    plt.title(head+":スポーツ実施頻度の割合")
    plt.pie(x=category_counts, labels=category_counts.index,startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,textprops={'fontsize': 18})
    plt.savefig(os.path.join(result_path, head + "playSports.png"),bbox_inches="tight")
    plt.close()

def make_playSportsGraph_onlyTU(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df = df_name.copy()
    df = df[df['カテゴリー'] == '筑波大生']  # '筑波大生' のみを抽出
    # スポーツ実施頻度の列で、コンマで区切られた最初の選択肢のみを取得
    df_name["スポーツ実施頻度"] = df_name["スポーツ実施頻度"].apply(lambda x: x.split(',')[0])
    # カテゴリの出現回数を数える
    category_counts = df["スポーツ実施頻度"].value_counts()

    # 円グラフを描画
    plt.figure(figsize=(9,9))
    plt.title(head+":TLに来た筑波大生のスポーツ実施頻度の割合")
    plt.pie(x=category_counts, labels=category_counts.index,startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,textprops={'fontsize': 18})
    plt.savefig(os.path.join(result_path, head + "playSportsOnlyTU.png"),bbox_inches="tight")
    plt.close()
    
def make_playSportsGraph_onlyBachelor(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df = df_name.copy()
    df['学年'] = df['学年'].apply(lambda x: '学群生' if x in ['1年', '2年', '3年', '4年'] else x)
    df = df.drop(df[df['学年'] != '学群生'].index)
    # スポーツ実施頻度の列で、コンマで区切られた最初の選択肢のみを取得
    df_name["スポーツ実施頻度"] = df_name["スポーツ実施頻度"].apply(lambda x: x.split(',')[0])
    # カテゴリの出現回数を数える
    category_counts = df["スポーツ実施頻度"].value_counts()

    # 円グラフを描画
    plt.figure(figsize=(9,9))
    plt.title(head+":TLに来た学群生のスポーツ実施頻度の割合")
    plt.pie(x=category_counts, labels=category_counts.index,startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,textprops={'fontsize': 18})
    plt.savefig(os.path.join(result_path, head + "playSportsOnlyBachelor.png"),bbox_inches="tight")
    plt.close()

def make_TicketPrice_GradeGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    # "チケット価格"と"Grade"の組み合わせの出現回数を計算
    seat_grade_counts = df_name.groupby('チケット価格')["学年"].value_counts()

    # 出現回数を基に割合を算出
    seat_grade_percentage = seat_grade_counts.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).unstack()

    # 棒グラフで表示
    seat_grade_percentage.plot(kind='bar', figsize=(12, 6))

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':チケット価格ごとの学年の割合')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "TicketType_Grade_bar.png"),bbox_inches="tight")
    plt.close()
    

def make_TicketPrice_GradeGraph2(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df2 = df_name.copy()
    df2['学年'] = df2['学年'].apply(lambda x: '学群生' if x in ['1年', '2年', '3年', '4年'] else x)
    
    # "チケット価格"と"Grade"の組み合わせの出現回数を計算
    seat_grade_counts = df2.groupby('チケット価格')["学年"].value_counts()

    # 出現回数を基に割合を算出
    seat_grade_percentage = seat_grade_counts.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).unstack()

    # 棒グラフで表示
    seat_grade_percentage.plot(kind='bar', figsize=(12, 6))

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':チケット価格ごとの購入者層の割合')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "TicketType_Grade_bar2.png"),bbox_inches="tight")
    plt.close()

def make_TicketPrice_GradeGraph3(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df3 = df_name.copy()
    df3['学年'] = df3['学年'].apply(lambda x: '筑波大生' if x in ['1年', '2年', '3年', '4年','Master','Ph.D'] else x)
    
    # "チケット価格"と"Grade"の組み合わせの出現回数を計算
    seat_grade_counts = df3.groupby('チケット価格')["学年"].value_counts()

    # 出現回数を基に割合を算出
    seat_grade_percentage = seat_grade_counts.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).unstack()

    # 棒グラフで表示
    seat_grade_percentage.plot(kind='bar', figsize=(12, 6))

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':チケット価格ごとの購入者層の割合')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "TicketType_Grade_bar3.png"),bbox_inches="tight")
    plt.close()
    
def make_realTicketPrice_GradeGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df = df_name.copy()
    df['チケット価格'] = df.apply(lambda row: row['チケット価格'] - 500 if row['クーポン有無'] == 'クーポンあり' else row['チケット価格'], axis=1)
    # "チケット価格"と"Grade"の組み合わせの出現回数を計算
    seat_grade_counts = df_name.groupby('チケット価格')["学年"].value_counts()

    # 出現回数を基に割合を算出
    seat_grade_percentage = seat_grade_counts.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).unstack()

    # 棒グラフで表示
    seat_grade_percentage.plot(kind='bar', figsize=(12, 6))

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':クーポン込みのチケット価格ごとの学年の割合')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "realTicketType_Grade_bar.png"),bbox_inches="tight")
    plt.close()
    

def make_realTicketPrice_GradeGraph2(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df2 = df_name.copy()
    df2['チケット価格'] = df2.apply(lambda row: row['チケット価格'] - 500 if row['クーポン有無'] == 'クーポンあり' else row['チケット価格'], axis=1)
    df2['学年'] = df2['学年'].apply(lambda x: '学群生' if x in ['1年', '2年', '3年', '4年'] else x)
    
    # "チケット価格"と"Grade"の組み合わせの出現回数を計算
    seat_grade_counts = df2.groupby('チケット価格')["学年"].value_counts()

    # 出現回数を基に割合を算出
    seat_grade_percentage = seat_grade_counts.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).unstack()

    # 棒グラフで表示
    seat_grade_percentage.plot(kind='bar', figsize=(12, 6))

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':クーポン込みのチケット価格ごとの購入者層の割合')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "realTicketType_Grade_bar2.png"),bbox_inches="tight")
    plt.close()

def make_realTicketPrice_GradeGraph3(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df3 = df_name.copy()
    df3['チケット価格'] = df3.apply(lambda row: row['チケット価格'] - 500 if row['クーポン有無'] == 'クーポンあり' else row['チケット価格'], axis=1)
    df3['学年'] = df3['学年'].apply(lambda x: '筑波大生' if x in ['1年', '2年', '3年', '4年','Master','Ph.D'] else x)
    
    # "チケット価格"と"Grade"の組み合わせの出現回数を計算
    seat_grade_counts = df3.groupby('チケット価格')["学年"].value_counts()

    # 出現回数を基に割合を算出
    seat_grade_percentage = seat_grade_counts.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).unstack()

    # 棒グラフで表示
    seat_grade_percentage.plot(kind='bar', figsize=(12, 6))

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':クーポン込みのチケット価格ごとの購入者層の割合')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "realTicketType_Grade_bar3.png"),bbox_inches="tight")
    plt.close()

##############
#チケット価格に関して
##############

def make_TicketPrice_CouponBarGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    # "Ticket type"と"Grade"の組み合わせの出現回数を計算
    seat_grade_counts = df_name.groupby(['チケット価格', 'クーポン有無']).size()

    # 出現回数を基に割合を算出
    seat_grade_percentage = seat_grade_counts.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).unstack()

    # 棒グラフで表示
    seat_grade_percentage.plot(kind='bar', figsize=(6, 6))

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':チケット価格ごとのクーポン使用の割合')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "TicketPrice_coupon_bar.png"),bbox_inches="tight")
    plt.close()
    
def make_TicketPrice_CouponBarGraph_onlyStudents(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    # "Ticket type"と"Grade"の組み合わせの出現回数を計算
    df55 = df_name.copy().drop(df_name[df_name['学年'] == '筑波大生でない'].index)
    seat_grade_counts = df55.groupby(['チケット価格', 'クーポン有無']).size()

    # 出現回数を基に割合を算出
    seat_grade_percentage = seat_grade_counts.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).unstack()

    # 棒グラフで表示
    seat_grade_percentage.plot(kind='bar', figsize=(6, 6))

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':チケット価格ごとのクーポン使用の割合(筑波大生のみ)')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "TicketPrice_coupon_bar_onlyTU.png"),bbox_inches="tight")
    plt.close()

def make_TicketPrice_CouponPieGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df = df_name.drop(df_name[df_name['クーポン有無'] == 'クーポンなし'].index)
    price_counts = df['チケット価格'].value_counts()

    # 棒グラフで表示
    price_counts.plot(kind='pie', figsize=(9, 9),startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,textprops={'fontsize': 14})

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':クーポン使用のチケット価格割合')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket price')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "TicketPrice_coupon_pie.png"),bbox_inches="tight")
    plt.close()
    
#########
#########チケット種類に関して
#########

def make_TicketType_CouponPieGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df = df_name.drop(df_name[df_name['クーポン有無'] == 'クーポンなし'].index)
    price_counts = df['チケット種類'].value_counts()

    # 円グラフで表示
    price_counts.plot(kind='pie', figsize=(9, 9),startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2)

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':クーポン使用の席種割合')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "TicketType_coupon_pie.png"),bbox_inches="tight")
    plt.close()
    
def make_TicketType_CouponPieGraph_onlyStudents(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df = df_name.copy().drop(df_name[df_name['学年'] == '筑波大生でない'].index)
    df = df_name.drop(df_name[df_name['クーポン有無'] == 'クーポンなし'].index)
    price_counts = df['チケット種類'].value_counts()

    # 円グラフで表示
    price_counts.plot(kind='pie', figsize=(9, 9),startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2)

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':クーポン使用の席種割合')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "TicketType_coupon_pie_onlyTU.png"),bbox_inches="tight")
    plt.close()
    
def make_TicketType_CouponBarGraph_onlyStudents(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    # "Ticket type"と"Grade"の組み合わせの出現回数を計算
    df = df_name.copy().drop(df_name[df_name['学年'] == '筑波大生でない'].index)
    seat_grade_counts = df.groupby(['チケット種類', 'クーポン有無']).size()

    # 出現回数を基に割合を算出
    seat_grade_percentage = seat_grade_counts.groupby(level=0).apply(lambda x: 100 * x / float(x.sum())).unstack()

    # 棒グラフで表示
    seat_grade_percentage.plot(kind='bar', figsize=(6, 6))

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':チケット種類ごとのクーポン使用の割合(筑波大生のみ)')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "TicketType_coupon_bar_onlyTU.png"),bbox_inches="tight")
    plt.close()
    
def make_Ticket_coreFanGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df = df_name[df_name['来場回数'] != 0]
    price_counts = df['チケット種類'].value_counts()

    # 円グラフで表示
    price_counts.plot(kind='pie', figsize=(9, 9),startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2)

    # グラフのタイトルとレイアウトの調整
    plt.title(head+':前回から知っていたファンの席種割合')
    plt.ylabel('割合 (%)')
    plt.xlabel('Ticket type')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.legend(title='Grade', loc='upper left', bbox_to_anchor=(1, 0.5))
    plt.savefig(os.path.join(result_path, head + "TicketType_coreFan_pie.png"),bbox_inches="tight")
    plt.close()
    
def make_HowManyTimesGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    # カテゴリの出現回数を数える
    Times = df_name['来場回数'].value_counts()

    # 円グラフを描画
    plt.figure(figsize=(9,9))
    plt.title(head+":TL来場経験")
    plt.pie(x=Times, labels=Times.index,startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,textprops={'fontsize': 18})
    plt.savefig(os.path.join(result_path, head + "PastVisits.png"),bbox_inches="tight")
    plt.close()
    
def day_sales(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    df = df_name.copy()
    df['購入日'] = pd.to_datetime(df['購入日'],format='%Y/%m/%d', errors='coerce')
    df['購入日'] = df['購入日'].dt.strftime('%m/%d')
    
    # 購入日ごとのデータ数をカウント
    sales_count = df['購入日'].value_counts().sort_index()
    
    plt.figure(figsize=(12, 6))
    plt.bar(sales_count.index, sales_count.values)
    plt.title("日別売上")
    plt.xlabel('日付')
    plt.ylabel('売上[枚]')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(result_path, head + "day_sales_count.png"), bbox_inches="tight")
    plt.close()
    
def make_AgeGraph(df_name,csv_Path):
    name,head,result_path = make_data_name(csv_Path)
    # カテゴリの出現回数を数える
    Age_counts = df_name["年代"].value_counts()
    # カテゴリーと色のマッピング
    color_mapping = {
        '18歳以下': '#1978B5',
        '19&20代': '#FF8006',
        '30代': '#9567BE',
        '40代': '#D72223',
        '50代': '#28A128',
        '60代': '#8D554A',
        '70代以上': '#808080'
    }
    colors = [color_mapping.get(category, 'white') for category in Age_counts.index]

    # 円グラフを描画
    plt.figure(figsize=(9,9))
    plt.title(head+":年代ごとの割合")
    plt.pie(x=Age_counts, labels=Age_counts.index,startangle=90, counterclock=False, autopct="%1.1f%%",labeldistance=1.2,textprops={'fontsize': 18},colors=colors)
    plt.savefig(os.path.join(result_path, head + "Age.png"),bbox_inches="tight")
    plt.close()

def makeAll(df_1,df_f):
    make_reasonsGraph(df_1)
    make_reasonsPercentageGraph(df_1)
    #make_genderGraph(df_1)
    if 'カテゴリー' in df_1.columns:
        make_categoryGraph(df_f)
    make_gradeGraph(df_f)
    make_watchSportsGraph(df_1)
    if 'カテゴリー' in df_1.columns:
        make_watchSportsGraph_onlyTU(df_1)
    make_watchSportsGraph_onlyBachelor(df_1)
    if 'スポーツ実施頻度' in df_1.columns:
        make_playSportsGraph(df_1)
        if 'カテゴリー' in df_1.columns:
            make_playSportsGraph_onlyTU(df_1)
        make_playSportsGraph_onlyBachelor(df_1)
    plt.close('all')
    if df_f["チケット価格"].sum() > 0:
        make_TicketPrice_GradeGraph(df_f)
        make_TicketPrice_GradeGraph2(df_f)
        make_TicketPrice_GradeGraph3(df_f)
        if 'クーポン有無' in df_f.columns:
            if "クーポンあり" in df_f["クーポン有無"].unique():
                make_realTicketPrice_GradeGraph(df_f)
                make_realTicketPrice_GradeGraph2(df_f)
                make_realTicketPrice_GradeGraph3(df_f)
                make_TicketPrice_CouponBarGraph(df_f)
                make_TicketPrice_CouponBarGraph_onlyStudents(df_f)
                make_TicketPrice_CouponPieGraph(df_f)
                make_TicketType_CouponPieGraph(df_f)
                make_TicketType_CouponBarGraph_onlyStudents(df_f)
    if '来場回数' in df_1.columns:
        make_Ticket_coreFanGraph(df_1)
        make_HowManyTimesGraph(df_1)
    if '購入日' in df_1.columns:
        day_sales(df_f)
    if '年代' in df_1.columns:
        make_AgeGraph(df_1)
    plt.close('all')

def make_graph_for_app(only_Path,full_Path):
    # CSVファイルの読み込み
    df_1 = pd.read_csv(only_Path)
    df_f = pd.read_csv(full_Path)
    
    if '購入日' in df_1.columns:
        day_sales(df_f,full_Path)
    make_gradeGraph(df_f,full_Path)
    make_reasonsGraph(df_1,only_Path)
    make_reasonsPercentageGraph(df_1,only_Path)
    if 'カテゴリー' in df_1.columns:
        make_categoryGraph(df_f,full_Path)
    if 'スポーツ観戦頻度' in df_1.columns:
        make_watchSportsGraph(df_1,only_Path)
        if 'カテゴリー' in df_1.columns:
            make_watchSportsGraph_onlyTU(df_1,only_Path)
    if 'スポーツ実施頻度' in df_1.columns:
        make_playSportsGraph(df_1,only_Path)
        if 'カテゴリー' in df_1.columns:
            make_playSportsGraph_onlyTU(df_1,only_Path)
    if '来場回数' in df_1.columns:
        make_Ticket_coreFanGraph(df_1,only_Path)
        make_HowManyTimesGraph(df_1,only_Path)
    if 'クーポン有無' in df_f.columns:
            if "クーポンあり" in df_f["クーポン有無"].unique():
                make_TicketPrice_CouponBarGraph_onlyStudents(df_f,full_Path)
    if '性別' in df_1.columns:
        make_genderGraph(df_1,only_Path)
    if '年代' in df_1.columns:
        make_AgeGraph(df_1,only_Path)

def make_data_name(csv_Path):
    name = os.path.basename(csv_Path)
    head = name[:6]
    result_path = os.path.join(settings.MEDIA_ROOT+ head + "result")
    os.makedirs(result_path, exist_ok=True)    # ディレクトリが存在しない場合は作成
    return name,head,result_path

def GraphForApp(csv_Path):
    created_csv_Path = csv_Path.replace("original.csv","full.csv")
    onlyP_csv_Path = csv_Path.replace("original.csv","onlyP.csv")

    # ファイルの存在確認
    if not os.path.isfile(created_csv_Path):
        raise FileNotFoundError(f"File not found: {created_csv_Path}")

    if not os.path.isfile(onlyP_csv_Path):
        raise FileNotFoundError(f"File not found: {onlyP_csv_Path}")

    
    
    make_graph_for_app(created_csv_Path,onlyP_csv_Path)
    
