import flet as ft
import re
import unicodedata

from apps.app_configure_theme.app_configure_theme import set_theme, get_current_theme
from content.application.infra.instruments.InstrumentsConfig import get_instruments_name_strings, get_strings_by_name, \
    get_instrument_name_by_index
from content.application.infra.tuner.afinacoes.Afinacoes import insert_tuning, get_all_tuning_saved, \
    get_tuning_notes_by_index, \
    delete_tuning_json, get_current_default_tuning, set_current_default_tuning, get_tuning_description_by_index, \
    get_tuning_instrument, get_tuning_by_id, edit_tuning_json


def open_tuning(page):
    def edit_tuning(e, index):
        if index >= 1:
            tuning_edit_dialog.content.controls = [

                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(
                                    "Edite sua afinação",
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
                            on_click=lambda e: close_dialog(e, tuning_edit_dialog),
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
                                        value="Nome da Afinação:",
                                        size=12,
                                        color="#AEB6C5",
                                    ),

                                    tuning_description_edit := ft.TextField(
                                        value=get_tuning_description_by_index(index),
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

                                    instrument_description_edit := ft.Dropdown(
                                        value=get_tuning_instrument(get_tuning_by_id(index)),
                                        label="Instrumento",
                                        options=[
                                            ft.DropdownOption(
                                                text=inst["nome"]
                                            )
                                            for inst in get_instruments_name_strings()
                                        ],
                                        on_select=lambda e: update_edit_cordas(e, index)
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

                cordas_container_edit,

                ft.Container(
                    margin=ft.Margin(top=20),
                    data="card_container",
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        spacing=8,

                        controls=[

                            ft.Button(
                                "Editar Afinação",
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
                                on_click=lambda e: update_tuning(e, index, tuning_description_edit,
                                                                 instrument_description_edit, new_notes),
                            ),
                        ],
                    ),
                ),
            ]

            update_edit_cordas(e, index)

            new_notes = []
            for note in cordas_container_edit.content.controls:
               new_notes.append(note.controls[1].value)

    def update_edit_cordas(e, index):

        if (index - 1) >= 0:
            open_dialog(e, tuning_edit_dialog)
            set_theme(page, get_current_theme())

            instrumento = get_instrument_name_by_index(index-1)

            if not instrumento:
                return

            quantidade_cordas = get_strings_by_name(instrumento)
            notas = get_tuning_notes_by_index(index).split(" ")
            notas.pop(len(notas) - 1)

            cordas_container_edit.content = ft.Column(
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                tight=True
            )

            for i in range(quantidade_cordas):
                numero_corda = quantidade_cordas - i


                cordas_container_edit.content.controls.append(
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
                                value=notas[i],
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
                root=cordas_container_edit,
                update=False
            )

        page.update()

    def update_tuning(e, index, description, instrument, notes):
        if description.value == "":
            description.data = "field_wrong"
        else:
            description.data = "field_correct"
        if instrument.value == None:
            instrument.data = "drop_incorrect"
        else:
            instrument.data = "drop_correct"

        set_theme(page, get_current_theme())

        if description.value != "" and instrument.value != "Instrumento":

            notas_existentes = ["Cb", "C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A",
                                "A#", "Bb", "B"]

            notas = []
            notas_do_instrumento = []

            for i, textfield in enumerate(cordas_container_edit.content.controls):
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

                                    base = parte
                                    local_bmol = False

                                    if len(parte) > 1 and parte[-1].lower().__contains__("b"):
                                        local_bmol = True
                                        base = parte[:-1]

                                    if base == name or base == chord:
                                        if local_bmol:
                                            verified_string = f"{chord}b{corda[-1]}"
                                        else:
                                            verified_string = f"{chord}{corda[-1]}"

                        # verifica se tem nota
                        if any(i in notas_existentes for i in re.split('[0-9]+', verified_string)):
                            notas.append((verified_string, nota_para_hz(verified_string)))

            count_valid = 0
            for value in cordas_container_edit.content.controls:
                if value.controls[1].value != "":
                    count_valid += 1

            if len(notes) == count_valid:
                edit_tuning_json(index, description.value, notas, instrument.value)
                close_dialog(e, tuning_edit_dialog)

                afinacoes = get_all_tuning_saved()
                afinacoes.reverse()

            else:
                for i, textfield in enumerate(cordas_container_edit.content.controls):
                    corda = textfield.controls[1]

                    if corda.value not in notes:
                        corda.data = "field_wrong"

                    else:
                        corda.data = "field_correct"
                    set_theme(page, get_current_theme())

        load_tunings()
        page.update()

    def delete_tuning(e, index):
        if index > 1:
            index_delete = index - 1
            delete_tuning_json(index_delete)

            if get_current_default_tuning() >= index:
                set_current_default_tuning(index)

        load_tunings()

    def remove_accents(texto):
        return ''.join(
            c for c in unicodedata.normalize('NFD', texto)
            if unicodedata.category(c) != 'Mn'
        )

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

    def create_tuning(e):

        if tuning_description.value == "":
            tuning_description.data = "field_wrong"
        else:
            tuning_description.data = "field_correct"
        if instrument_description.value == None:
            instrument_description.data = "drop_incorrect"
        else:
            instrument_description.data = "drop_correct"

        set_theme(page, get_current_theme())

        if tuning_description.value != "" and instrument_description.value != "Instrumento":

            notas_existentes = ["Cb", "C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A",
                                "A#", "Bb", "B"]

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

                                    base = parte
                                    local_bmol = False

                                    if len(parte) > 1 and parte[-1].lower().__contains__("b"):
                                        local_bmol = True
                                        base = parte[:-1]

                                    if base == name or base == chord:
                                        if local_bmol:
                                            verified_string = f"{chord}b{corda[-1]}"
                                        else:
                                            verified_string = f"{chord}{corda[-1]}"

                        # verifica se tem nota
                        if any(i in notas_existentes for i in re.split('[0-9]+', verified_string)):
                            notas_do_instrumento.append(verified_string)
                            notas.append((verified_string, nota_para_hz(verified_string)))

            if len(notas_do_instrumento) == len(cordas_container.content.controls):
                insert_tuning(tuning_description.value, notas, instrument_description.value)
                close_dialog(e, tuning_create_dialog)

                afinacoes = get_all_tuning_saved()
                afinacoes.reverse()

            else:
                for i, textfield in enumerate(cordas_container.content.controls):
                    corda = textfield.controls[1]

                    if corda.value not in notas_do_instrumento:
                        corda.data = "field_wrong"

                    else:
                        corda.data = "field_correct"
                    set_theme(page, get_current_theme())

        load_tunings()
        page.update()

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

    def open_dialog(e, dialog):
        barrier.visible = True
        dialog.visible = True
        page.update()

    def close_dialog(e, dialog):
        barrier.visible = False
        dialog.visible = False
        page.update()

    def load_tunings():

        tunings_columns.controls.clear()

        tunings = get_all_tuning_saved()

        for i, tuning in enumerate(tunings):
            tunings_columns.controls.append(
                ft.Container(
                    ft.Row(
                        [
                            ft.Row(
                                [
                                    edit_container := ft.Container(
                                        content=ft.Icon(ft.Icons.EDIT, size=15),
                                        data="card_container",
                                        width=67,
                                        height=34,
                                        bgcolor=ft.Colors.TRANSPARENT,
                                        alignment=ft.Alignment.CENTER,
                                        border_radius=5,
                                        ink=False,
                                        on_click=lambda e, index=i: edit_tuning(e, index)
                                    ),

                                    ft.Column(
                                        [
                                            ft.Column(
                                                [
                                                    ft.Text(tuning["afinacao_descricao"], size=24,
                                                            weight=ft.FontWeight.BOLD),
                                                    ft.Column(
                                                        [
                                                            ft.Text(
                                                                "Instrumento vinculado: " + get_instrument_name_by_index(
                                                                    tuning["afinacao_instrumento"]), size=15),
                                                            ft.Text("Notas: " + get_tuning_notes_by_index(i), size=12),
                                                        ],
                                                        spacing=2,
                                                    )
                                                ],
                                                spacing=1
                                            ),
                                        ]
                                    )
                                ],
                                spacing=20
                            ),
                            delete_container := ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Icon(ft.Icons.CLOSE, size=15),
                                        data="card_container",
                                        width=67,
                                        height=34,
                                        bgcolor=ft.Colors.TRANSPARENT,
                                        alignment=ft.Alignment.CENTER,
                                        border_radius=5,
                                        ink=False,
                                        on_click=lambda e, index=i: delete_tuning(e, index + 1),
                                    )
                                ]
                            )
                        ],
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=20,
                    data=f"card_container_above_{i}",
                    border_radius=10,
                )
            )


        tunings_columns.controls[0].content.controls[0].controls[0].visible = False
        tunings_columns.controls[0].content.controls[1].controls[0].visible = False

        set_theme(page, get_current_theme())

    afinacoes = get_all_tuning_saved()
    afinacoes.reverse()

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
                    on_click=lambda e: close_dialog(e, tuning_create_dialog),
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

    tuning_create_dialog = ft.Container(
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

    edit_tuning_content = []

    cordas_container_edit = ft.Container(
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

    tuning_edit_dialog = ft.Container(
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
            controls=edit_tuning_content,
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
            tuning_create_dialog,
            tuning_edit_dialog
        ],
    )

    tunings_columns = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    content = ft.Container(
        expand=True,
        padding=50,
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("Afinações", weight=ft.FontWeight.BOLD, size=30),
                            ft.Button(
                                ft.Text("Criar Afinações"),
                                style=ft.ButtonStyle(
                                    mouse_cursor=ft.MouseCursor.CLICK,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=20
                                ),
                                on_click=lambda e: open_dialog(e, tuning_create_dialog)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=30,
                    data="card_container_above",
                    border_radius=30,
                ),

                ft.Divider(),

                tunings_content := ft.Container(
                    content=tunings_columns,
                    padding=5,
                    expand=True
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            expand=True,
        ),
    )

    load_tunings()

    return ft.Stack(
        expand=True,
        controls=[
            content,
            overlay,
        ],
    )
