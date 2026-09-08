import flet as ft

def open_tuning(e):

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
        ],
    )

    tuning_header = ft.Container(
        padding=30,
        content=ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Minhas Afinações", size=34, weight=ft.FontWeight.BOLD),
                        ft.Text("Cadastre suas afinações customizadas, ou edite as já geradas.")
                    ],
                    tight=True
                ),
                ft.Button(
                    ft.Text(" + Cadastrar novo Instrumento", size=18),
                    height=70,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=20),
                    ),
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        data="card_container_above",
        border_radius=30,
    ),

    content = ft.Container(
        expand=True,
        padding=20,
        content=ft.Container(
            ft.Column(
                [

                    tuning_header,

                    ft.Divider(),

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

    return ft.Stack(
        expand=True,
        controls=[
            content,
            overlay,
        ],
    )