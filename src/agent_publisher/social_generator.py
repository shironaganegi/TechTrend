import os
import google.generativeai as genai
from dotenv import load_dotenv
import glob
import sys
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Ensure stdout handles unicode
if sys.stdout.encoding:
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key.startswith("your_gemini"):
    print("WARNING: GEMINI_API_KEY is missing. Cannot generate tweets.")
    exit()

genai.configure(api_key=api_key)

def generate_tweet_thread(draft_content):
    """
    Generates a viral-style Twitter thread from the blog post content.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    あなたはXで合計600万インプレッション以上獲得している、技術動向に精通したAIネイティブな日本人テックライターです。
    提供されたブログ記事（ドラフト）に基づき、2026年現在で最もバズりやすいTwitter (X) スレッド（3-5ツイート）を作成してください。

    **ターゲット**: 日本人のエンジニア、テック愛好家、最新ツールに敏感な層。
    **トーン**: 
    - 「友達にLINEで熱く語っている」ような親しみやすさと、プロとしての深い洞察を融合。
    - 自然なネット言葉（「まじで」「ヤバい」「〜すぎる」など）を適度に使用。

    **構成ルール（2026年アルゴリズム最適化）**:
    1. **第1ポスト（フック）**: 
       - 冒頭2行（140文字以内）で、絶対に「さらに表示」を押したくなる強烈なフックを作成。
       - **※重要**: ハッシュタグ（1〜2個）はこの第1ポストの末尾に必ず含めること。
    2. **中盤ポスト**:
       - 役立つ＋ユニークな情報を1枚の図解（テキストによる説明）のように配置。
    3. **最終ポスト**:
       - ブログへの誘導（リンクプレースホルダー: [LINK]）を含める。
       - コメントやリポストを促す行動喚起（CTA）を含める。

    **ハッシュタグ**: 
    - 以下から最も関連性の高いものを選択：`#AI活用`, `#生成AI`, `#エンジニアの日常`, `#AIツール`, `#LLM`

    **画像生成指示**:
    スレッド全体を通して最もバズりそうな画像を1つ提案してください。
    - パターン：コード比較、図解、UI注釈、未来感ビジュアル等。

    **ブログ内容**:
    {draft_content[:6000]}

    **出力形式**:
    [Tweet 1]
    (本文...ハッシュタグはここ)
    ...
    [Tweet N]
    (本文)
    
    [Image Prompt]
    (提案内容と、そのまま使える英語プロンプトをここに出力。※ポスト本文とは分離すること)
    """
    
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # 1. Find the latest draft
    draft_dir = os.path.join(os.path.dirname(__file__), "..", "drafts")
    files = sorted(glob.glob(os.path.join(draft_dir, "draft_*.md")), key=os.path.getmtime, reverse=True)
    
    if not files:
        print("No drafts found. Run analyst agent first.")
        exit()
        
    latest_draft = files[0]
    print(f"Generating tweets for: {os.path.basename(latest_draft)}")
    
    with open(latest_draft, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 2. Generate Thread
    tweets = generate_tweet_thread(content)
    
    # 3. Save Tweets (Simulate Draft)
    base_name = os.path.basename(latest_draft).replace("draft_", "tweets_").replace(".md", ".txt")
    output_path = os.path.join(draft_dir, base_name)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(tweets)
        
    print(f"✅ Tweets saved to: {output_path}")
    print("-" * 30)
    print(tweets)
