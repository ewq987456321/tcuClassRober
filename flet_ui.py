import flet as ft
from threading import Timer
from datetime import datetime
from main_process.aha import ClassRobber


class Timers(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class Parameter():
    def __init__(self):
        self.running = False
        self.timer = None
        self.page_windows_width = 300
        self.page_windows_height = 550
        self.countDelay = 10


def show_main_page(paramter: Parameter):
    def rob(**kwargs):
        e = kwargs.get('e')
        count_code = list()
        for k in user_input_list:
            if k.value:
                count_code.append(k.value)
        if user_input_student_number.value and user_input_password.value and count_code.__len__():
            robber = ClassRobber(studentNum=user_input_student_number.value,
                                 password=user_input_password.value,
                                 code=count_code)
            now = datetime.now().strftime("%H:%M:%S\n")
            system_output.value += now + robber.all()
        else:
            print('Please input correct user info.')
            if paramter.running:
                handle_stop_button_click('just put it not mean what')
            e.page.snack_bar = ft.SnackBar(
                content=ft.Text('請輸入正確的學號密碼及課程代碼！')
            )
            e.page.snack_bar.open = True
            e.page.update()

    def countDownTimes(e):
        if count_down_text.value == '0':
            rob(e)
            count_down_text.value = paramter.countDelay
        else:
            count_down_text.value = str(int(count_down_text.value) - 1)
            e.page.update()

    def handle_start_button_click(e):
        if user_input_delay_time.value == '':
            e.page.snack_bar = ft.SnackBar(
                content=ft.Text(value='請輸入正確的冷卻時間')
            )
            e.page.snack_bar.open = True
            e.page.update()

        elif int(user_input_delay_time.value) <= 299:
            e.page.snack_bar = ft.SnackBar(
                content=ft.Text(value='冷卻時間需大於299')
            )
            e.page.snack_bar.open = True
            e.page.update()
        elif paramter.timer is None or not paramter.running:
            paramter.countDelay = user_input_delay_time.value
            count_down_text.disabled = True
            e.page.update()
            paramter.timer = Timers(1, countDownTimes, [], {'e': e})
            paramter.timer.start()
            paramter.running = True
            rob()

    def handle_stop_button_click(e):
        count_down_text.value = str(paramter.countDelay)
        paramter.timer.cancel()
        paramter.running = False
        count_down_text.disabled = False
        e.page.update()

    page = []
    page.append(
        ft.AppBar(
            title=ft.Text("Setting"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(
                    icon=ft.icons.SETTINGS,
                    width=paramter.page_windows_width / 2 - 50,
                    on_click=lambda e: e.page.go('/setting'),
                )
            ]
        )
    )
    user_input_student_number = ft.TextField(
        hint_text='113316187', content_padding=ft.padding.only(top=10, left=10),
        width=220, height=30, text_size=15,
        bgcolor=ft.colors.BACKGROUND, border_color=ft.colors.WHITE,
        text_align='left', can_reveal_password=True)
    user_input_password = ft.TextField(
        hint_text='A123456789', content_padding=ft.padding.only(top=10, left=10),
        width=220, height=30, text_size=15,
        bgcolor=ft.colors.BACKGROUND, border_color=ft.colors.WHITE,
        text_align='left', password=True, can_reveal_password=True)
    user_input_delay_time = ft.TextField(
        label='冷卻時間', text_align='right', width=80, height=20, text_size=11, label_style={'size': "13"}
    )
    system_output = ft.TextField(
        multiline=True, height=200, value='', read_only=True)
    count_down_text = user_input_delay_time
    user_input_code1 = ft.TextField(
        label='代碼1', width=110, height=30, text_size=15,
        bgcolor=ft.colors.BACKGROUND, border_color=ft.colors.WHITE,
        text_align='left')
    user_input_code2 = ft.TextField(
        label='代碼2', width=110, height=30, text_size=15,
        bgcolor=ft.colors.BACKGROUND, border_color=ft.colors.WHITE,
        text_align='left')
    user_input_code3 = ft.TextField(
        label='代碼3', width=110, height=30, text_size=15,
        bgcolor=ft.colors.BACKGROUND, border_color=ft.colors.WHITE,
        text_align='left')
    user_input_code4 = ft.TextField(
        label='代碼4', width=110, height=30, text_size=15,
        bgcolor=ft.colors.BACKGROUND, border_color=ft.colors.WHITE,
        text_align='left')
    user_input_list = (user_input_code1, user_input_code2,
                       user_input_code3, user_input_code4)

    page.append(ft.Row([
        ft.Text(value='', width=200),
        count_down_text
    ]))
    page.append(ft.Row([
        ft.Text(value='學號：', width=50),
        user_input_student_number
    ]))
    page.append(ft.Row([
        ft.Text(value='密碼：', width=50),
        user_input_password
    ]))
    page.append(ft.Divider())
    page.append(ft.Text(value='課程代碼：', width=paramter.page_windows_width - 30))
    page.append(ft.Row([
        user_input_code1,
        user_input_code2
    ]))
    page.append(ft.Row([
        user_input_code3,
        user_input_code4
    ]))

    page.append(ft.Row([
        ft.ElevatedButton(text='開始', on_click=handle_start_button_click,
                          width=paramter.page_windows_width / 2 - 50),
        ft.ElevatedButton(text='停止', on_click=handle_stop_button_click,
                          width=paramter.page_windows_width / 2 - 50)
    ]))
    page.append(system_output)
    return page


def show_setting_page():
    page = []
    page.append(
        ft.AppBar(
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK_IOS_SHARP, on_click=lambda e: e.page.go('/')),
            title=ft.Text("Setting"),
            bgcolor=ft.colors.SURFACE_VARIANT
        )
    )
    return page


def main(page: ft.Page):
    paramter = Parameter()

    page.window_width = paramter.page_windows_width
    page.window_height = paramter.page_windows_height

    def on_route_change(route):
        page.views.clear()
        if page.route == '/':
            page.views.append(
                ft.View(
                    '/',
                    [control for control in show_main_page(paramter)]
                )
            )
        elif page.route == '/setting':
            page.views.append(
                ft.View(
                    '/setting',
                    [control for control in show_setting_page()]
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    page.on_view_pop = view_pop
    page.on_route_change = on_route_change
    page.go('/')


ft.app(target=main, assets_dir="assets")
