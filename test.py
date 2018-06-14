from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse
import re
import boto3
import pandas as pd
import requests
import shutil
import csv
from time import sleep
import os

CATEGORY_DIC = {
    473:("スキンケア",
        "クレンジング",
        "洗顔料",
        "ローション",
        "エマルジョン",
        "パック",
        "マッサージ",
        "美容液",
        "美容クリーム",
        "トライアル",
        "ベースメイク",
        "化粧下地",
        "ｺﾝｼ−ﾗ−・ｺﾝﾄﾛ−ﾙｶﾗ−",
        "ファンデーション",
        "パウダータイプ",
        "リキッドタイプ",
        "クリームタイプ",
        "目元＆部分用",
        "フェースパウダー",
        "メイクアップ",
        "アイ",
        "リップ",
        "チーク",
        "バス＆ボディ",
        "ボディソープ",
        "石鹸",
        "入浴料",
        "ボディマッサージ",
        "ボディローション・ジェル",
        "ボディミルク・クリーム",
        "ボディパウダー",
        "ボディ美容液",
        "日やけ止め",
        "ハンドソープ",
        "ハンドクリーム",
        "フットケア",
        "ヘアケア",
        "シャンプー",
        "ｺﾝﾃﾞｨｼｮﾅ−・ﾄﾘ−ﾄﾒﾝﾄ・ﾏｽｸ",
        "育毛剤（スカルプ）",
        "スタイリング・ヘアコロン",
        "香水＆アロマ",
        "香水・コロン",
        "エッセンシャルオイル",
        "ホームフレグランス",
        "雑貨",
        "メイク小物",
        "フェース",
        "バス",
        "一般雑貨",
        "ヘア",
        "アロマ",
        "ギフト袋",
        "ギフトセット",
        "スキンケア",
        "保湿/乾燥・かさつき",
        "センシティブ/ゆらぎ・敏感肌",
        "美白/シミ・ソバカス",
        "エイジング/ハリ・弾力不足",
        "アクネ/ニキビ",
        "角質・毛穴/ザラつき・ベタつき",
        "ベースメイク",
        "美白/シミ・ソバカス・ＵＶ",
        "目元の乾燥・クマ",
        "くすみ・色ムラ",
        "テカリ・ベタつき・化粧崩れ",
        "アクネ/ニキビ",
        "バス＆ボディ",
        "保湿/乾燥・かさつき",
        "美白/シミ・ソバカス・ＵＶ",
        "エイジング/ハリ・弾力不足",
        "アクネ/ニキビ",
        "角質/ザラつき・ごわつき",
        "リフレッシュ/マッサージ",
        "スキンケア",
        "ミルキュア ピュア",
        "マイセンシュア",
        "ユーヴィーシーズ クリアホワイト",
        "ピュアリーホワイト",
        "ポーグレイス",
        "ピュアリーエイジ",
        "エーシーコンフロント",
        "スペシャルケア",
        "ポアクリアジェル",
        "フェイスクリア　ジェル",
        "雑貨（スキンケア）",
        "リファイニングホワイト",
        "ベースメイク",
        "アミュールシフォン",
        "ナチュラル フィニッシュ フルデュアル",
        "ナチュラル フィニッシュ アクネ",
        "雑貨（ベースメイク）",
        "アクネヴェール",
        "メイクアップ",
        "ファイナス",
        "雑貨（メイク）",
        "ロゼジュール",
        "バス＆ボディ",
        "オーベイビー",
        "ブランポート",
        "ドゥ・サージ",
        "リマエナジエ",
        "コリキュアーズ",
        "アロボディ",
        "フットラボ",
        "フルーツパルフェ",
        "カモマイルド",
        "ハーバルメッド",
        "Hand",
        "モイストボディモイスト",
        "その他",
        "ハンドケアシリーズ",
        "へちまスリッパ",
        "雑貨（ボディ）",
        "雑貨（バス）",
        "日本の四季湯",
        "アロマルセット",
        "ヘアケア",
        "カモマイルド",
        "バオバリッチ",
        "アロメディケア",
        "オリーヴィアン",
        "ホホバランス",
        "ハーバルエナジー",
        "その他",
        "雑貨（ヘア）",
        "ナチュラルプラント",
        "オーガニック　OGN",
        "メイプリーゼ",
        "トータルケア",
        "ラ・ローゼ",
        "アクアファヴール マリンハーブスパ",
        "プティビジュー",
        "プティコケット",
        "クラシック プー",
        "エッセンシャルオイル",
        "ビーハニー",
        "ハニーセラム",
        "ローズバレー",
        "ビーハニー",
        "越冬クリーム",
        "クリアランスセール",
        "クラブツリー＆イヴリン",
        "ハンドケア",
        "ハンドクリーム",
        "ハンドウォッシュ",
        "ハンドプライマー",
        "オーバーナイトハンドクリーム",
        "フレグランス",
        "ボディミスト",
        "オードトワレ・オードパヒューム",
        "バス＆ボディ",
        "バス＆シャワージェル",
        "スクラブ",
        "ソープ",
        "ローション・クリーム",
        "パウダー",
        "アットホーム",
        "ホームフレグランス",
        "ファブリック",
        "コレクション",
        "イヴリンローズ",
        "リリー",
        "ローズウォーター",
        "ラベンダー",
        "サマーヒル",
        "ナンタケットブライアー",
        "サマセットメドー",
        "ポメグラネイト",
        "カリビアンアイランド ワイルドフラワーズ",
        "ラソース",
        "アイリス",
        "アボカド",
        "ガーデナーズ",
        "シトロン",
        "バーベナ＆ラベンダー ドゥ プロヴァンス",
        "ペア＆ピンクマグノリア",
        "ノエル",
        "ウィンザーフォレスト",
        "ヘリテージソープ",
        "ホホバ",
        "ギフト",
        "ギフトセット",
        "キャンペーン",
        "バリューサイズ",
        "ハンドクリームフェア",
        "ハンドケア ラグジュアリーキット",
        "スプリングキャンペーン",
        "スキンケア",
        "ベースメイク",
        "メイクアップ",
        "バス＆ボディ",
        "ヘアケア"),
    486:("ヘアケア",
        "頭皮",
        "ハリ・コシ/ボリュームがない",
        "ツヤ感/パサつき",
        "フケ・かゆみ",
        "ダメージ/枝毛・切れ毛",
        "カラーキープ",
        "オーガニック"),
    479:("香水＆アロマ"),
    536:("雑貨",
        "新商品・限定商品"),
    2915:(
        "トータルケア",
        "リフレッシュ・リラックス",
        "限定品"),
    5838:("ギフト袋"),
    469:("季節限定",
        "桜ほの香",
        "スプリングギフト",
        "ラ・ローゼ",
        "ポアクリアジェル",
        "オーベイビー",
        "マーマレードジンジャー",
        "ピンクグレープフルーツ",
        "レモン",
        "グレープフルーツ",
        "ゆず",
        "ミントリープ",
        "シャーベットローション",
        "アクアファヴール マリンハーブスパ",
        "ロゼジュール",
        "ウインターギフト ",
        "プレゼントキャンペーン",
        "クリスマス",
        "クラシックプー X'mas",
        "ハッピーホリデーズ",
        "アミュールシフォン限定パウダー",
        "温活",
        "セラミド",
        "周年祭",
        "限定セット",
        "セール",
        "夏セール",
        "スキンケア",
        "ヘアケア",
        "ボディケア",
        "バラエティ",
        "ビーハニー",
        "冬セール",
        "スキンケア",
        "ヘアケア",
        "ボディケア",
        "バラエティ",
        "ビーハニー",
        "福袋",
        "クリアランスセール",
        "アウトレット",
        "新商品,"
        "限定商品",
        "クリスマス(2014)",
        "2016冬セールテスト",
        "【C&E】ラソース公開時用TOPページtest",
        "【C&E】ペア＆ピンク マグノリア test",
        "【C&E】ペア＆ピンクマグノリア公開時用TOPtest")
}

BRANDS_LIST = {}

SLLEP_SPAN_SECOND = 3

def retry_get_connect(url, session = None):
    if(session is None):
        session = requests.session()
    try_count = 0
    res = None
    while try_count < 3:
        try:
            sleep(SLLEP_SPAN_SECOND)
            print(url)
            res = session.get(url)
            break
        except:
            try_count+=1
    if res is None:
        raise Exception
    return res

def retry_post_connect(url, request, session = None):
    if(session is None):
        session = requests.session()
    try_count = 0
    res = None
    while try_count < 3:
        try:
            sleep(SLLEP_SPAN_SECOND)
            print(url)
            res = session.post(url, data=request)
            break
        except:
            try_count+=1
    if res is None:
        raise Exception
    return res

def put_s3(data):
    iam = _get_user_iam()
    s3 = boto3.client('s3',
                  aws_access_key_id=iam[0],
                  aws_secret_access_key=iam[1],
                  region_name='ap-northeast-1')
    bucket_name = "criteofeed"
    obj_key = "www.hor.jp.csv"
    _create_csv(data)
    s3.put_object(ACL="public-read", Bucket=bucket_name, Key=obj_key, Body=open("./www.hor.jp.csv", 'rb'))

def _create_csv(data):
    header = []
    cr_dir = os.path.dirname(os.path.abspath(__file__))
    with open('{}/criteo_feed_template.csv'.format(cr_dir), 'r') as f:
        header = csv.reader(f,delimiter=";")
        for row in header:
            header = row
            break

    out = []
    for row in data:
        if len(row.keys()) == 0:
            continue
        tmp = []
        for key in header:
           tmp.append(row[key] if(key in row and not row[key] is None) else '')
        out.append(tmp)

    pd.DataFrame(out,columns=header).to_csv('./www.hor.jp.csv', sep=",", encoding="utf-8")

def notice_error(msg):
    iam = _get_user_iam()
    sns = boto3.client(
        "sns",
        aws_access_key_id=iam[0],
        aws_secret_access_key=iam[1],
        region_name='ap-northeast-1')
    request = {
        'TopicArn': 'arn:aws:sns:ap-northeast-1:708034295681:symple_sendmail',
        'Message': msg,
        'Subject': 'www.hor.jpのfeed取得に失敗しました。'
    }
    sns.publish(**request)

def notice_finish():
    iam = _get_user_iam()
    sns = boto3.client(
        "sns",
        aws_access_key_id=iam[0],
        aws_secret_access_key=iam[1],
        region_name='ap-northeast-1')
    request = {
        'TopicArn': 'arn:aws:sns:ap-northeast-1:708034295681:symple_sendmail',
        'Message': "出力内容：https://s3-ap-northeast-1.amazonaws.com/criteofeed/www.hor.jp.csv",
        'Subject': 'www.hor.jpのfeed取得が正常に終了しました'
    }
    sns.publish(**request)

def _get_user_iam():
    return ('AKIAJFQVQWSVG5LJEK7Q',
        '0DaJ1zjjhbGr9413R87OOfSV8wP7xBk5S5pZmyv9')

def _fetch_itemids_all(url, session = None):
    fetch = _fetch_itemids_lis(url, session)
    res = fetch[0]
    lis = fetch[1]

    while len(lis) > 0 and lis[-1].string == '>':
        page_link = lis[-1].contents[0].attrs['href']
        fetch = _fetch_itemids_lis(page_link, session)
        res += fetch[0]
        lis = fetch[1]
    return res

def _fetch_itemids_lis(url, session = None):
    res = retry_get_connect(url, session)
    res.raise_for_status()
    html = res.text        
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("[data-item-id]")
    ids = []
    for item in items:
        item_id = item.attrs["data-item-id"]    
        ids.append(item_id)

    lis = soup.select('#sysMain > div.sysPagination > ul > li')
    return ids,lis


def analyze_item(item_id, disp_flg, session):
    url = 'https://www.hor.jp/i/{}'.format(item_id)
    res = retry_get_connect(url, session)
    #res.raise_for_status()
    html = res.text        
    soup = BeautifulSoup(html, "html.parser")
    res = {}
    res['id'] = item_id
    res['mpn'] = item_id

    tmp = soup.select('#sysMain > article > p')
    if len(tmp) > 0 and tmp[0].get_text() == '商品情報を取得出来ませんでした。':
        return {}

    _tmp = soup.select('title')[0].string.split("｜")
    if len(_tmp) == 0:
        raise Exception('failed find feed')
    
    res['title'] = _tmp[0]
    description = soup.select('head > meta[name="description"]')
    res['description'] = description[0].attrs['content'] if len(description) > 0 else ''
    res['link'] = url
    imgs = soup.select('#sysMain > article div.sysItemImages.sysDisplayKeitaiNone > ul > li > img')
    res['image_link'] = imgs[0].attrs['src']
    res['additional_image_link'] = imgs[1].attrs['src'] if len(imgs) > 1 else None
    price = soup.select('#sysMain > article div.sysBlock.orderArea > div.sysRetailPrice > span:nth-of-type(1)')[0].attrs['data-retail-price']
    price = re.sub(r'[^0-9]', '', price)
    true_price = soup.select('#sysMain > article div.sysBlock.orderArea > div.sysSuggestedRetailPrice')
    true_price = true_price[0].get_text() if len(true_price) > 0 else ''
    true_price = re.sub(r'[^0-9]', '', true_price)
    if true_price == '':
        res['price'] = price
        res['sale_price'] = price
    else :
        res['price'] = true_price
        res['sale_price'] = price

    res['brand'] = BRANDS_LIST[res['id']] if res['id'] in BRANDS_LIST else "ハウスオブローゼ"
    res['adult'] = 'no'
    res['gtin'] = None
    res['product_type'] = None
    res['product_type_key'] = None
    res['number_of_reviews'] = None
    res['product_rating'] = None
    res['filters'] = None

    res['google_product_category'] = None
    cate = soup.select("#sysMain div.sysCategoryPankuzu.sysDisplayKeitaiNone > a")[-1].get_text()
    for k, keywords in CATEGORY_DIC.items():
        if cate in keywords:
            res['google_product_category'] = k
            break

    # 表示非表示判断
    disp_flg = False if cate == "ギフト袋" else disp_flg
    disp_flg = False if re.match('非表示', res['title']) else disp_flg
    disp_flg = False if len(soup.select('#sysNumber > select > option')) == 0 else disp_flg
    res['availability'] = "in stock" if disp_flg else "out of stock"
    return res

def get_login_session():
    login_info = {
        'mailaddress':'shogo.yamamoto@reservele.com',
        'member_password':'kQ9VaM3Z',
        'action_front_mypage_login':'true'
    }
    session = requests.session()
    res = retry_post_connect('https://ssl.aispr.jp/houseofrose/mypage/', login_info, session)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.text, "html.parser")
    if len(soup.select_one('#sysHeader > div.sysFuncMemberLogin.mypage_point > div > div:nth-of-type(1)')) == 0:
        raise Exception('failed login action')

    # 外部認証サービスを利用しているので、session_idをリクエストで渡す
    res = retry_get_connect("https://www.hor.jp?action_front_mypage_index=true&SID={}".format(session.cookies.get('SID')), session)
    res.raise_for_status()

    return session

def fetch_itemids(session=None):
    params = urllib.parse.urlencode({
        'price_range_start': 0,
        'price_range_end': 3000,
        'sort': 0,
        'limit': 150,
        'p': 0
    })
    item_ids = _fetch_itemids_all("https://www.hor.jp/is/?{}".format(params),session)

    params = urllib.parse.urlencode({
        'price_range_start': 3000,
        'price_range_end': '',
        'sort': 0,
        'limit': 150,
        'p': 0
    })
    item_ids += _fetch_itemids_all("https://www.hor.jp/is/?{}".format(params),session)

    return item_ids

def set_brand_list(session):
    res = retry_get_connect('https://www.hor.jp', session)
    soup = BeautifulSoup(res.text, "html.parser")
    for li in soup.select('#sysFooter > div.sysFuncText.f_brand.sysDisplayMobileNone.sysDisplayTabletNone > div > div > ul > li'):
        brand_str = li.find('img').attrs['alt']
        for id in _fetch_itemids_all('https://www.hor.jp{}'.format(li.find('a').attrs['href'])):
            BRANDS_LIST[id] = brand_str

def execute():
    session = get_login_session()
    set_brand_list(session)

    public_items = fetch_itemids()

    # 会員限定商品(会員にあって、非会員にはない)
    all_items = fetch_itemids(session)
    private_items = [x for x in all_items if x not in public_items]

    data = []
    for item in public_items:
        print('public:{}----'.format(item))
        data.append(analyze_item(item, True, session))

    for item in private_items:
        print('private:{}----'.format(item))
        data.append(analyze_item(item, False, session))

    for item in all_items:
        print('test:{}----'.format(item))
        # テストページの画面構成が各々違うように見える
        try:
            data.append(analyze_item("test"+item, False, session))
        except:
            print('NG')

    put_s3(data)

# -------------------------------------------
try:
    # print(analyze_item(34379, False, session=requests.session()))
    execute()
    notice_finish()
except:
    import traceback
    msg = traceback.format_exc()
    print(msg)
    notice_error(msg)
    
    
    
#test
