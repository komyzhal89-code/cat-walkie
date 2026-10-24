import flet as ft

def main(page: ft.Page):
    # 아이폰 화면 비율에 맞춘 설정
    page.title = "냥냥 무전기"
    page.window.width = 390
    page.window.height = 780
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FFF8F0"  # 따뜻한 아이보리 톤

    # 상태 관리 변수들
    current_channel = ft.Ref[ft.Text]()
    status_text = ft.Ref[ft.Text]()
    ptt_button = ft.Ref[ft.Container]()
    ptt_label = ft.Ref[ft.Text]()
    cat_status_icon = ft.Ref[ft.Text]()

    # 상단 타이틀 바
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("🐾", size=24),
                        ft.Text("냥냥 무전기", size=18, weight=ft.FontWeight.BOLD, color="#5D4037"),
                    ],
                    spacing=8,
                ),
                ft.Container(
                    content=ft.Text("온라인 (3명)", size=12, color="#4CAF50", weight=ft.FontWeight.BOLD),
                    bgcolor="#E8F5E9",
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=12,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        ),
        bgcolor="#FFE0B2",
        padding=ft.padding.all(16),
    )

    # 현재 채널 및 상태 카드
    status_card = ft.Card(
        elevation=2,
        color="#FFFFFF",
        content=ft.Container(
            padding=16,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("현재 채널", size=12, color="#8D6E63"),
                            ft.Text(ref=current_channel, value="[CH 1] 카운터 & 음료", size=15, weight=ft.FontWeight.BOLD, color="#5D4037"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Divider(height=10, color="#E0E0E0"),
                    ft.Row(
                        controls=[
                            ft.Text(ref=cat_status_icon, value="🐱", size=28),
                            ft.Column(
                                controls=[
                                    ft.Text(ref=status_text, value="대기 중... (버튼을 누르고 말하세요)", size=13, color="#757575"),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=12,
                        alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=8,
            ),
        ),
    )

    # PTT 버튼 동작 (누를 때 / 뗄 때)
    def on_ptt_press(e):
        ptt_button.current.bgcolor = "#FF5252"
        ptt_label.current.value = "🎙️ 송신 중..."
        ptt_label.current.color = "#FFFFFF"
        status_text.current.value = "내 목소리가 매장에 전달되고 있습니다!"
        status_text.current.color = "#D32F2F"
        cat_status_icon.current.value = "📢"
        page.update()

    def on_ptt_release(e):
        ptt_button.current.bgcolor = "#FFB74D"
        ptt_label.current.value = "🐾 누르고 말하기"
        ptt_label.current.color = "#5D4037"
        status_text.current.value = "대기 중... (버튼을 누르고 말하세요)"
        status_text.current.color = "#757575"
        cat_status_icon.current.value = "🐱"
        page.update()

    # 채널 변경 함수
    def change_channel(channel_name):
        current_channel.current.value = channel_name
        page.update()

    def make_channel_btn(name, icon):
        return ft.ElevatedButton(
            content=ft.Row([ft.Text(icon, size=16), ft.Text(name, size=13, weight=ft.FontWeight.BOLD, color="#5D4037")]),
            style=ft.ButtonStyle(
                bgcolor="#FFF3E0",
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
            ),
            on_click=lambda _: change_channel(f"{icon} {name}"),
        )

    # PTT 발바닥 버튼
    ptt_container = ft.GestureDetector(
        on_tap_down=on_ptt_press,
        on_tap_up=on_ptt_release,
        content=ft.Container(
            ref=ptt_button,
            width=180,
            height=180,
            bgcolor="#FFB74D",
            shape=ft.BoxShape.CIRCLE,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                blur_radius=15,
                spread_radius=2,
                color="#FFCC80",
                offset=ft.Offset(0, 5),
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAuthority.CENTER if hasattr(ft, 'CrossAuthority') else ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("🐾", size=50),
                    ft.Text(ref=ptt_label, value="누르고 말하기", size=15, weight=ft.FontWeight.BOLD, color="#5D4037"),
                ],
                spacing=5,
            ),
        ),
    )

    # 긴급 알림 버튼
    def on_emergency_click(e):
        dlg = ft.AlertDialog(
            title=ft.Text("🚨 긴급 상황 발생!"),
            content=ft.Text("매장에 긴급 알림을 전송하시겠습니까?"),
            actions=[
                ft.TextButton("취소", on_click=lambda _: page.close(dlg)),
                ft.TextButton("알림 전송", on_click=lambda _: page.close(dlg)),
            ],
        )
        page.open(dlg)

    emergency_btn = ft.Container(
        content=ft.ElevatedButton(
            content=ft.Row([ft.Text("🚨", size=16), ft.Text("긴급 / 돌발상황 알림", size=13, color="#FFFFFF", weight=ft.FontWeight.BOLD)]),
            style=ft.ButtonStyle(bgcolor="#FF5252", shape=ft.RoundedRectangleBorder(radius=10)),
            on_click=on_emergency_click,
        ),
        alignment=ft.alignment.center,
    )

    # 전체 UI 배치
    page.add(
        header,
        ft.Container(
            padding=16,
            content=ft.Column(
                controls=[
                    status_card,
                    ft.Text("채널 선택", size=13, weight=ft.FontWeight.BOLD, color="#8D6E63"),
                    ft.Row(
                        controls=[
                            make_channel_btn("카운터/음료", "🍹"),
                            make_channel_btn("홀/테이블", "☕"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    ft.Row(
                        controls=[
                            make_channel_btn("냥이케어/간식", "🍗"),
                            make_channel_btn("전체 방송", "📢"),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    ),
                    ft.Container(height=10),
                    ft.Container(content=ptt_container, alignment=ft.alignment.center),
                    ft.Container(height=10),
                    emergency_btn,
                ],
                spacing=12,
            ),
        ),
    )

ft.app(target=main)