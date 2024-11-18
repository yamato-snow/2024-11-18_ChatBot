import flet as ft
import google.generativeai as genai
import os
from dotenv import load_dotenv

class ChatMessage(ft.Row):
    """チャットメッセージを表示するためのカスタムコンポーネント"""
    def __init__(self, message: str, is_user: bool = True):
        super().__init__()
        # メッセージの位置を設定（ユーザー：左側、AI：右側）
        self.alignment = "start" if is_user else "end"                
        # メッセージの背景色とテキストの配置を設定
        color = ft.colors.BLUE_100 if is_user else ft.colors.GREEN_100
        alignment = ft.alignment.center_left if is_user else ft.alignment.center_right                
        # メッセージコンテナの作成
        self.controls = [
            ft.Container(
                content=ft.Text(
                    message, 
                    selectable=True,  # テキストを選択可能に
                    size=14,          # フォントサイズ
                ),
                bgcolor=color,
                padding=10,
                border_radius=10,
                alignment=alignment,
                width=400
            )
        ]

class ChatBot(ft.Column):
    """チャットボットのメインコンポーネント"""
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.spacing = 10
        self.scroll = "auto"
        self.expand = True
        
        # Gemini APIの設定と初期化
        self._setup_gemini()
        
        # ローディングインジケータの初期化 (非表示)
        self.loading_indicator = ft.ProgressRing(visible=False)
        
        # ファイルピッカーの初期化
        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)
        
        # UIコンポーネントの初期化
        self._setup_ui()

    def _setup_gemini(self):
        """Gemini APIの設定を行う"""
        # 環境変数からAPIキーを読み込み
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("環境変数 'GEMINI_API_KEY' が設定されていません。.envファイルを確認してください。")
        # Gemini APIの初期化
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-exp-1114")
        self.chat = self.model.start_chat(history=[])

    def _setup_ui(self):
        """UIコンポーネントの初期化を行う"""
        # チャット履歴を表示する領域
        self.chat_history = ft.Column(
            spacing=10,
            scroll="auto",
            expand=True,
            auto_scroll=True
        )

        # メッセージ入力フィールド
        self.message_input = ft.TextField(
            hint_text="メッセージを入力してEnterを押すか、送信ボタンをクリックしてください",
            expand=True,
            multiline=True,  # 複数行入力を許可
            min_lines=1,  # 最小行数を1に設定
            on_change=self.adjust_input_size,  # 入力内容変更時のイベントハンドラを追加
            on_submit=self.send_message,
            autofocus=True,
            border_radius=8
        )

        # 送信ボタン
        self.send_button = ft.IconButton(
            icon=ft.icons.SEND_ROUNDED,
            on_click=self.send_message,
            icon_color=ft.colors.BLUE,
            tooltip="メッセージを送信"
        )

        # ファイル添付ボタン
        self.attach_button = ft.IconButton(
            icon=ft.icons.ATTACH_FILE,
            on_click=self.pick_files,
            icon_color=ft.colors.BLUE,
            tooltip="ファイルを添付"
        )

        # メインレイアウトの設定
        self.controls = [
            self.chat_history,
            ft.Row(
                controls=[
                    self.message_input,
                    self.send_button,
                    self.attach_button  # ファイル添付ボタンを追加
                ],
                alignment="center"
            ),
            self.loading_indicator  # ローディングインジケータを追加
        ]

    def send_message(self, e=None):
        """メッセージを送信し、AIからの応答を取得する"""
        if not self.message_input.value:
            return
        
        # 入力されたメッセージを取得し、入力欄をクリア
        user_message = self.message_input.value.strip()
        self.message_input.value = ""
        self.message_input.min_lines = 1  # 入力ボックスを初期状態に戻す
        self.page.update()

        # ユーザーメッセージの表示
        self.chat_history.controls.append(
            ChatMessage(user_message, is_user=True)
        )
        self.page.update()

        # ローディングインジケータを表示
        self.loading_indicator.visible = True
        self.page.update()

        try:
            # AIからの応答を取得
            response = self.chat.send_message(user_message)
            # AIの応答を表示
            self.chat_history.controls.append(
                ChatMessage(response.text, is_user=False)
            )
        except Exception as e:
            # エラーメッセージを表示
            self.chat_history.controls.append(
                ChatMessage(f"エラーが発生しました: {str(e)}", is_user=False)
            )
        finally:
            # ローディングインジケータを非表示
            self.loading_indicator.visible = False
            self.page.update()
            
    def pick_files(self, e):
        """ファイルを選択する"""
        self.file_picker.pick_files(allow_multiple=False)

    def adjust_input_size(self, e):
        """入力文字数に応じて入力ボックスのサイズを調整する"""
        lines = self.message_input.value.count('\n') + 1
        self.message_input.min_lines = lines
        self.page.update()

def main(page: ft.Page):
    """アプリケーションのメインエントリーポイント"""
    # ページの基本設定
    page.title = "Gemini AI チャットボット"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window.width = 600
    page.window.min_width = 400

    # ダークモード切り替えボタンの設定
    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT
            if page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        page.update()

    # ヘッダーの設定
    page.appbar = ft.AppBar(
        title=ft.Text("Gemini AI チャットボット"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(
                ft.icons.DARK_MODE,
                on_click=toggle_theme,
                tooltip="テーマの切り替え"
            )
        ]
    )

    # チャットボットの初期化と追加
    page.add(ChatBot(page))

if __name__ == "__main__":
    ft.app(target=main)