import sounddevice as sd
import flet.canvas as cv
import numpy as np
import flet as ft
import asyncio
import math

from config.user.microphone.MicrophoneSettings import get_saved_microphones
from content.application.infra.tuner.afinacoes.Afinacoes import get_current_tuning_notes_frequency

GAUGE_SIZE = 300
START_ANGLE = math.pi
SWEEP_TOTAL = math.pi

RATE = 44100
CHUNK = 4096
alvo = 0.0

stream = None
running = False
current_frequency = 0.0

MIN_VALUE = -50.0
MAX_VALUE = 50.0

def audio_callback(indata, frames, time, status):
    global current_frequency

    audio = indata[:, 0].astype(np.float32)

    audio -= np.mean(audio)

    rms = np.sqrt(np.mean(audio ** 2))

    if rms < 0.01:
        current_frequency = 0.0
        return

    min_freq = 50
    max_freq = 1000

    min_lag = int(RATE / max_freq)
    max_lag = int(RATE / min_freq)

    correlation = np.correlate(audio, audio, mode="full")
    correlation = correlation[len(correlation) // 2:]

    correlation[:min_lag] = 0

    if max_lag < len(correlation):
        correlation[max_lag:] = 0

    lag = np.argmax(correlation)

    if lag == 0:
        current_frequency = 0.0
        return

    if 1 <= lag < len(correlation) - 1:

        y1 = correlation[lag - 1]
        y2 = correlation[lag]
        y3 = correlation[lag + 1]

        denominator = y1 - 2 * y2 + y3

        if denominator != 0:
            shift = 0.5 * (y1 - y3) / denominator
            lag = lag + shift

    current_frequency = RATE / lag

async def update_frequency(frequency_text, note, value_expected, set_gauge_value, page, gauge):
    while running:

        if current_frequency > 0:

            # Encontra a nota mais próxima
            nota_proxima, frequencia_proxima = min(
                get_current_tuning_notes_frequency(),
                key=lambda x: abs(x[1] - current_frequency)
            )

            diferenca = current_frequency - frequencia_proxima

            global MIN_VALUE, MAX_VALUE, alvo

            alvo = float(f"{frequencia_proxima:.2f}")

            MIN_VALUE = float(f"{current_frequency:+.2f}") - (float(f"{current_frequency:+.2f}") / 2)
            MAX_VALUE = float(f"{current_frequency:+.2f}")  + (float(f"{current_frequency:+.2f}") / 2)

            # DEBUG

            # print(
            #     f"Detectado: {current_frequency:.2f} Hz | "
            #     f"Nota: {nota_proxima} | "
            #     f"Alvo: {frequencia_proxima:.2f} Hz | "
            #     f"Diferença: {diferenca:+.2f} Hz"
            # )

            set_gauge_value(current_frequency)

            note.value = nota_proxima

            frequency_text.value = f"{current_frequency:.2f} Hz"
            value_expected.value = f"{frequencia_proxima:.2f} Hz"

        page.update()

        await asyncio.sleep(0.05)

def toggle_audio(e, frequency_text, note, value_expected, button, page, set_gauge_value, gauge):
    global stream, running

    sd_default_mic_index = None

    saved_mic = get_saved_microphones()["default_microphone"]

    devices = sd.query_devices()

    for i, device in enumerate(devices):

        if device["max_input_channels"] <= 0:
            continue

        if saved_mic == device["name"]:
            sd_default_mic_index = i
            break

        if sd_default_mic_index is not None:
            break

    if not running:
        # Liga
        stream = sd.InputStream(
            device=sd_default_mic_index,
            samplerate=RATE,
            blocksize=CHUNK,
            channels=1,
            callback=audio_callback
        )

        stream.start()
        running = True

        button.content = "Para Afinador"

        page.run_task(update_frequency, frequency_text, note, value_expected, set_gauge_value, page, gauge)

    else:
        # Desliga
        stream.stop()
        stream.close()
        stream = None

        running = False

        button.content = "Ligar Afinador"
        frequency_text.value = "0.00 Hz"

    page.update()

def get_gauge(value_label, value_caption, value_expected):

    global current_frequency

    def value_to_color(v: float) -> str:
        if v < (alvo + 1.5) and v > (alvo - 1.5) :
            return ft.Colors.GREEN
        elif v < (alvo + 10) and v > (alvo - 10):
            return ft.Colors.ORANGE
        else:
            return ft.Colors.RED

    def set_value(v: float):

        min_value = alvo - ( alvo / 2)
        max_value = alvo + ( alvo / 2)

        fraction_raw = (v - min_value) / (max_value - min_value)
        fraction = max(0.0, min(1.0, fraction_raw))

        # DEBUG

        # print(f"detectado: {current_frequency}")
        # print(f"min: {min_value}")
        # print(f"max: {max_value}")
        # print(f"fraction: {fraction}")

        progress_arc.sweep_angle = SWEEP_TOTAL * fraction
        progress_arc.paint.color = value_to_color(current_frequency)

        # Atualiza agulha
        needle.rotate.angle = -math.pi / 2 + (math.pi * fraction)

        # Texto
        value_label.value = f"{current_frequency:.2f}"
        value_label.color = value_to_color(current_frequency)

        gauge_canvas.update()
        needle.update()
        value_label.update()

    arc_bg = cv.Arc(
        x=10,
        y=10,
        width=GAUGE_SIZE - 20,
        height=GAUGE_SIZE - 20,
        start_angle=START_ANGLE,
        sweep_angle=SWEEP_TOTAL,
        paint=ft.Paint(
            stroke_width=10,
            style=ft.PaintingStyle.STROKE,
            stroke_cap=ft.StrokeCap.ROUND,
            color=ft.Colors.with_opacity(0.15, ft.Colors.ON_SURFACE)
        )
    )

    progress_arc = cv.Arc(
        x=10,
        y=10,
        width=GAUGE_SIZE - 20,
        height=GAUGE_SIZE - 20,
        start_angle=START_ANGLE,
        sweep_angle=0,
        paint=ft.Paint(
            stroke_width=18,
            style=ft.PaintingStyle.STROKE,
            stroke_cap=ft.StrokeCap.ROUND,
            color=ft.Colors.GREEN,
        ),
    )

    # Canva pra incluir na page
    gauge_canvas = cv.Canvas(
        width=GAUGE_SIZE + 20,
        height=GAUGE_SIZE + 20,
        shapes=[arc_bg, progress_arc],
    )

    needle = ft.Container(
        width=4,
        height=GAUGE_SIZE / 2 - 25,
        bgcolor=ft.Colors.RED,
        border_radius=2,
        alignment=ft.Alignment.TOP_CENTER,
        rotate=ft.Rotate(angle=-math.pi / 2, alignment=ft.Alignment.BOTTOM_CENTER),
        animate_rotation=ft.Animation(100, ft.AnimationCurve.EASE_OUT)
    )

    needle_hub = ft.Container(
        width=16,
        height=16,
        bgcolor=ft.Colors.RED,
        border_radius=8,
    )

    gauge = ft.Stack(
        width=GAUGE_SIZE,
        height=GAUGE_SIZE,
        controls=[
            gauge_canvas,
            ft.Container(
                alignment=ft.Alignment.BOTTOM_CENTER,
                padding=ft.Padding(bottom=25),
                content=ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=0,
                    controls=[value_caption, value_expected, value_label]
                ),
            ),
            ft.Container(
                width=GAUGE_SIZE,
                height=GAUGE_SIZE,
                alignment=ft.Alignment.CENTER,
                padding=ft.Padding(bottom=GAUGE_SIZE / 2 - 8),
                content=needle,
            ),
            ft.Container(
                width=GAUGE_SIZE,
                height=GAUGE_SIZE,
                alignment=ft.Alignment.CENTER,
                content=needle_hub,
            )
        ]
    )

    return gauge, set_value
