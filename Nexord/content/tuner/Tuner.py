from apps.app_configure_theme.app_configure_theme import set_theme, get_current_theme
from config.user.microphone.MicrophoneSettings import isDefaultMicrophoneConfigurated, get_saved_microphones, save_microphones
from apps.app_calculate_hertz.app_calculate_hertz import get_gauge, toggle_audio

import flet as ft

from content.tuner.afinacoes.Afinacoes import get_current_afinacao, get_all_tuning_saved, get_current_tuning_notes, \
    get_current_tuning_description, set_current_default_tuning, insert_tuning, delete_tuning_json, \
    get_current_default_tuning, get_tuning_description_by_index

running = False
value_label = ft.Text("0.00 Hz", size=32, weight=ft.FontWeight.BOLD)
value_caption = ft.Text("--", size=25, color=ft.Colors.ON_SURFACE_VARIANT)
value_expected = ft.Text("0.00 Hz", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY)

gauge, set_value_gauge = get_gauge(value_label, value_caption, value_expected)

def open_afinador(page):

    def on_window_resized(e):
        dialog_tuning_select.margin = ft.Margin.symmetric(
            horizontal=page.window.width / 4,
            vertical=page.window.width / 6,
        )

        edit_tuning_dialog.margin = ft.Margin.symmetric(
            horizontal=page.window.width / 4,
            vertical=page.window.width / 6,
        )

        dialog_tuning_create.margin = ft.Margin.symmetric(
            horizontal=page.window.width / 4,
            vertical=page.window.width / 6,
        )

        dialog.margin = ft.Margin.symmetric(
            horizontal=page.window.width / 4,
            vertical=page.window.width / 6,
        )


        page.update()

    def edit_tuning(e, index):

        tuning_description = edit_tuning_dialog.content.controls[0].controls[1]

        tuning_description.value = get_tuning_description_by_index(index)
        tuning_description.update()

        set_theme(page, get_current_theme())

        close_dialog(e, dialog_tuning_select)

        open_dialog(e, edit_tuning_dialog)

        pass

    def change_current_tuning(e, index):
        set_current_default_tuning(index)
        title_tuning.value = get_current_tuning_description()
        notes_tuning.value = get_current_tuning_notes()

        page.update()

        close_dialog(e, dialog_tuning_select)

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

        NOTAS_CORDAS = {
            6: "E",
            5: "A",
            4: "D",
            3: "G",
            2: "B",
            1: "E"
        }

        nota_padrao = NOTAS_CORDAS[corda]
        oitava = OITAVAS_CORDAS[corda]

        midi_padrao = (
                (oitava + 1) * 12
                + NOTAS[nota_padrao]
        )

        semitons = NOTAS[nota] - NOTAS[nota_padrao]

        if semitons > 6:
            semitons -= 12
        elif semitons < -6:
            semitons += 12

        midi = midi_padrao + semitons

        frequencia = 440 * (2 ** ((midi - 69) / 12))

        return round(frequencia, 2)

    def delete_tuning(e, index):
        index_delete = index - 1
        delete_tuning_json(index_delete)

        if get_current_default_tuning() >= index:
            set_current_default_tuning(index)

        return_tuning(e)

        page.update()

    def open_select_tuning(e):

        tuning_list_column.controls.clear()

        tuning_list_column.controls.append(new_tuning_button)

        # name button
        for i, afinacao in enumerate(get_all_tuning_saved()):
            tuning_list_column.controls.append(
                ft.Button(
                    ft.Row(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Icon(ft.Icons.CLOSE, size=15),
                                        data="card_button",
                                        width=67,
                                        height=34,
                                        bgcolor=ft.Colors.TRANSPARENT,
                                        alignment=ft.Alignment.CENTER,
                                        border_radius=5,
                                        ink=False,
                                        on_click=lambda e: close_dialog(e, dialog_tuning_select),
                                    ),
                                    ft.Text(afinacao["afinacao_descricao"]),
                                ],
                                spacing=5
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    on_click=lambda e, index=i: change_current_tuning(e, index+1),
                    style=ft.ButtonStyle(
                        mouse_cursor = ft.MouseCursor.CLICK,
                        shape=ft.RoundedRectangleBorder(radius=5),
                        padding=0
                    ),
                )
            )

        # delete button
        for i, button in enumerate(tuning_list_column.controls):
            if i > 1:
                button.content.controls.append(
                    ft.Button(
                        ft.Icon(ft.Icons.DELETE),
                        on_click=lambda e, index=i:delete_tuning(e, index),
                        style=ft.ButtonStyle(
                            mouse_cursor = ft.MouseCursor.CLICK,
                            shape=ft.RoundedRectangleBorder(radius=5),
                        ),
                    )
                )

        set_theme(page, get_current_theme())

        open_dialog(e, dialog_tuning_select)

    def open_tuning_dialog(e):

        close_dialog(e, dialog_tuning_select)

        open_dialog(e, dialog_tuning_create)

    def save_default_and_close(default_mic):
        save_microphones(default_mic)
        if isDefaultMicrophoneConfigurated():
            close_dialog(None, dialog)

    def set_value(e):
        if isDefaultMicrophoneConfigurated() == True:
            toggle_audio(e, value_label, value_caption, value_expected, start_button, page, set_value_gauge, gauge)
        else:
            open_mic_default_chooser(e)

    def open_mic_default_chooser(e):
        barrier.visible = True
        dialog.visible = True
        page.update()

    def close_dialog(e, dialog):
        barrier.visible = False
        dialog.visible = False
        page.update()

    def open_dialog(e, dialog):
        barrier.visible = True
        dialog.visible = True
        page.update()

    def return_tuning(e):
        close_dialog(e, dialog_tuning_create)
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

    edit_tuning_dialog = ft.Container(
        data="card_container_above",
        margin=ft.Margin.symmetric(horizontal=250, vertical=200),
        bgcolor="#202020",
        border_radius=12,
        padding=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=2,
        ),
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row([ft.Text(f"Edite sua Afinação", size=20, weight=ft.FontWeight.W_500), ft.Text("", size=20, weight=ft.FontWeight.BOLD)]),
                        ft.Container(
                            content=ft.Icon(ft.Icons.CLOSE, size=15),
                            data="card_container",
                            width=67,
                            height=34,
                            bgcolor=ft.Colors.TRANSPARENT,
                            alignment=ft.Alignment.CENTER,
                            border_radius=5,
                            ink=False,
                            on_click=lambda e: close_dialog(e, edit_tuning_dialog),
                        )
                    ]
                )

            ],
            tight=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        visible=False,
    )

    tuning_list_column = ft.Column(
        [
            new_tuning_button := ft.Button(
                ft.Text(" + Criar Afinação"),
                data="card_button",
                on_click=open_tuning_dialog,
                style=ft.ButtonStyle(
                    mouse_cursor = ft.MouseCursor.CLICK,
                    shape=ft.RoundedRectangleBorder(radius=5),
                ),
            )
        ],
        spacing=0,
        height=200,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    dialog_tuning_select = ft.Container(
        data="card_container_above",
        margin=ft.Margin.symmetric(horizontal=page.window.width / 4,vertical=page.window.width / 6),
        border_radius=12,
        padding=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=2,
        ),
        content=ft.Column(
            tight=True,
            controls=[

                ft.Row(
                    [
                        ft.Text(
                            "Selecione uma nova afinação",
                            size=22,
                            weight=ft.FontWeight.BOLD,
                        ),

                        ft.Container(
                            content=ft.Icon(ft.Icons.CLOSE, size=15),
                            data="card_container",
                            width=67,
                            height=34,
                            bgcolor=ft.Colors.TRANSPARENT,
                            alignment=ft.Alignment.CENTER,
                            border_radius=5,
                            ink=False,
                            on_click=lambda e: close_dialog(e, dialog_tuning_select),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),

                ft.Text("Escolha uma das opções de afinação listada abaixo:"),
                tuning_list_column,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=30
        ),
        visible=False,
    )

    dialog_tuning_create = ft.Container(
        data="card_container_above",
        margin=ft.Margin.symmetric(horizontal=250, vertical=180),
        bgcolor="#202633",
        border_radius=14,
        padding=24,

        border=ft.Border.all(1, "#394152"),

        shadow=ft.BoxShadow(
            blur_radius=25,
            spread_radius=2,
        ),

        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            tight=True,
            spacing=0,
            controls=[

                ft.Text(
                    "Crie uma nova afinação",
                    size=23,
                    weight=ft.FontWeight.BOLD,
                ),

                ft.Container(
                    data="card_container",
                    margin=ft.Margin(top=6, bottom=20),
                    content=ft.Text(
                        "Configure as notas de cada corda, da mais grave "
                        "até a mais aguda.",
                        size=13,
                        color="#AEB6C5",
                    ),
                ),

                ft.Text(
                    "Informações",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color="#DDE3ED",
                ),

                ft.Container(
                    data="card_container",
                    margin=ft.Margin(top=8, bottom=20),
                    content=ft.Column(
                        spacing=6,
                        controls=[
                            ft.Text(
                                "Descrição da afinação",
                                size=12,
                                color="#AEB6C5",
                            ),

                            tuning_description := ft.TextField(
                                hint_text="Ex: Drop B",
                                height=44,
                                border_radius=7,
                                border_width=1,
                                filled=True,
                                bgcolor="#1A202D",
                                border_color="#3B4353",
                                focused_border_color="#65748A",
                                content_padding=ft.Padding.symmetric(
                                    horizontal=12,
                                    vertical=8,
                                ),
                            ),
                        ],
                    ),
                ),

                ft.Divider(),

                ft.Text(
                    "Cordas",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color="#DDE3ED",
                ),

                ft.Container(
                    data="card_container",
                    margin=ft.Margin(top=8),
                    padding=ft.Padding(
                        left=12,
                        right=12,
                        top=8,
                        bottom=8,
                    ),
                    bgcolor="#1A202D",
                    border_radius=9,
                    border=ft.Border.all(1, "#303849"),

                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        #height=200,
                        tight=True,
                        spacing=8,
                        controls=[

                            ft.Row(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        data="card_container",
                                        width=65,
                                        content=ft.Text(
                                            "6ª Corda",
                                            size=12,
                                            color="#AEB6C5",
                                        ),
                                    ),

                                    sexta_corda := ft.TextField(
                                        expand=True,
                                        height=40,
                                        hint_text="Ex: B",
                                        border_radius=6,
                                        filled=True,
                                        bgcolor="#202633",
                                        border_color="#353E4F",
                                        focused_border_color="#65748A",
                                        content_padding=ft.Padding.symmetric(
                                            horizontal=10,
                                            vertical=7,
                                        ),
                                    ),
                                ],
                            ),

                            ft.Row(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        data="card_container",
                                        width=65,
                                        content=ft.Text(
                                            "5ª Corda",
                                            size=12,
                                            color="#AEB6C5",
                                        ),
                                    ),

                                    quinta_corda := ft.TextField(
                                        expand=True,
                                        height=40,
                                        hint_text="Ex: F#",
                                        border_radius=6,
                                        filled=True,
                                        bgcolor="#202633",
                                        border_color="#353E4F",
                                        focused_border_color="#65748A",
                                        content_padding=ft.Padding.symmetric(
                                            horizontal=10,
                                            vertical=7,
                                        ),
                                    ),
                                ],
                            ),

                            ft.Row(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        data="card_container",
                                        width=65,
                                        content=ft.Text(
                                            "4ª Corda",
                                            size=12,
                                            color="#AEB6C5",
                                        ),
                                    ),

                                    quarta_corda := ft.TextField(
                                        expand=True,
                                        height=40,
                                        hint_text="Ex: B",
                                        border_radius=6,
                                        filled=True,
                                        bgcolor="#202633",
                                        border_color="#353E4F",
                                        focused_border_color="#65748A",
                                        content_padding=ft.Padding.symmetric(
                                            horizontal=10,
                                            vertical=7,
                                        ),
                                    ),
                                ],
                            ),

                            ft.Row(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        data="card_container",
                                        width=65,
                                        content=ft.Text(
                                            "3ª Corda",
                                            size=12,
                                            color="#AEB6C5",
                                        ),
                                    ),

                                    terceira_corda := ft.TextField(
                                        expand=True,
                                        height=40,
                                        hint_text="Ex: E",
                                        border_radius=6,
                                        filled=True,
                                        bgcolor="#202633",
                                        border_color="#353E4F",
                                        focused_border_color="#65748A",
                                        content_padding=ft.Padding.symmetric(
                                            horizontal=10,
                                            vertical=7,
                                        ),
                                    ),
                                ],
                            ),

                            ft.Row(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        data="card_container",
                                        width=65,
                                        content=ft.Text(
                                            "2ª Corda",
                                            size=12,
                                            color="#AEB6C5",
                                        ),
                                    ),

                                    segunda_corda := ft.TextField(
                                        expand=True,
                                        height=40,
                                        hint_text="Ex: B",
                                        border_radius=6,
                                        filled=True,
                                        bgcolor="#202633",
                                        border_color="#353E4F",
                                        focused_border_color="#65748A",
                                        content_padding=ft.Padding.symmetric(
                                            horizontal=10,
                                            vertical=7,
                                        ),
                                    ),
                                ],
                            ),

                            ft.Row(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        data="card_container",
                                        width=65,
                                        content=ft.Text(
                                            "1ª Corda",
                                            size=12,
                                            color="#AEB6C5",
                                        ),
                                    ),

                                    primeira_corda := ft.TextField(
                                        expand=True,
                                        height=40,
                                        hint_text="Ex: E",
                                        border_radius=6,
                                        filled=True,
                                        bgcolor="#202633",
                                        border_color="#353E4F",
                                        focused_border_color="#65748A",
                                        content_padding=ft.Padding.symmetric(
                                            horizontal=10,
                                            vertical=7,
                                        ),
                                    ),
                                ],
                            ),
                        ],
                    ),
                ),

                ft.Container(
                    margin=ft.Margin(top=20),
                    data="card_container",
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=8,

                        controls=[

                            ft.Button(
                                "Voltar",
                                style=ft.ButtonStyle(
                                    bgcolor="#181E29",
                                    color="#D7DCE5",
                                    padding=ft.Padding.symmetric(
                                        horizontal=18,
                                        vertical=10,
                                    ),
                                    shape=ft.RoundedRectangleBorder(
                                        radius=7
                                    ),
                                    mouse_cursor=ft.MouseCursor.CLICK,
                                ),
                                on_click=lambda e: return_tuning(e),
                            ),

                            ft.Button(
                                "Criar Afinação",
                                data="card_button",
                                style=ft.ButtonStyle(
                                    bgcolor="#3B4A61",
                                    color="#FFFFFF",
                                    padding=ft.Padding.symmetric(
                                        horizontal=20,
                                        vertical=10,
                                    ),
                                    shape=ft.RoundedRectangleBorder(
                                        radius=7
                                    ),
                                    mouse_cursor=ft.MouseCursor.CLICK,
                                ),
                                on_click=lambda e: create_tuning(e),
                            ),
                        ],
                    ),
                ),
            ],
        ),

        visible=False,
    )

    buttons_row = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        scroll=ft.ScrollMode.AUTO,
        height=200
    )

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
            ),
        )

    dialog = ft.Container(
        data="card_container_above",
        margin=ft.Margin.symmetric(horizontal=page.window.width / 4,vertical=page.window.width / 6),
        border_radius=12,
        padding=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=2,
        ),
        content=ft.Column(
            controls=[
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    "Defina um Microfone Padrão",
                                    size=25,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Container(
                                    content=ft.Icon(ft.Icons.CLOSE, size=15),
                                    data="card_container",
                                    width=67,
                                    height=34,
                                    bgcolor=ft.Colors.TRANSPARENT,
                                    alignment=ft.Alignment.CENTER,
                                    border_radius=5,
                                    ink=False,
                                    on_click=lambda e: close_dialog(e, dialog),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),

                        ft.Text("Escolha uma das opções de microfones abaixo:"),
                    ]
                ),
                buttons_row,
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
            dialog_tuning_select,
            edit_tuning_dialog
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
        ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Afinação Atual:", size=15),
                        title_tuning := ft.Text(get_current_tuning_description(), size=30, weight=ft.FontWeight.BOLD)
                    ],
                    alignment = ft.MainAxisAlignment.START,
                    spacing=5,
                ),
                ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        data="card_container",
        style=ft.ButtonStyle(
            mouse_cursor = ft.MouseCursor.CLICK,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        width=350,
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
        data="card_container_above",
        padding=20,
        border_radius=20,
    )

    start_button = ft.Button(
        ft.Text("Ligar Afinador"),
        style=ft.ButtonStyle(
            mouse_cursor = ft.MouseCursor.CLICK,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=20
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
        data="card_container",
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
                            tuner_button_chooser
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    tuner_body,
                    ft.Row([start_button],alignment=ft.MainAxisAlignment.CENTER)
                ],
                spacing=10
            ),
            data="card_container_above",
            padding=30,
            border_radius = 20
        ),
    )

    #page.on_resize = on_window_resized

    return ft.Stack(
        expand=True,
        controls=[
            content,
            overlay,
        ],
    )