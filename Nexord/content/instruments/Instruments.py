import flet as ft

from apps.app_configure_theme.app_configure_theme import set_theme, get_current_theme
from config.user.user_preferences.UserConfig import dont_show_again_delete_instrument, get_delete_instrument_confirm
from content.instruments.InstrumentsConfig import get_all_instruments, insert_new_instrument, favorite_instrument_json, \
    unfavorite_instrument_json, get_all_favorite_instruments, delete_instrument_json, get_instrument_by_index, \
    get_instrument_name_by_index, get_description_name_by_index, get_strings_name_by_index, \
    get_brand_name_by_index, edit_instrument_json


def open_instruments(page: ft.Page):

    def just_digit(e):
        valor = e.control.value

        novo_valor = "".join(c for c in valor if c.isdigit())

        if valor != novo_valor:
            e.control.value = novo_valor
            e.control.update()

    def favorite_instrument_function(e, index):

        container = e.control

        if index not in get_all_favorite_instruments():
            favorite_instrument_json(index)

            container.content = ft.Icon(
                ft.Icons.STAR,
                size=15
            )

        else:
            unfavorite_instrument_json(index)

            container.content = ft.Icon(
                ft.Icons.STAR_BORDER_OUTLINED,
                size=15
            )

        container.update()

    def get_current_icon(index):
        if index in get_all_favorite_instruments():
            return ft.Icon(ft.Icons.STAR, size=15)
        else:
            return ft.Icon(ft.Icons.STAR_BORDER_OUTLINED, size=15)

    def delete_instrument(e, index):

        def delete(index):
            delete_instrument_json(index)
            close_dialog(e, dialog_confirm_exclude)

            reload_page()

        if get_delete_instrument_confirm():
            dialog_confirm_exclude.content = ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("Deletar um Instrumento", size=25),
                                    ft.Text("Tem certeza que quer excluir este instrumento?")
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
                                on_click=lambda e: close_dialog(e, dialog_confirm_exclude),
                            )

                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.Divider(),

                    ft.Column(
                        [
                            ft.Text("Itens a serem excluídos: ", size=15),
                            ft.Text(get_instrument_by_index(index)["instrumento_nome"], size=20)
                        ]
                    ),

                    ft.Row(
                        [
                            ft.Checkbox(
                                on_change=lambda e: dont_show_again_delete_instrument(e),
                                visible=True
                            ),
                            ft.Text("Não perguntar Novamente")
                        ],
                        spacing=3
                    ),

                    ft.Divider(),

                    ft.Row(
                        [
                            confirm_button_delete_instrument := ft.Button(
                                "Sim, tenho certeza",
                                data="card_button",
                                on_click=lambda e: delete(index),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=5),
                                    mouse_cursor=ft.MouseCursor.CLICK
                                )
                            )
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END
                    )

                ],
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                tight=True,
            )

            open_dialog(e, dialog_confirm_exclude)

        else:
            delete_instrument_json(index)
            reload_page(e)

    def reload_page():
        load_instruments()

        set_theme(
            page,
            get_current_theme(),
            root=view,
            update=False
        )

        page.update()

    def insert_instrument(e, dialog):

        descricao = descricao_field.value
        cordas    = cordas_field.value
        marca     = marca_field.value
        nome      = nome_field.value

        if not nome:
            nome_field.border_color = ft.Colors.RED
            nome_field.label_style = ft.TextStyle(color=ft.Colors.RED)
        if not descricao:
            descricao_field.border_color = ft.Colors.RED
            descricao_field.label_style = ft.TextStyle(color=ft.Colors.RED)
        if not marca:
            marca_field.border_color = ft.Colors.RED
            marca_field.label_style = ft.TextStyle(color=ft.Colors.RED)
        if not cordas or any(letra.isalpha() for letra in cordas):
            cordas_field.border_color = ft.Colors.RED
            cordas_field.label_style = ft.TextStyle(color=ft.Colors.RED)

        if nome and descricao and marca and cordas and not any(letra.isalpha() for letra in cordas):
            insert_new_instrument(nome, descricao, marca, cordas)

            close_dialog(e, dialog)
            reload_page()

    def open_dialog(e, dialog):
        barrier.visible = True
        dialog.visible = True
        page.update()

    def close_dialog(e, dialog):
        barrier.visible = False
        dialog.visible = False
        page.update()

    def edit_instrument(e, index):

        def edit(index, name_field, description_field, brand_field, strings_field):

            description = description_field.value
            strings     = strings_field.value
            brand       = brand_field.value
            name        = name_field.value


            if not name:
                name_field.border_color = ft.Colors.RED
                name_field.label_style = ft.TextStyle(color=ft.Colors.RED)
            if not description:
                description_field.border_color = ft.Colors.RED
                description_field.label_style = ft.TextStyle(color=ft.Colors.RED)
            if not brand:
                brand_field.border_color = ft.Colors.RED
                brand_field.label_style = ft.TextStyle(color=ft.Colors.RED)
            if not strings:
                strings_field.border_color = ft.Colors.RED
                strings_field.label_style = ft.TextStyle(color=ft.Colors.RED)

            if name and description and brand and strings:

                edit_instrument_json(index, name, description, brand, strings)
                close_dialog(e, insert_instrument_dialog_edit)

                reload_page()

        insert_instrument_dialog_edit.content = ft.Column(
            [
                # header
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Edite seu Instrumento!", size=25),
                                ft.Text("Edite as informações de seu instrumento por aqui!")
                            ],
                            spacing = 5,
                            tight=True
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
                            on_click=lambda e: close_dialog(e, insert_instrument_dialog_edit),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                ft.Divider(),

                # insert instrument body configurations

                ft.ResponsiveRow(
                    controls=[
                        ft.Column(
                            [
                                ft.Text("Nome do Instrumento:"),
                                nome_field_edit := ft.TextField(
                                    value=get_instrument_name_by_index(index),
                                    hint_text="Ex: Violão Kansas",
                                    label="Nome",
                                ),
                            ],
                            col={"xs": 12, "sm": 6, "md": 3},
                        ),
                        ft.Column(
                            [
                                ft.Text("Descrição do Instrumento:"),
                                descricao_field_edit := ft.TextField(
                                    value=get_description_name_by_index(index),
                                    hint_text="Ex: Meu Primeiro Violão",
                                    label="Descrição",
                                ),
                            ],
                            col={"xs": 12, "sm": 6, "md": 3},
                        ),
                        ft.Column(
                            [
                                ft.Text("Marca do Instrumento:"),
                                marca_field_edit := ft.TextField(
                                    value=get_brand_name_by_index(index),
                                    hint_text="Ex: Tagima, Gibson, Ibanez",
                                    label="Marca",
                                ),
                            ],
                            col={"xs": 12, "sm": 6, "md": 3},
                        ),
                        ft.Column(
                            [
                                ft.Text("Cordas do instrumento:"),
                                cordas_field_edit := ft.TextField(
                                    value=get_strings_name_by_index(index),
                                    hint_text="Ex: 3, 4, 5, 6...",
                                    label="Cordas",
                                    on_change=just_digit,
                                ),
                            ],
                            col={"xs": 12, "sm": 6, "md": 3},
                        ),
                    ],
                    spacing=20,
                    run_spacing=20,
                ),

                ft.Divider(),

                ft.Row(
                    [
                        ft.Button(
                            ft.Text("Concluir"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=5),
                                padding=ft.Padding.symmetric(horizontal=20, vertical=5)
                            ),
                            on_click=lambda e: edit(index, nome_field_edit, descricao_field_edit, marca_field_edit, cordas_field_edit)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                )

            ],
            spacing=30,
            tight=True
        )

        open_dialog(e, insert_instrument_dialog_edit)

    def load_instruments():

        instrumentos_colunas.controls.clear()

        instrumentos = get_all_instruments()

        if len(instrumentos) > 0:
            for i, instrumento in enumerate(instrumentos):
                instrumentos_colunas.controls.append(
                    ft.Container(
                        ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Icon(ft.Icons.EDIT, size=15),
                                            data="card_container",
                                            width=67,
                                            height=34,
                                            bgcolor=ft.Colors.TRANSPARENT,
                                            alignment=ft.Alignment.CENTER,
                                            border_radius=5,
                                            ink=False,
                                            on_click=lambda e, index=i: edit_instrument(e, index + 1),
                                        ),

                                        ft.Column(
                                            [
                                                ft.Column(
                                                    [
                                                        ft.Text(instrumento["instrumento_nome"], size=24, weight=ft.FontWeight.BOLD),
                                                        ft.Column(
                                                            [
                                                                ft.Text("Descrição: " +instrumento["instrumento_descricao"], size=15),
                                                                ft.Text("Marca: " + instrumento["instrumento_marca"], size=12),
                                                            ],
                                                            spacing=2,
                                                        )
                                                    ],
                                                    spacing=1
                                                ),
                                                ft.Text(f"{instrumento["instrumento_quantidade_cordas"]} Cordas")
                                            ]
                                        )
                                    ],
                                    spacing=20
                                ),
                                ft.Row(
                                    [
                                        star_favorite := ft.Container(
                                            content=get_current_icon(i+1),
                                            data="card_container",
                                            width=67,
                                            height=34,
                                            bgcolor=ft.Colors.TRANSPARENT,
                                            alignment=ft.Alignment.CENTER,
                                            border_radius=5,
                                            ink=False,
                                            on_click=lambda e, index=i: favorite_instrument_function(e, index + 1),
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
                                            on_click=lambda e, index=i: delete_instrument(e, index + 1),
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

        else:
            instrumentos_colunas.controls.append(
                ft.Row(
                    [
                        ft.Text("Sem Instrumentos no momento...", size=15)
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

    view = None

    insert_instrument_dialog_edit = ft.Container(
        data="card_container_above",
        width=min(page.width * 0.85, 600),
        bgcolor="#202020",
        border_radius=12,
        padding=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=2,
        ),
        visible=False
    )

    dialog_confirm_exclude = ft.Container(
        data="card_container_above",
        width=min(page.width * 0.85, 600),
        bgcolor="#202020",
        border_radius=12,
        padding=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=2,
        ),
        visible=False,
    )

    insert_instrument_dialog = ft.Container(
        data="card_container_above",
        width=min(page.width * 0.85, 600),
        bgcolor="#202020",
        border_radius=12,
        padding=20,
        shadow=ft.BoxShadow(
            blur_radius=20,
            spread_radius=2,
        ),
        content=ft.Column(
            [
                # header
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Insira seu novo Instrumento!", size=25),
                                ft.Text("Cadastre seu instrumento por aqui, e desfrute do Nexord!")
                            ],
                            spacing = 5,
                            tight=True
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
                            on_click=lambda e: close_dialog(e, insert_instrument_dialog),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

                ft.Divider(),

                # insert instrument body configurations

                ft.ResponsiveRow(
                    controls=[
                        ft.Column(
                            [
                                ft.Text("Nome do Instrumento:"),
                                nome_field := ft.TextField(
                                    hint_text="Ex: Violão Kansas",
                                    label="Nome",
                                ),
                            ],
                            col={"xs": 12, "sm": 6, "md": 3},
                        ),
                        ft.Column(
                            [
                                ft.Text("Descrição do Instrumento:"),
                                descricao_field := ft.TextField(
                                    hint_text="Ex: Meu Primeiro Violão",
                                    label="Descrição",
                                ),
                            ],
                            col={"xs": 12, "sm": 6, "md": 3},
                        ),
                        ft.Column(
                            [
                                ft.Text("Marca do Instrumento:"),
                                marca_field := ft.TextField(
                                    hint_text="Ex: Tagima, Gibson, Ibanez",
                                    label="Marca",
                                ),
                            ],
                            col={"xs": 12, "sm": 6, "md": 3},
                        ),
                        ft.Column(
                            [
                                ft.Text("Cordas do instrumento:"),
                                cordas_field := ft.TextField(
                                    hint_text="Ex: 3, 4, 5, 6...",
                                    label="Cordas",
                                    on_change=just_digit
                                ),
                            ],
                            col={"xs": 12, "sm": 6, "md": 3},
                        ),
                    ],
                    spacing=20,
                    run_spacing=20,
                ),

                ft.Divider(),

                ft.Row(
                    [
                        ft.Button(
                            ft.Text("Concluir"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=5),
                                padding=ft.Padding.symmetric(horizontal=20, vertical=5)
                            ),
                            on_click=lambda e: insert_instrument(e, insert_instrument_dialog)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                )

            ],
            spacing=30,
            tight=True
        ),
        visible=False
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
            insert_instrument_dialog,
            dialog_confirm_exclude,
            insert_instrument_dialog_edit
        ],
    )

    instrumentos_colunas = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    content = ft.Container(
        bgcolor="green",
        expand=True,
        padding=30,
        content=ft.Container(
            ft.Column(
                [
                    instrument_header := ft.Container(
                        padding=30,
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text("Meus Instrumentos", size=34, weight=ft.FontWeight.BOLD),
                                        ft.Text("Cadastre seus instrumentos músicas, ou gerencie-os por este painel")
                                    ],
                                    tight=True
                                ),
                                ft.Button(
                                    ft.Text(" + Cadastrar novo Instrumento", size=18),
                                    height=70,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=20),
                                    ),
                                    on_click=lambda e: open_dialog(e, insert_instrument_dialog)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        data="card_container_above",
                        border_radius=30,
                    ),

                    ft.Divider(),

                    instrumentos_cadastrados := ft.Container(
                        content=instrumentos_colunas,
                        padding=5,
                        expand=True
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
                expand=True,
            ),
            padding=30,
            border_radius=20,
            expand=True,
        ),
    )

    load_instruments()

    view = ft.Stack(
        expand=True,
        controls=[
            content,
            overlay,
        ],
    )

    return view