# 🤖 Gemini Chat Application

## 概要
Google の Gemini AI APIを使用したシンプルなチャットアプリケーションです。Fletフレームワークを使用して構築された、クロスプラットフォーム対応のモダンなUIを備えています。

## ✨ 特徴
- 🎯 シンプルで使いやすいUI
- 💬 リアルタイムチャット機能
- 🔄 チャット履歴の保持
- 🌈 レスポンシブデザイン
- ⌨️ キーボードショートカット対応

## 🔧 必要要件
- Python 3.8以上
- pip (Pythonパッケージマネージャー)
- Gemini API Key

## 📦 インストール

### 1. リポジトリのクローン
```bash
git clone https://github.com/yourusername/gemini-chat.git
cd gemini-chat
```

### 2. 必要なパッケージのインストール
```bash
pip install -r requirements.txt
```

または個別にインストール：
```bash
pip install flet google-generativeai python-dotenv
```

### 3. 環境設定
1. `.env`ファイルを作成
2. 以下の内容を追加（APIキーを自身のものに置き換え）

```plaintext
GEMINI_API_KEY=your_api_key_here
```

#### APIキーの取得方法
1. [Google AI Studio](https://makersuite.google.com/app/apikey)にアクセス
2. "Get API Key"をクリック
3. 新しいAPIキーを生成
4. 生成されたキーをコピーして`.env`ファイルに貼り付け

## 🚀 使用方法

### アプリケーションの起動
```bash
python main.py
```

これにより、デフォルトのWebブラウザでアプリケーションが起動します。

### 基本的な使い方
1. テキスト入力欄にメッセージを入力
2. Enterキーを押すか、送信ボタンをクリックしてメッセージを送信
3. AIからの応答を待つ
4. チャット履歴は自動的にスクロールされます

## 🛠️ カスタマイズ

### テーマの変更
`main.py`の以下の部分を修改することでテーマを変更できます：
```python
page.theme_mode = ft.ThemeMode.LIGHT  # または DARK
```

### ウィンドウサイズの変更
デスクトップアプリケーションとして実行する場合：
```python
ft.app(target=main)  # ブラウザではなくデスクトップウィンドウで起動
```

## 📝 注意事項
- APIキーは必ず`.env`ファイルで管理し、直接コードに記載しないでください
- `.env`ファイルはGitにコミットしないよう、`.gitignore`に追加してください
- Gemini APIの利用制限に注意してください

## 🔍 トラブルシューティング

### よくある問題と解決方法
1. "GEMINI_API_KEYが設定されていません"
   - `.env`ファイルが正しい場所に配置されているか確認
   - APIキーが正しく設定されているか確認

2. "モジュールが見つかりません"
   - 必要なパッケージが全てインストールされているか確認
   ```bash
   pip list
   ```

## 👥 コントリビューション
1. このリポジトリをフォーク
2. 機能追加用の新しいブランチを作成
3. 変更をコミット
4. プルリクエストを作成

## 📜 ライセンス
このプロジェクトはMITライセンスの下で公開されています。

## 📮 連絡先
質問や提案がありましたら、Issuesセクションに投稿してください。

---
※ このREADMEは開発中のプロジェクトのため、随時更新される可能性があります。