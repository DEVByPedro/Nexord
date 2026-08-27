from config.user.microphone.MicrophoneSettings import isDefaultMicrophoneConfigurated, get_saved_microphones, save_microphones
from apps.app_calculate_hertz.app_calculate_hertz import get_gauge, toggle_audio

import flet as ft

from content.afinador.afinacoes.Afinacoes import get_current_afinacao, get_all_tuning_saved, get_current_tuning_notes, \
    get_current_tuning_description, set_current_default_tuning, insert_tuning

running = False
value_label = ft.Text("0.00 Hz", size=32, weight=ft.FontWeight.BOLD)
value_caption = ft.Text("--", size=25, color=ft.Colors.ON_SURFACE_VARIANT)

gauge, set_value_gauge = get_gauge(value_label, value_caption)

def open_afinador(page):

    def change_current_tuning(e, index):
        set_current_default_tuning(index)
        title_tuning.value = get_current_tuning_description()
        notes_tuning.value = get_current_tuning_notes()

        page.update()

        close_tuning_create_dialog(e)

    def nota_para_hz(corda, nota):
        NOTAS = {
            "C": 0,
            "C#": 1,
            "Db": 1,
            "D": 2,
            "D#": 3,
            "Eb": 3,
            "E": 4,
            "Fb": 4,
            "F": 5,
            "F#": 6,
            "Gb": 6,
            "G": 7,
            "G#": 8,
            "Ab": 8,
            "A": 9,
            "A#": 10,
            "Bb": 10,
            "B": 11,
            "Cb": 11,
        }

        OITAVAS_CORDAS = {
            6: 2,
            5: 2,
            4: 3,
            3: 3,
            2: 3,
            1: 4
        }



        oitava = OITAVAS_CORDAS[corda]

        midi = (oitava + 1) * 12 + NOTAS[nota]
        frequencia = 440 * (2 ** ((midi - 69) / 12))
        return float(f"{frequencia:.2f}")

    def open_select_tuning(e):

        tuning_list_column.controls.clear()

        tuning_list_column.controls.append(new_tuning_button)

        for i, afinacao in enumerate(get_all_tuning_saved()):
            tuning_list_column.controls.append(
                ft.Button(
                    ft.Text(afinacao["afinacao_descricao"]),
                    on_click=lambda e, index=i: change_current_tuning(e, index+1),
                    style=ft.ButtonStyle(
                        mouse_cursor = ft.MouseCursor.CLICK,
                        shape=ft.RoundedRectangleBorder(radius=5),
                    ),
                )
            )


        barrier.visible = True
        dialog_tuning_select.visible = True
        page.update()

    def close_tuning_create_dialog(e):
        barrier.visible = False
        dialog_tuning_select.visible = False
        page.update()

    def open_tuning_dialog(e):

        close_tuning_create_dialog(e)

        barrier.visible = True
        dialog_tuning_create.visible = True
        page.update()

    def close_tuning_dialog(e):
        barrier.visible = False
        dialog_tuning_create.visible = False
        page.update()

    def save_default_and_close(default_mic):
        save_microphones(default_mic)
        if isDefaultMicrophoneConfigurated():
            fechar()

    def set_value(e):
        if isDefaultMicrophoneConfigurated() == True:
            toggle_audio(e, value_label, value_caption, start_button, page, set_value_gauge, gauge)
        else:
            open_mic_default_chooser(e)

    def open_mic_default_chooser(e):
        barrier.visible = True
        dialog.visible = True
        page.update()

    def fechar():
        barrier.visible = False
        dialog.visible = False
        page.update()

    def return_tuning(e):
        close_tuning_dialog(e)
        open_select_tuning(e)

    def create_tuning(e):
        notas = [
            [sexta_corda.value, nota_para_hz(6, sexta_corda.value)],
            [quinta_corda.value, nota_para_hz(5, quinta_corda.value)],
            [quarta_corda.value, nota_para_hz(4, quarta_corda.value)],
            [terceira_corda.value, nota_para_hz(3, terceira_corda.value)],
            [segunda_corda.value, nota_para_hz(2, segunda_corda.value)],
            [primeira_corda.value, nota_para_hz(1, primeira_corda.value)],
        ]

        if tuning_description != "":
            insert_tuning(tuning_description.value, notas)
            return_tuning(e)

    tuning_list_column = ft.Column(
        [
            new_tuning_button := ft.Button(
                ft.Text(" + Criar Afinação"),
                key="card_button",
                on_click=open_tuning_dialog,
                style=ft.ButtonStyle(
                    mouse_cursor = ft.MouseCursor.CLICK,
                    shape=ft.RoundedRectangleBorder(radius=5),
                ),
            )
        ],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    dialog_tuning_select = ft.Container(
        key="card_container_above",
        width=400,
        bgcolor="#202020",
        border_radius=12,
        padding=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=2,
        ),
        content=ft.Column(
            tight=True,
            controls=[
                ft.Text(
                    "Selecione uma nova afinação",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text("Escolha uma das opções de afinação listada abaixo:"),
                ft.Container(
                    content=tuning_list_column,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Button(
                            "Fechar",
                            key="close_button",
                            style=ft.ButtonStyle(
                                mouse_cursor = ft.MouseCursor.CLICK,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            ),
                            on_click=lambda e: close_tuning_create_dialog(e),
                        )
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        visible=False,
    )

    dialog_tuning_create = ft.Container(
        key="card_container_above",
        bgcolor="#202020",
        width=400,
        border_radius=12,
        padding=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=2,
        ),
        content=ft.Column(
            tight=True,
            controls=[
                ft.Text(
                    "Crie uma nova afinação",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text("Configure sua nova afinação, da mais grave até a mais agúda:"),

                ft.Column(
                    [
                        ft.Column([ft.Text("Descrição da Afinação:"), tuning_description := ft.TextField()]),
                        ft.Column(
                            [
                                ft.Text("Cordas:"),
                                ft.Row([ft.Text("6 Corda:"), sexta_corda := ft.TextField()]),
                                ft.Row([ft.Text("5 Corda:"), quinta_corda := ft.TextField()]),
                                ft.Row([ft.Text("4 Corda:"), quarta_corda := ft.TextField()]),
                                ft.Row([ft.Text("3 Corda:"), terceira_corda := ft.TextField()]),
                                ft.Row([ft.Text("2 Corda:"), segunda_corda := ft.TextField()]),
                                ft.Row([ft.Text("1 Corda:"), primeira_corda := ft.TextField()]),
                            ]
                        )
                    ]
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Button(
                            "Voltar",
                            style=ft.ButtonStyle(
                                mouse_cursor = ft.MouseCursor.CLICK,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            ),
                            on_click=lambda e: return_tuning(e),
                        ),
                        ft.Button(
                            "Criar Afinação",
                            key="card_button",
                            style=ft.ButtonStyle(
                                mouse_cursor = ft.MouseCursor.CLICK,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            ),
                            on_click=lambda e: create_tuning(e),
                        ),
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=20
        ),
        visible=False,
    )

    buttons_row = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    for button in get_saved_microphones()["all_microphones"]:
        buttons_row.controls.append(
            ft.Button(
                button["name"],
                style=ft.ButtonStyle(
                    mouse_cursor = ft.MouseCursor.CLICK,
                    shape=ft.RoundedRectangleBorder(radius=5),
                ),
                expand=True,
                on_click=lambda e, name=button["name"]: save_default_and_close(name)
            )
        )

    dialog = ft.Container(
        key="card_container_above",
        width=400,
        height=250,
        bgcolor="#202020",
        border_radius=12,
        padding=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=2,
        ),
        content=ft.Column(
            controls=[
                ft.Text(
                    "Defina um Microfone Padrão",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Text("Escolha uma das opções de microfones abaixo:"),
                buttons_row,
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Button(
                            "Fechar",
                            key="close_button",
                            style=ft.ButtonStyle(
                                mouse_cursor = ft.MouseCursor.CLICK,
                                shape=ft.RoundedRectangleBorder(radius=5),
                            ),
                            on_click=lambda e: fechar(),
                        )
                    ],
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        visible=False,
    )

    barrier = ft.Container(
        bgcolor="#80000000",
        opacity=0.7,
        expand=True,
        visible=False,
    )

    overlay = ft.Stack(
        expand=True,
        alignment=ft.Alignment.CENTER,
        controls=[
            barrier,
            dialog,
            dialog_tuning_create,
            dialog_tuning_select
        ],
    )

    title_page = ft.Text(
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
        on_click=open_mic_default_chooser
    )

    tuner_button_chooser = ft.Button(
        title_tuning := ft.Text(get_current_tuning_description(), size=30, weight=ft.FontWeight.BOLD),
        key="card_container",
        style=ft.ButtonStyle(
            mouse_cursor = ft.MouseCursor.CLICK,
            shape=ft.RoundedRectangleBorder(radius=5)
        ),
        on_click=open_select_tuning
    )

    header_row_container = ft.Container(

        ft.Column(
            [
                ft.Row(
                    [
                        title_page,
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
        ft.Text("Ligar Afinador"),
        style=ft.ButtonStyle(
            mouse_cursor = ft.MouseCursor.CLICK,
            shape=ft.RoundedRectangleBorder(radius=5)
        ),
        on_click=lambda e: set_value(e)
    )

    afinacoes_lista = get_all_tuning_saved()


    gauge_column = ft.Column(
        [
            notes_tuning := ft.Text(get_current_tuning_notes()),
            gauge
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
        spacing=10
    )

    tuner_body = ft.Container(
        ft.Row(
            gauge_column,
            expand=True,
            spacing=10
        ),
        key="card_container",
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
                    ft.Container(),
                    ft.Row(
                        [
                            ft.Text("Afinação:", size=30, weight=ft.FontWeight.BOLD),
                            tuner_button_chooser
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    tuner_body,
                    ft.Row([start_button],alignment=ft.MainAxisAlignment.CENTER)
                ],
                spacing=10
            ),
            key="card_container_above",
            padding=30,
            border_radius = 20
        ),
    )

    return ft.Stack(
        expand=True,
        controls=[
            content,
            overlay,
        ],
    )