from apps.app_configure_theme.app_configure_theme import set_theme, get_current_theme
from config.user.microphone.MicrophoneSettings import isDefaultMicrophoneConfigurated, get_saved_microphones, save_microphones
from apps.app_calculate_hertz.app_calculate_hertz import get_gauge, toggle_audio

from content.instruments.InstrumentsConfig import get_instruments_name_strings, get_strings_by_name
from content.tuner.afinacoes.Afinacoes import get_current_afinacao, get_all_tuning_saved, get_current_tuning_notes, \
    get_current_tuning_description, set_current_default_tuning, insert_tuning, delete_tuning_json, \
    get_tuning_description_by_index, get_current_default_tuning, set_tuning_instrument, get_tuning_instrument, \
    get_tuning_index_by_description

import random
import re
import flet as ft
import unicodedata

running = False
value_label = ft.Text("0.00 Hz", size=32, weight=ft.FontWeight.BOLD)
value_caption = ft.Text("--", size=25, color=ft.Colors.ON_SURFACE_VARIANT)
value_expected = ft.Text("0.00 Hz", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY)

MIN_VALUE_WIDTH=1000
MIN_VALUE_HEIGHT=800

gauge, set_value_gauge = get_gauge(value_label, value_caption, value_expected)

def open_afinador(page):

    def update_cordas(e):

        instrumento = e.control.value

        if not instrumento:
            return

        quantidade_cordas = get_strings_by_name(instrumento)

        cordas_container.content = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            tight=True
        )

        for i in range(quantidade_cordas):
            numero_corda = quantidade_cordas - i

            cordas_container.content.controls.append(
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            data="card_container",
                            width=65,
                            content=ft.Text(
                                f"{numero_corda}ª Corda",
                                size=12,
                            ),
                        ),

                        ft.TextField(
                            expand=True,
                            height=40,
                            hint_text=f"Ex: E2",
                            border_radius=6,
                            filled=True,
                            content_padding=ft.Padding.symmetric(
                                horizontal=10,
                                vertical=7,
                            ),
                        ),
                    ],
                )
            )

        set_theme(
            page,
            get_current_theme(),
            root=cordas_container,
            update=False
        )

        page.update()

    def on_window_resized(e):

        if page.window.height == MIN_VALUE_HEIGHT or page.window.width == MIN_VALUE_WIDTH:
            dialog_tuning_select.margin = ft.Margin.symmetric(
            )

            edit_tuning_dialog.margin = ft.Margin.symmetric(
            )

            dialog_tuning_create.margin = ft.Margin.symmetric(
            )

            dialog.margin = ft.Margin.symmetric(
            )

        elif page.window.height > MIN_VALUE_HEIGHT or page.window.width > MIN_VALUE_WIDTH:
            dialog_tuning_select.margin = ft.Margin.symmetric(
                horizontal=page.window.width / 4,
                vertical=page.window.width / 6,
            )

            edit_tuning_dialog.margin = ft.Margin.symmetric(
                horizontal=page.window.width / 4,
                vertical=page.window.width / 6,
            )

            dialog_tuning_create.margin = ft.Margin.symmetric(horizontal=250, vertical=180)

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
        #title_tuning.value = get_current_tuning_description()
        notes_tuning.value = get_current_tuning_notes()

        page.update()

        close_dialog(e, dialog_tuning_select)

    def nota_para_hz(nota):
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

        nome = nota[:-1]
        oitava = int(nota[-1])

        midi = (oitava + 1) * 12 + NOTAS[nome]

        frequencia = 440 * (2 ** ((midi - 69) / 12))

        return round(frequencia, 2)

    def delete_tuning(e, index):
        index_delete = index - 1
        delete_tuning_json(index_delete)

        if get_current_default_tuning() >= index:
            set_current_default_tuning(index)

        page.update()

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

    def remove_accents(texto):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
    )

    def create_tuning(e):

        if not tuning_description:
            tuning_description.border_color = ft.Colors.RED
            tuning_description.label_style = ft.TextStyle(color=ft.Colors.RED)
        if instrument_description.value == "Instrumento":
            instrument_description.border_color = ft.Colors.RED
            instrument_description.label_style = ft.TextStyle(color=ft.Colors.RED)

        if tuning_description and instrument_description.value != "Instrumento":

            notas_existentes = ["Cb","C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]

            notas = []
            notas_do_instrumento = []

            for i, textfield in enumerate(cordas_container.content.controls):
                corda = textfield.controls[1].value

                if len(corda) > 0:

                    # verifica se tem número
                    if any(i.isdigit() and int(i) > 0 for i in re.split('[^0-9]', corda)):

                        verified_string = ""
                        bmol = False

                        correlation_names_to_chord_notation = [
                            ("Do", "C"),
                            ("Re", "D"),
                            ("Mi", "E"),
                            ("Fa", "F"),
                            ("Sol", "G"),
                            ("La", "A"),
                            ("Si", "B")
                        ]

                        for name, chord in correlation_names_to_chord_notation:
                            parts = re.split('[0-9]+', corda)
                            for parte in parts:
                                if parte.isalpha():
                                    parte = remove_accents(parte)

                                    if parte.lower().__contains__("b"):
                                        bmol = True
                                        parte = parte.replace("b", "")
                                        parte = parte.replace("B", "")
                                    if parte == name or parte == chord:
                                        if bmol:
                                            verified_string = f"{chord}b{corda[-1]}"
                                        else:
                                            verified_string = f"{chord}{corda[-1]}"

                        # verifica se tem nota
                        if any(i in notas_existentes for i in re.split('[0-9]+', verified_string)):
                            notas_do_instrumento.append(verified_string)
                            notas.append((verified_string, nota_para_hz(verified_string)))

            if len(notas_do_instrumento) == len(cordas_container.content.controls):
                insert_tuning(tuning_description.value, notas, instrument_description.value)
                close_dialog(e, dialog_tuning_create)

            else:
                for i, textfield in enumerate(cordas_container.content.controls):
                    corda = textfield.controls[1]

                    if i > len(notas_do_instrumento) - 1:
                        corda.border_color = ft.Colors.RED
                        corda.label_style = ft.TextStyle(color=ft.Colors.RED)
                    else:
                        set_theme(page, get_current_theme(), update=None)

                page.update()

            instrument_description.options=[
                ft.DropdownOption(
                    text=inst["nome"]
                )
                for inst in get_instruments_name_strings()
            ]

    def open_dropdown(e, descricao):

        if descricao == " + Criar Afinação":
            open_dialog(e, dialog_tuning_create)
        else:
            change_current_tuning(e, get_tuning_index_by_description(e.control.text))

    cordas_container = ft.Container(
        data="card_container",
        margin=ft.Margin(top=8),
        padding=ft.Padding(
            left=12,
            right=12,
            top=8,
            bottom=8,
        ),
        border_radius=9,
        border=ft.Border.all(1, "#303849"),
    )

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
                ft.Column(
                    [
                        tuning_list_column
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    alignment=ft.MainAxisAlignment.START
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=30
        ),
        visible=False,
    )

    create_tuning_content = [

        ft.Row(
            [
                ft.Column(
                    [
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
                                "até a mais aguda. Enviando também a oitava seguido da nota.",
                                size=13,
                                color="#AEB6C5",
                            ),
                        ),
                    ]
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
                    on_click=lambda e: close_dialog(e, dialog_tuning_create),
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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
            content=ft.Row(
                [
                    ft.Column(
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
                                content_padding=ft.Padding.symmetric(
                                    horizontal=12,
                                    vertical=8,
                                ),
                            ),
                        ],
                    ),

                    ft.Column(
                        spacing=6,
                        controls=[
                            ft.Text(
                                "Instrumento:",
                                size=12,
                                color="#AEB6C5",
                            ),

                            instrument_description := ft.Dropdown(
                                label="Instrumento",
                                options=[
                                    ft.DropdownOption(
                                        text=inst["nome"]
                                    )
                                    for inst in get_instruments_name_strings()
                                ],
                                on_select=update_cordas
                            ),
                        ],
                    )
                ]
            ),
        ),

        ft.Divider(),

        ft.Text(
            "Cordas",
            size=14,
            weight=ft.FontWeight.BOLD,
            color="#DDE3ED",
        ),

        cordas_container,

        ft.Container(
            margin=ft.Margin(top=20),
            data="card_container",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.END,
                spacing=8,

                controls=[

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
    ]

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
            controls=create_tuning_content,
        ),

        visible=False,
    )

    buttons_row = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        scroll=ft.ScrollMode.AUTO,
        height=200,
        tight=True
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
        width=min(page.width * 0.85, 600),
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
                    ],
                    tight=True
                ),
                buttons_row,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            tight=True
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

    afinacoes = get_all_tuning_saved()
    afinacoes.append({"afinacao_descricao": " + Criar Afinação"})
    afinacoes.reverse()

    tuner_button_chooser = ft.Dropdown(
        label="Selecione a Afinação",
        options=[
            ft.DropdownOption(
                text=tuning["afinacao_descricao"],
            )
            for i, tuning in enumerate(afinacoes)
        ],
        border_radius=20,
        on_select=lambda e: open_dropdown(e, e.control.text)
    )

    create_tuning_button = ft.Container(
        content=ft.Text("+", size=15),
        data="card_button",
        width=45,
        height=45,
        bgcolor=ft.Colors.TRANSPARENT,
        alignment=ft.Alignment.CENTER,
        border_radius=20,
        ink=False,
        on_click=lambda e: open_dialog(e, dialog_tuning_create),
    )

    header_row_container = ft.Container(

        ft.Column(
            [
                ft.Row(
                    [
                        title_page,
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
                            tuner_button_chooser,
                            create_tuning_button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    tuner_body,
                    ft.Row(
                        [
                            start_button,
                            ft.Button(
                                ft.Row([ft.Icon(ft.Icons.MIC)]),
                                style=ft.ButtonStyle(
                                    mouse_cursor = ft.MouseCursor.CLICK,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=20
                                ),
                                on_click=open_mic_default_chooser

                            )
                        ],
                    alignment=ft.MainAxisAlignment.CENTER)
                ],
                spacing=10
            ),
            data="card_container_above",
            padding=30,
            border_radius = 20
        ),
    )

    page.on_resize = on_window_resized

    return ft.Stack(
        expand=True,
        controls=[
            content,
            overlay,
        ],
    )