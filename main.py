import datetime
import json
import os
import flet as ft

#日記アプリ
def main(page: ft.Page):
    
    #日記ファイル名
    file_name = 'diary.json'
    #辞書配列キー(現在時刻を挿入)
    day_date=str(datetime.date.today())
    #辞書配列
    json_data={day_date:["",""]}

    #ファイルが存在するか確認
    if not os.path.isfile(file_name):
        #ファイル生成
        with open(file_name,'w') as file:
            json.dump(json_data, file)
            file.close()
        print(file_name,"を生成しました")
    else:
        #jsonファイルから辞書配列を取得
        with open(file_name,'r') as file:
            json_data = json.load(file)
            file.close()
            #現在時刻のキーが存在しない場合キーを挿入
            if day_date not in json_data:
                with open('diary.json', 'w') as file:
                    json_data[day_date] = ["",""]
                    json.dump(json_data, file)
                    file.close()
        print(file_name,"は既に存在します")

    #日付を変更した時
    def handle_change(e):
        #指定した日付を挿入
        day_date = e.control.value.strftime('%Y-%m-%d')
        select_day.value = day_date
        select_day.update()
        with open(file_name,'r') as file:
            json_data = json.load(file)
            file.close()
        #キーが存在しない場合キーを挿入
        if day_date not in json_data:
            with open('diary.json', 'w') as file:
                json_data[day_date] = ["",""]
                json.dump(json_data, file)
                file.close()
        #日記を更新
        memo0.value = json_data[day_date][0]
        memo1.value = json_data[day_date][1]
        memo0.update()
        memo1.update()
        
    #日記編集
    def edit_diary(e):
        page.bgcolor = ft.colors.WHITE54
        diary_row_control.controls.append(diary_cancel)
        diary_row_control.controls.append(diary_confirm)
        diary_row_control.controls.remove(diary_edit)
        calend.disabled = True
        memo0.read_only=False
        memo1.read_only=False
        memo0.bgcolor = ft.colors.BACKGROUND
        memo1.bgcolor = ft.colors.BACKGROUND
        page.update()
    #日記編集内容確定
    def confirm_diary(e):
        day_date = select_day.value
        page.bgcolor = ft.colors.BACKGROUND
        diary_row_control.controls.append(diary_edit)
        diary_row_control.controls.remove(diary_cancel)
        diary_row_control.controls.remove(diary_confirm)
        calend.disabled = False
        with open(file_name,'r') as file:
            json_data = json.load(file)
            file.close()
        #書き込んだ日記を保存
        with open('diary.json', 'w') as file:
            json_data[day_date] = [memo0.value, memo1.value]
            json.dump(json_data, file)
            file.close()
        memo0.read_only=True
        memo1.read_only=True
        page.update()
    #編集キャンセル
    def cancel_diary(e):
        day_date = select_day.value
        page.bgcolor = ft.colors.BACKGROUND
        diary_row_control.controls.append(diary_edit)
        diary_row_control.controls.remove(diary_cancel)
        diary_row_control.controls.remove(diary_confirm)
        calend.disabled = False
        with open(file_name,'r') as file:
            json_data = json.load(file)
            file.close()
        memo0.value=json_data[day_date][0]
        memo1.value=json_data[day_date][1]
        memo0.read_only=True
        memo1.read_only=True
        page.update()

    #カレンダー用コントロール
    calend=ft.ElevatedButton(
            "カレンダー",
            icon=ft.icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2000, month=1, day=1),
                    last_date=datetime.datetime(year=2038, month=1, day=1),
                    on_change=handle_change,
                    help_text="日付を選択",
                )
            ),
        )
    
    #日記用テキストコントロール
    memo0 = ft.TextField(
        label="タイトル", 
        value=json_data[day_date][0], 
        read_only=True, 
        border="underline", 
        )
    memo1 = ft.TextField(
        label="内容", 
        value=json_data[day_date][1], 
        read_only=True, 
        multiline=True, 
        min_lines=15, 
        max_lines=15, 
        border="none", 
        )
    
    #選択日時保持用テキストコントロール
    select_day = ft.Text(value=str(datetime.date.today()), theme_style=ft.TextThemeStyle.DISPLAY_LARGE)
    #日記編集ボタンコントロール
    diary_edit = ft.FilledTonalButton(text="編集", on_click=edit_diary)
    #日記確定ボタンコントロール
    diary_confirm = ft.FilledTonalButton(text="確定", on_click=confirm_diary)
    #日記キャンセルボタンコントロール
    diary_cancel = ft.FilledTonalButton(text="キャンセル", on_click=cancel_diary)
    diary_row_control = ft.Row(controls=[diary_edit])
    diary_control=ft.Column(controls=[select_day, calend,memo0,memo1,diary_row_control])

    page.add(
        diary_control
    )

ft.app(target=main)