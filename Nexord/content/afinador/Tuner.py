from config.user.microphone.MicrophoneSettings import get_microphones, isDefaultMicrophoneConfigurated, save_microphones, get_default_microphone
from apps.app_calculate_hertz.app_calculate_hertz import get_gauge, toggle_audio

import flet as ft

running = False
value_label = ft.Text("0.00 Hz", size=32, weight=ft.FontWeight.BOLD)
value_caption = ft.Text("--", size=25, color=ft.Colors.ON_SURFACE_VARIANT)

gauge, set_value = get_gauge(value_label, value_caption)

def open_afinador(page):

    title = ft.Text(
        "Afinador",
        size=30,
    )

    mic_button = ft.Button(
        ft.Row(
            [
                ft.Icon(ft.Icons.MIC),
                ft.Text("Configurar Microfone")
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        style=ft.ButtonStyle(
            mouse_cursor = ft.MouseCursor.CLICK,
            shape=ft.RoundedRectangleBorder(radius=5)
        ),
    )

    header_row_container = ft.Container(

        ft.Column(
            [
                ft.Row(
                    [
                        title,
                        mic_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],

        ),
        key="card_container_above",
        padding=20,
        border_radius=20,
    )

    start_button = ft.Button(
        "Ligar Afinador",
        on_click=lambda e: toggle_audio(e, value_label, value_caption, start_button, page, set_value, gauge)
    )

    gauge_column = ft.Column(
        [
            ft.Text("Afinador"),
            gauge,
            start_button
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
        spacing=10
    )

    tuner_body = ft.Container(
        ft.Row(
            gauge_column,
            expand=True,
            spacing=10
        ),
        key="card_container_above",
        expand=True,
        border_radius=20
    )

    content = ft.Container(
        expand=True,
        padding=20,
        content=ft.Container(
            ft.Column(
                [
                    header_row_container,
                    tuner_body
                ]
            ),
        ),
    )

    return content