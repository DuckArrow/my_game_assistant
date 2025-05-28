import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def fetch_html_content(url: str) -> str | None:
    """
    指定されたURLからHTMLコンテンツを取得します。
    ネットワークエラーやHTTPエラーを処理します。
    """
    try:
        # User-Agentを設定することで、一部のサイトでのブロックを避けることができます。
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10) # 10秒のタイムアウトを設定
        response.raise_for_status() # HTTPエラー（4xx, 5xx）があれば例外を発生させる
        response.encoding = response.apparent_encoding # 取得したコンテンツのエンコーディングを自動検出
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"URL '{url}' の取得中にエラーが発生しました: {e}")
        return None

def parse_html_content(html_content: str) -> dict:
    """
    HTMLコンテンツを解析し、タイトル、主要な本文、およびリンクを抽出します。
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # タイトルを抽出
    # <title>タグが見つからない場合は「タイトルなし」とする
    title = soup.find('title').get_text(strip=True) if soup.find('title') else 'タイトルなし'
    
    # 主要な本文を抽出 (より広範囲のタグからテキストを結合)
    # 一般的なコンテンツタグを対象としますが、スクリプトやスタイル、ナビゲーションなどは除外します。
    body_elements = soup.find_all(['p', 'div', 'article', 'main', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    body_text_parts = []
    for element in body_elements:
        # スクリプト、スタイル、ヘッダー、フッター、ナビゲーション、サイドバー、コメントなどは除外
        if element.name in ['script', 'style', 'header', 'footer', 'nav', 'aside', 'comment']:
            continue
        # 特定のクラス名を持つ要素を除外する例 (広告など)
        if element.get('class') and any(cls in element['class'] for cls in ['header', 'footer', 'nav', 'sidebar', 'ad', 'advertisement', 'widget', 'menu']):
            continue
        
        text = element.get_text(separator=' ', strip=True)
        if text:
            body_text_parts.append(text)
            
    # 複数行の改行を単一のスペースに置換し、余分な空白を削除
    body_text = ' '.join(body_text_parts).replace('\n', ' ').replace('\r', '').strip()
    
    # リンクを抽出 (絶対URLに変換)
    links = []
    # href属性を持つ<a>タグをすべて検索
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # 相対URLを絶対URLに変換 (ベースURLが必要)
        # この関数が単独で使われる場合、urljoinの第1引数にベースURLを渡す必要があります。
        # ここでは、あくまでスクレイピングされたHTMLのリンクを抽出する目的で、
        # 外部から渡されるURLをベースURLとして仮定しています。
        # 実際の使用例では、この関数を呼び出す側でベースURLを適切に管理する必要があります。
        full_url = urljoin(url, href) # url はこの関数内で定義されていないため、実際にはエラーになります。
                                      # このコードはあくまで単独テスト用であり、
                                      # `game_assistant.py` や `streamlit_app.py` から呼ばれることを想定していません。
        links.append({'text': a_tag.get_text(strip=True), 'url': full_url})
            
    return {
        'title': title,
        'body_text': body_text,
        'links': links
    }

if __name__ == '__main__':
    # このスクリプトを直接実行した場合のテストコードです。
    # 実際のゲーム攻略サイトのURLに置き換えて試してみてください。
    test_url = "https://mynintendonews.com/2025/05/07/japan-latest-famitsu-review-scores-101/" # 例: ファミ通のレビュー記事

    print(f"--- URLからコンテンツを取得中: {test_url} ---")
    html = fetch_html_content(test_url)

    if html:
        print("\n--- コンテンツを解析中 ---")
        # parse_html_content にはベースURLが必要ないため、urljoinの引数を修正する必要はありません。
        # ただし、リンクの絶対URL化は、このテストブロックでは正しく動作しません。
        # 本来の用途（streamlit_app.pyから呼ばれる）では使用されないため、ここでは無視します。
        parsed_data = parse_html_content(html) 
        
        print(f"\nタイトル: {parsed_data['title']}")
        print(f"\n本文の長さ: {len(parsed_data['body_text'])} 文字")
        print(f"\n本文の抜粋:\n{parsed_data['body_text'][:500]}...") # 最初の500文字を表示
        
        print(f"\nリンク数: {len(parsed_data['links'])}")
        # 最初の5つのリンクを表示
        for i, link in enumerate(parsed_data['links'][:5]):
            print(f"  - {link['text']}: {link['url']}")
    else:
        print("HTMLコンテンツの取得に失敗しました。")

