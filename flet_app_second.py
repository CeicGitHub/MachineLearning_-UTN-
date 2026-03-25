import flet as ft
import numpy as np
import asyncio

# -------------------------------------------------
# LÓGICA DEL PERCEPTRÓN
# -------------------------------------------------
def funcion_activacion(x):
    return 1 if x >= 0 else 0

def predecir(input_1, input_2, pesos, bias):
    x_input = np.array([input_1, input_2])
    z = np.dot(pesos, x_input) + bias
    return funcion_activacion(z)

# -------------------------------------------------
# EFECTOS VISUALES
# -------------------------------------------------
def glow_style(color: str, blur: int = 30):
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


async def resaltar_nodo(page, nodo, color_encendido, color_apagado, tiempo=0.15):
    nodo.bgcolor = color_encendido
    nodo.shadow = glow_style(color_encendido, 35)
    page.update()
    await asyncio.sleep(tiempo)
    nodo.bgcolor = color_apagado
    nodo.shadow = glow_style(color_apagado, 12)
    page.update()


# -------------------------------------------------
# APLICACIÓN PRINCIPAL
# -------------------------------------------------
def main(page: ft.Page):
    page.title = "Perceptrón AND Animado"
    page.window.width = 1000
    page.window.height = 720
    page.padding = 20
    page.bgcolor = "#050816"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Estado interno
    pesos_entrenados = None
    bias_entrenado = None
    entrenando = False

    # Datos AND
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([0, 0, 0, 1])

    # -------------------------------------------------
    # TEXTOS PRINCIPALES
    # -------------------------------------------------
    titulo = ft.Text(
        "Perceptrón Animado - Compuerta AND",
        size=28,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    subtitulo = ft.Text(
        "Visualización del entrenamiento y de la predicción",
        size=14,
        color="#AAB4C3",
    )

    estado_txt = ft.Text("Estado: En espera", size=16, color="#B8C7DA")

    epoca_txt = ft.Text("Época: 0", size=24, color="white", left=30, top=20)
    z_txt = ft.Text("z = 0.00", size=18, color="white", left=350, top=410)
    error_txt = ft.Text("error = 0", size=18, color="white", left=350, top=440)

    valor_x1 = ft.Text("x1 = 0", size=24, color="white", left=50, top=185)
    valor_w1 = ft.Text("w1 = 0.00", size=22, color="#9BE7FF", left=170, top=185)

    valor_x2 = ft.Text("x2 = 0", size=24, color="white", left=50, top=335)
    valor_w2 = ft.Text("w2 = 0.00", size=22, color="#9BE7FF", left=170, top=335)

    valor_bias = ft.Text("bias = 0.00", size=24, color="#FFD166", left=325, top=285)
    valor_y = ft.Text(
        "y = 0",
        size=30,
        weight=ft.FontWeight.BOLD,
        color="white",
        left=770,
        top=250,
    )

    valor_prediccion = ft.Text("Predicción: -", size=24, color="white")

    formula_txt = ft.Text(
        "z = x1*w1 + x2*w2 + bias",
        size=16,
        color="#98A8BC",
    )

    # -------------------------------------------------
    # NODOS
    # -------------------------------------------------
    input1_node = ft.Container(
        width=32,
        height=32,
        border_radius=16,
        bgcolor="#1A8F3C",
        shadow=glow_style("#1A8F3C", 12),
        left=120,
        top=195,
    )

    input2_node = ft.Container(
        width=32,
        height=32,
        border_radius=16,
        bgcolor="#1A8F3C",
        shadow=glow_style("#1A8F3C", 12),
        left=120,
        top=345,
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
        width=38,
        height=38,
        border_radius=19,
        bgcolor="#39FF6F",
        shadow=glow_style("#39FF6F", 18),
        left=820,
        top=250,
    )

    # -------------------------------------------------
    # CONEXIONES
    # -------------------------------------------------
    linea_1 = ft.Container(
        width=240,
        height=6,
        bgcolor="#39FF6F",
        border_radius=5,
        left=145,
        top=208,
        shadow=glow_style("#39FF6F", 10),
    )

    linea_2 = ft.Container(
        width=240,
        height=6,
        bgcolor="#39FF6F",
        border_radius=5,
        left=145,
        top=358,
        shadow=glow_style("#39FF6F", 10),
    )

    linea_salida = ft.Container(
        width=330,
        height=8,
        bgcolor="#39FF6F",
        border_radius=5,
        left=470,
        top=255,
        shadow=glow_style("#39FF6F", 14),
    )

    # Ramificaciones visuales simples
    rama_1 = ft.Container(
        width=60,
        height=4,
        bgcolor="#39FF6F",
        border_radius=5,
        left=300,
        top=220,
        shadow=glow_style("#39FF6F", 8),
    )

    rama_2 = ft.Container(
        width=55,
        height=4,
        bgcolor="#39FF6F",
        border_radius=5,
        left=305,
        top=250,
        shadow=glow_style("#39FF6F", 8),
    )

    rama_3 = ft.Container(
        width=55,
        height=4,
        bgcolor="#39FF6F",
        border_radius=5,
        left=305,
        top=290,
        shadow=glow_style("#39FF6F", 8),
    )

    # -------------------------------------------------
    # PULSOS ANIMADOS
    # -------------------------------------------------
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

    # -------------------------------------------------
    # PANEL VISUAL
    # -------------------------------------------------
    panel_neurona = ft.Container(
        width=920,
        height=520,
        bgcolor="#07111F",
        border_radius=20,
        padding=10,
        content=ft.Stack(
            controls=[
                epoca_txt,
                linea_1,
                linea_2,
                linea_salida,
                rama_1,
                rama_2,
                rama_3,
                input1_node,
                input2_node,
                soma,
                nucleo,
                output_node,
                pulso_1,
                pulso_2,
                pulso_out,
                valor_x1,
                valor_w1,
                valor_x2,
                valor_w2,
                valor_bias,
                valor_y,
                z_txt,
                error_txt,
            ],
            width=900,
            height=500,
        ),
    )

    # -------------------------------------------------
    # CONTROLES
    # -------------------------------------------------
    boton_entrenar = ft.ElevatedButton("Entrenar")
    boton_reiniciar = ft.ElevatedButton("Reiniciar vista")

    input_1 = ft.TextField(label="Input 1", width=120, value="1")
    input_2 = ft.TextField(label="Input 2", width=120, value="1")
    boton_predecir = ft.ElevatedButton("Predecir")

    controles = ft.Row(
        controls=[boton_entrenar, boton_reiniciar, input_1, input_2, boton_predecir],
        alignment=ft.MainAxisAlignment.CENTER,
        wrap=True,
    )

    # -------------------------------------------------
    # FUNCIONES DE APOYO
    # -------------------------------------------------
    def reiniciar_vista():
        valor_x1.value = "x1 = 0"
        valor_x2.value = "x2 = 0"

        if pesos_entrenados is None:
            valor_w1.value = "w1 = 0.00"
            valor_w2.value = "w2 = 0.00"
        else:
            valor_w1.value = f"w1 = {pesos_entrenados[0]:.2f}"
            valor_w2.value = f"w2 = {pesos_entrenados[1]:.2f}"

        if bias_entrenado is None:
            valor_bias.value = "bias = 0.00"
        else:
            valor_bias.value = f"bias = {bias_entrenado:.2f}"

        valor_y.value = "y = 0"
        valor_y.color = "white"
        z_txt.value = "z = 0.00"
        error_txt.value = "error = 0"
        estado_txt.value = "Estado: En espera"

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

    async def animar_ejemplo(x1, x2, y_pred):
        if x1 == 1:
            await resaltar_nodo(page, input1_node, "#B7FF00", "#1A8F3C", 0.12)

        if x2 == 1:
            await resaltar_nodo(page, input2_node, "#B7FF00", "#1A8F3C", 0.12)

        if x1 == 1:
            await animar_pulso(page, pulso_1, 136, 201, 355, 220, pasos=22, delay=0.018)

        if x2 == 1:
            await animar_pulso(page, pulso_2, 136, 351, 355, 290, pasos=22, delay=0.018)

        soma.bgcolor = "#7CFF6B"
        soma.shadow = glow_style("#7CFF6B", 45)
        nucleo.bgcolor = "#FFF59D"
        nucleo.shadow = glow_style("#FFF59D", 30)
        page.update()
        await asyncio.sleep(0.12)

        soma.bgcolor = "#2FDB63"
        soma.shadow = glow_style("#39FF6F", 30)
        nucleo.bgcolor = "#FFF176"
        nucleo.shadow = glow_style("#FFF176", 22)
        page.update()

        if y_pred == 1:
            valor_y.color = "#00E5FF"
            output_node.bgcolor = "#00E5FF"
            output_node.shadow = glow_style("#00E5FF", 30)
            page.update()

            await animar_pulso(page, pulso_out, 490, 250, 820, 260, pasos=28, delay=0.016)

            await asyncio.sleep(0.1)

            output_node.bgcolor = "#39FF6F"
            output_node.shadow = glow_style("#39FF6F", 18)
            page.update()
        else:
            valor_y.color = "white"
            page.update()

    # -------------------------------------------------
    # ENTRENAR
    # -------------------------------------------------
    async def entrenar_click(e):
        nonlocal pesos_entrenados, bias_entrenado, entrenando

        if entrenando:
            return

        entrenando = True
        boton_entrenar.disabled = True
        boton_predecir.disabled = True
        boton_reiniciar.disabled = True

        estado_txt.value = "Estado: Entrenando..."
        page.update()

        n_caracteristicas = X.shape[1]
        pesos = np.zeros(n_caracteristicas)
        bias = 0.0

        for ep in range(100):
            epoca_txt.value = f"Época: {ep + 1}"
            page.update()

            pesos_actualizados = False

            for i in range(X.shape[0]):
                x1 = int(X[i][0])
                x2 = int(X[i][1])

                valor_x1.value = f"x1 = {x1}"
                valor_x2.value = f"x2 = {x2}"
                valor_w1.value = f"w1 = {pesos[0]:.2f}"
                valor_w2.value = f"w2 = {pesos[1]:.2f}"
                valor_bias.value = f"bias = {bias:.2f}"
                page.update()

                z = np.dot(pesos, X[i]) + bias
                y_pred = funcion_activacion(z)
                error = int(y[i] - y_pred)

                z_txt.value = f"z = {z:.2f}"
                error_txt.value = f"error = {error}"
                valor_y.value = f"y = {y_pred}"
                page.update()

                await animar_ejemplo(x1, x2, y_pred)

                if error != 0:
                    pesos += 0.1 * error * X[i]
                    bias += 0.1 * error
                    pesos_actualizados = True

                    valor_w1.value = f"w1 = {pesos[0]:.2f}"
                    valor_w2.value = f"w2 = {pesos[1]:.2f}"
                    valor_bias.value = f"bias = {bias:.2f}"

                    estado_txt.value = "Estado: Ajustando pesos..."
                    soma.bgcolor = "#FFD54F"
                    soma.shadow = glow_style("#FFD54F", 45)
                    page.update()
                    await asyncio.sleep(0.18)

                    soma.bgcolor = "#2FDB63"
                    soma.shadow = glow_style("#39FF6F", 30)
                    page.update()
                else:
                    estado_txt.value = "Estado: Sin ajuste en este patrón"
                    page.update()

                await asyncio.sleep(0.25)

            if not pesos_actualizados:
                estado_txt.value = "Estado: Convergencia alcanzada"
                epoca_txt.value = f"Época: {ep + 1} (convergió)"
                page.update()
                break

        pesos_entrenados = pesos.copy()
        bias_entrenado = float(bias)

        estado_txt.value = (
            f"Estado: Entrenamiento finalizado | "
            f"pesos={pesos_entrenados}, bias={bias_entrenado:.2f}"
        )

        boton_entrenar.disabled = False
        boton_predecir.disabled = False
        boton_reiniciar.disabled = False
        entrenando = False
        page.update()

    # -------------------------------------------------
    # PREDECIR
    # -------------------------------------------------
    async def predecir_click(e):
        nonlocal pesos_entrenados, bias_entrenado

        if pesos_entrenados is None or bias_entrenado is None:
            valor_prediccion.value = "Predicción: primero debes entrenar"
            page.update()
            return

        try:
            x1 = int(input_1.value)
            x2 = int(input_2.value)
        except:
            valor_prediccion.value = "Predicción: ingresa valores enteros"
            page.update()
            return

        if x1 not in [0, 1] or x2 not in [0, 1]:
            valor_prediccion.value = "Predicción: usa solo 0 o 1"
            page.update()
            return

        valor_x1.value = f"x1 = {x1}"
        valor_x2.value = f"x2 = {x2}"
        valor_w1.value = f"w1 = {pesos_entrenados[0]:.2f}"
        valor_w2.value = f"w2 = {pesos_entrenados[1]:.2f}"
        valor_bias.value = f"bias = {bias_entrenado:.2f}"

        z = np.dot(pesos_entrenados, np.array([x1, x2])) + bias_entrenado
        y_pred = funcion_activacion(z)

        z_txt.value = f"z = {z:.2f}"
        error_txt.value = "error = -"
        valor_y.value = f"y = {y_pred}"
        estado_txt.value = "Estado: Ejecutando predicción"
        page.update()

        await animar_ejemplo(x1, x2, y_pred)

        valor_prediccion.value = f"Predicción: {y_pred}"
        estado_txt.value = "Estado: Predicción lista"
        page.update()

    # -------------------------------------------------
    # REINICIAR
    # -------------------------------------------------
    def reiniciar_click(e):
        reiniciar_vista()
        valor_prediccion.value = "Predicción: -"
        page.update()

    # Eventos
    boton_entrenar.on_click = entrenar_click
    boton_predecir.on_click = predecir_click
    boton_reiniciar.on_click = reiniciar_click

    # Layout principal
    page.add(
        ft.Column(
            controls=[
                titulo,
                subtitulo,
                formula_txt,
                controles,
                estado_txt,
                panel_neurona,
                valor_prediccion,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
        )
    )

    reiniciar_vista()


ft.run(main)