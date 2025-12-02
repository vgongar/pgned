import flet as ft
import re

def main(page: ft.Page):
    # FUNCIONES DE LÓGICA
    def click(e: ft.TapEvent):
        """
        Solo vale para introducir en el modal las coordenadas del click 
        y que el dialogo las recuerde.
        """
        if canvas.mode == "node":
            node_name_modal.click_x = e.local_x
            node_name_modal.click_y = e.local_y
            
            page.open(node_name_modal)

        
    def crear_nodo(e):
        """
        Se llama una vez que hemos escrito el nombre del nodo en el diálogo.
        """
        nombre = node_name_modal.content.value
        x, y = node_name_modal.click_x, node_name_modal.click_y

        node_name_modal.content.value = ""
        page.close(node_name_modal)

        bg_color = ft.Colors.BLUE_50
        accent_color = ft.Colors.BLUE
        node = (
            ft.Container(
                content = (
                        ft.Column(
                            [
                                ft.Text(nombre, text_align="center", size=14, weight=ft.FontWeight.BOLD),
                                
                                ft.Dropdown(
                                    label="Estado",
                                    content_padding=5, 
                                    options=[
                                        ft.dropdown.Option("No"),
                                        ft.dropdown.Option("Sí")
                                    ],
                                    label_style=ft.TextStyle(size=10),
                                    text_size=10
                                    # on_change=dropdown_changed, # Descomentar cuando tengas la función
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ),
                bgcolor=bg_color,
                border_radius=5,
                padding=5
            )
        )

        node.border = ft.border.only(left=ft.border.BorderSide(width=3, color=accent_color))


        gd = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            on_vertical_drag_update=on_pan_update,
            on_tap=on_select_node,
            on_double_tap=abrir_editor_nodo,
            left=x,
            top=y,
            content=node,
        )
        stack = canvas.content.content
        stack.controls.append(gd)
        stack.update()


    def borrar_nodo(e):
        nodo_borrar = e.control.data 

        canvas.content.controls.remove(widget_a_borrar)
        
        canvas.content.update
        canvas.update()


    def on_keyboard(e: ft.KeyboardEvent):
        key = e.key.upper()
        if key == "N":
            canvas.mode = "node"
            text.value = "node"
        elif key == "E":
            canvas.mode = "edge"
            text.value = "edge"
        else:
            canvas.mode = "select"
            text.value = "select"
        text.update()
    

    def on_pan_update(e: ft.DragUpdateEvent):
        if canvas.mode == "select":
            e.control.top = max(0, e.control.top + e.delta_y)
            e.control.left = max(0, e.control.left + e.delta_x)
            e.control.update()
    

    def on_select_node(e):
        if canvas.mode == "select":
            nodo = e.control.content
            nodo.border = ft.border.only(left=ft.border.BorderSide(width=3, color=ft.Colors.RED))
            nodo.update()
    

    def abrir_editor_nodo(e):
        gd = e.control
        nodo = e.control.content
        nombre_nodo = nodo.content.controls[0].value
        prob_si = ft.TextField(value="0.5", text_align="right", width=80, content_padding=5)
        prob_no = ft.TextField(value="0.5", text_align="right", width=80, content_padding=5)
        
        nombre_field = ft.TextField(label="Nombre", value=nombre_nodo)

        editor_nodo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Propiedades del Nodo"),
            content=ft.Column(
                [
                    nombre_field,
                    ft.Divider(),
                    ft.Text("Tabla de Probabilidades (CPT)", weight="bold", size=14),
                    
                    # 3. Editor de Tabla
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Estado")),
                            ft.DataColumn(ft.Text("Probabilidad"), numeric=True),
                        ],
                        rows=[
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("Sí")), 
                                ft.DataCell(prob_si) # TextField incrustado
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("No")), 
                                ft.DataCell(prob_no)
                            ]),
                        ],
                        border=ft.border.all(1, ft.Colors.GREY_300),
                    )
                ],
                tight=True, # Ajusta la altura al contenido
                width=400,  # Ancho fijo para la ventana
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(editor_nodo)),
                ft.TextButton("Guardar", on_click=lambda e: guardar_editor_nodo(dialogo, nombre_field.value)),
            ],
        )

        page.open(editor_nodo)

        

    ### -- INTERFAZ -- ###

    canvas = (
        ft.GestureDetector(
            on_double_tap_down=click,
            content=ft.Container(
                content = ft.Stack([], expand = True),
                width = 500,
                height = 500,
                bgcolor = ft.Colors.BLACK
            )
        )
    )
    # Añadimos un control de estados al canvas para saber en que modo está
    # Opciones posibles "node", "edge", "select"
    canvas.mode = ""
    page.on_keyboard_event = on_keyboard

    text = ft.Text("Hola, por ahora", size=12)

    node_name_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Introduce el nombre del nodo"),
        content=ft.TextField(
            label="Nombre",
            hint_text="Solo letras y números",

            input_filter=ft.InputFilter(
                allow=True, 
                regex_string=r"^[a-zA-Z0-9]*$", 
                replacement_string=""
            ),
            on_submit=crear_nodo
        ),
        on_dismiss=lambda e: print("Modal cerrado"),
    )
    # Inicializamos las variables extra
    node_name_modal.click_x, node_name_modal.click_y = None, None

    page.add(canvas, text)

ft.app(target=main)