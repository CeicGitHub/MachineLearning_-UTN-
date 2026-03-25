import flet as ft
import numpy as np
import asyncio

# =========================================================
# CONFIGURACIÓN DE LA COMPUERTA
# Cambia estos valores para reutilizar la misma base
# =========================================================
NOMBRE_COMPUERTA = "AND"
PESOS = np.array([1.0, 1.0])
BIAS = -1.5


# =========================================================
# LÓGICA
# =========================================================
def funcion_activacion(x):
    return 1 if x >= 0 else 0


def evaluar_compuerta(x1, x2):
    entrada = np.array([x1, x2])
    z = np.dot(PESOS, entrada) + BIAS
    y = funcion_activacion(z)
    return z, y


# =========================================================
# EFECTOS VISUALES
# =========================================================
def glow_style(color: str, blur: int = 25):
    return ft.BoxShadow(
        spread_radius=1,
        blur_radius=blur,
        color=color,
    )


async def animar_pulso(page, pulso, x0, y0, x1, y1, pasos=20, delay=0.02):
    pulso.left = x0
    pulso.top = y0
    pulso.visible = True
    page.update()

    for i in range(pasos + 1):
        t = i / pasos
        pulso.left = x0 + (x1 - x0) * t
        pulso.top = y0 + (y1 - y0) * t
        page.update()
        await asyncio.sleep(delay)

    pulso.visible = False
    page.update()


async def resaltar_nodo(page, nodo, color_on, color_off, tiempo=0.12):
    nodo.bgcolor = color_on
    nodo.shadow = glow_style(color_on, 35)
    page.update()
    await asyncio.sleep(tiempo)
    nodo.bgcolor = color_off
    nodo.shadow = glow_style(color_off, 12)
    page.update()


# =========================================================
# APP
# =========================================================
def main(page: ft.Page):
    page.title = f"Compuerta {NOMBRE_COMPUERTA}"
    page.window.width = 980
    page.window.height = 720
    page.padding = 20
    page.bgcolor = "#06101D"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # -----------------------------------------------------
    # TEXTOS
    # -----------------------------------------------------
    titulo = ft.Text(
        f"Visualización simple de compuerta {NOMBRE_COMPUERTA}",
        size=28,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    descripcion = ft.Text(
        "Base reutilizable para AND, OR, NAND, NOR y otras compuertas implementadas con perceptrón.",
        size=14,
        color="#AAB4C3",
    )

    formula = ft.Text(
        "z = x1*w1 + x2*w2 + bias   |   y = activación(z)",
        size=16,
        color="#98A8BC",
    )

    parametros = ft.Text(
        f"Pesos: {PESOS.tolist()}   |   Bias: {BIAS}",
        size=16,
        color="#FFD166",
    )

    estado_txt = ft.Text("Estado: en espera", size=16, color="#B8C7DA")

    valor_x1 = ft.Text("x1 = 0", size=24, color="white", left=50, top=175)
    valor_x2 = ft.Text("x2 = 0", size=24, color="white", left=50, top=330)

    valor_w1 = ft.Text(f"w1 = {PESOS[0]:.2f}", size=22, color="#9BE7FF", left=170, top=175)
    valor_w2 = ft.Text(f"w2 = {PESOS[1]:.2f}", size=22, color="#9BE7FF", left=170, top=330)

    valor_bias = ft.Text(f"bias = {BIAS:.2f}", size=24, color="#FFD166", left=330, top=270)
    valor_z = ft.Text("z = 0.00", size=20, color="white", left=330, top=390)
    valor_y = ft.Text("y = 0", size=30, weight=ft.FontWeight.BOLD, color="white", left=770, top=245)

    valor_resultado = ft.Text("Resultado: -", size=24, color="white")
    tabla_txt = ft.Text("", size=18, color="#CDE7FF")

    # -----------------------------------------------------
    # NODOS
    # -----------------------------------------------------
    input1_node = ft.Container(
        width=34,
        height=34,
        border_radius=17,
        bgcolor="#1A8F3C",
        shadow=glow_style("#1A8F3C", 12),
        left=120,
        top=185,
    )

    input2_node = ft.Container(
        width=34,
        height=34,
        border_radius=17,
        bgcolor="#1A8F3C",
        shadow=glow_style("#1A8F3C", 12),
        left=120,
        top=340,
    )

    soma = ft.Container(
        width=130,
        height=130,
        border_radius=65,
        bgcolor="#2FDB63",
        shadow=glow_style("#39FF6F", 30),
        left=360,
        top=180,
    )

    nucleo = ft.Container(
        width=38,
        height=38,
        border_radius=19,
        bgcolor="#FFF176",
        shadow=glow_style("#FFF176", 22),
        left=406,
        top=226,
    )

    output_node = ft.Container(
        width=40,
        height=40,
        border_radius=20,
        bgcolor="#39FF6F",
        shadow=glow_style("#39FF6F", 18),
        left=820,
        top=245,
    )

    # -----------------------------------------------------
    # CONEXIONES
    # -----------------------------------------------------
    linea_1 = ft.Container(
        width=240,
        height=6,
        bgcolor="#39FF6F",
        border_radius=5,
        left=145,
        top=200,
        shadow=glow_style("#39FF6F", 10),
    )

    linea_2 = ft.Container(
        width=240,
        height=6,
        bgcolor="#39FF6F",
        border_radius=5,
        left=145,
        top=355,
        shadow=glow_style("#39FF6F", 10),
    )

    linea_out = ft.Container(
        width=330,
        height=8,
        bgcolor="#39FF6F",
        border_radius=5,
        left=470,
        top=255,
        shadow=glow_style("#39FF6F", 14),
    )

    # -----------------------------------------------------
    # PULSOS
    # -----------------------------------------------------
    pulso_1 = ft.Container(
        width=18,
        height=18,
        border_radius=9,
        bgcolor="#CCFF33",
        shadow=glow_style("#CCFF33", 25),
        visible=False,
        left=0,
        top=0,
    )

    pulso_2 = ft.Container(
        width=18,
        height=18,
        border_radius=9,
        bgcolor="#CCFF33",
        shadow=glow_style("#CCFF33", 25),
        visible=False,
        left=0,
        top=0,
    )

    pulso_out = ft.Container(
        width=20,
        height=20,
        border_radius=10,
        bgcolor="#00E5FF",
        shadow=glow_style("#00E5FF", 25),
        visible=False,
        left=0,
        top=0,
    )

    # -----------------------------------------------------
    # PANEL VISUAL
    # -----------------------------------------------------
    panel = ft.Container(
        width=920,
        height=500,
        bgcolor="#07111F",
        border_radius=20,
        padding=10,
        content=ft.Stack(
            controls=[
                linea_1,
                linea_2,
                linea_out,
                input1_node,
                input2_node,
                soma,
                nucleo,
                output_node,
                pulso_1,
                pulso_2,
                pulso_out,
                valor_x1,
                valor_x2,
                valor_w1,
                valor_w2,
                valor_bias,
                valor_z,
                valor_y,
            ],
            width=900,
            height=480,
        ),
    )

    # -----------------------------------------------------
    # ENTRADAS
    # -----------------------------------------------------
    input_1 = ft.TextField(label="Input 1", width=120, value="0")
    input_2 = ft.TextField(label="Input 2", width=120, value="0")

    boton_evaluar = ft.ElevatedButton("Evaluar")
    boton_tabla = ft.ElevatedButton("Mostrar tabla")
    boton_limpiar = ft.ElevatedButton("Limpiar")

    controles = ft.Row(
        controls=[input_1, input_2, boton_evaluar, boton_tabla, boton_limpiar],
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
    )

    # -----------------------------------------------------
    # FUNCIONES AUXILIARES
    # -----------------------------------------------------
    def reset_visual():
        valor_x1.value = "x1 = 0"
        valor_x2.value = "x2 = 0"
        valor_z.value = "z = 0.00"
        valor_y.value = "y = 0"
        valor_y.color = "white"
        valor_resultado.value = "Resultado: -"
        estado_txt.value = "Estado: en espera"

        input1_node.bgcolor = "#1A8F3C"
        input1_node.shadow = glow_style("#1A8F3C", 12)

        input2_node.bgcolor = "#1A8F3C"
        input2_node.shadow = glow_style("#1A8F3C", 12)

        soma.bgcolor = "#2FDB63"
        soma.shadow = glow_style("#39FF6F", 30)

        nucleo.bgcolor = "#FFF176"
        nucleo.shadow = glow_style("#FFF176", 22)

        output_node.bgcolor = "#39FF6F"
        output_node.shadow = glow_style("#39FF6F", 18)

        pulso_1.visible = False
        pulso_2.visible = False
        pulso_out.visible = False

        page.update()

    async def animar_evaluacion(x1, x2, y):
        if x1 == 1:
            await resaltar_nodo(page, input1_node, "#B7FF00", "#1A8F3C", 0.12)
            await animar_pulso(page, pulso_1, 136, 191, 355, 220, pasos=22, delay=0.018)

        if x2 == 1:
            await resaltar_nodo(page, input2_node, "#B7FF00", "#1A8F3C", 0.12)
            await animar_pulso(page, pulso_2, 136, 346, 355, 290, pasos=22, delay=0.018)

        soma.bgcolor = "#7CFF6B"
        soma.shadow = glow_style("#7CFF6B", 45)
        nucleo.bgcolor = "#FFF59D"
        nucleo.shadow = glow_style("#FFF59D", 30)
        page.update()
        await asyncio.sleep(0.14)

        soma.bgcolor = "#2FDB63"
        soma.shadow = glow_style("#39FF6F", 30)
        nucleo.bgcolor = "#FFF176"
        nucleo.shadow = glow_style("#FFF176", 22)
        page.update()

        if y == 1:
            valor_y.color = "#00E5FF"
            output_node.bgcolor = "#00E5FF"
            output_node.shadow = glow_style("#00E5FF", 30)
            page.update()

            await animar_pulso(page, pulso_out, 490, 250, 820, 255, pasos=28, delay=0.016)

            output_node.bgcolor = "#39FF6F"
            output_node.shadow = glow_style("#39FF6F", 18)
            page.update()
        else:
            valor_y.color = "white"
            page.update()

    # -----------------------------------------------------
    # EVENTOS
    # -----------------------------------------------------
    async def evaluar_click(e):
        try:
            x1 = int(input_1.value)
            x2 = int(input_2.value)
        except:
            valor_resultado.value = "Resultado: ingresa números enteros"
            page.update()
            return

        if x1 not in [0, 1] or x2 not in [0, 1]:
            valor_resultado.value = "Resultado: usa solo 0 o 1"
            page.update()
            return

        estado_txt.value = "Estado: evaluando entrada"
        valor_x1.value = f"x1 = {x1}"
        valor_x2.value = f"x2 = {x2}"

        z, y = evaluar_compuerta(x1, x2)

        valor_z.value = f"z = {z:.2f}"
        valor_y.value = f"y = {y}"
        page.update()

        await animar_evaluacion(x1, x2, y)

        valor_resultado.value = f"Resultado: {NOMBRE_COMPUERTA}({x1}, {x2}) = {y}"
        estado_txt.value = "Estado: evaluación lista"
        page.update()

    def tabla_click(e):
        filas = []
        for x1 in [0, 1]:
            for x2 in [0, 1]:
                _, y = evaluar_compuerta(x1, x2)
                filas.append(f"{x1}  {x2}  ->  {y}")

        tabla_txt.value = (
            f"Tabla de verdad de {NOMBRE_COMPUERTA}\n\n"
            f"x1 x2 -> y\n"
            + "\n".join(filas)
        )
        page.update()

    def limpiar_click(e):
        input_1.value = "0"
        input_2.value = "0"
        tabla_txt.value = ""
        reset_visual()
        page.update()

    boton_evaluar.on_click = evaluar_click
    boton_tabla.on_click = tabla_click
    boton_limpiar.on_click = limpiar_click

    # -----------------------------------------------------
    # LAYOUT
    # -----------------------------------------------------
    page.add(
        ft.Column(
            controls=[
                titulo,
                descripcion,
                formula,
                parametros,
                controles,
                estado_txt,
                panel,
                valor_resultado,
                tabla_txt,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
        )
    )

    reset_visual()


ft.run(main)