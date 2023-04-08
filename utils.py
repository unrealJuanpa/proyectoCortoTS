import numpy as np
import sounddevice as sd
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas


def play_frequency(frequency:float, duration:float, decibels:float):
    # Generar la señal de audio
    intensity = 10**(decibels/20)
    t = np.linspace(0, duration, int(duration * 44100), endpoint=False)
    audio_signal = np.sin(2 * np.pi * frequency * t)*intensity
    # Reproducir la señal de audio
    sd.play(audio_signal, 44100)
    sd.wait()

def insert(freq:float, duracion:float, intensidad:float, escuchado:int):
    # 2023-04-07 18:40:28
    conn = sqlite3.connect('BD.db')
    ds = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(f"INSERT INTO mediciones (frecuencia, duracion, intensidad, escuchado, createdAt, updatedAt) VALUES ({freq}, {duracion}, {intensidad}, {escuchado}, '{ds}', '{ds}');")
    conn.commit()
    conn.close()

def select():
    conn = sqlite3.connect('BD.db')
    cursor = conn.execute("SELECT * from mediciones")
    ret = []
    for fila in cursor:
       ret.append(fila)
    conn.close()
    return ret

def generar_pdf_audiometria(resultados_audiometria):
    # Crear la figura de Matplotlib
    fig, ax = plt.subplots()
    ax.set_xlabel('Frecuencia (Hz)')
    ax.set_ylabel('Nivel de audición (dB HL)')
    ax.set_title('Audiometría')
    ax.plot([r[0] for r in resultados_audiometria], [r[1] for r in resultados_audiometria], 'o-')
    
    # Obtener la fecha y hora actual
    fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Ajustar los límites del eje y de la figura para desplazar la gráfica hacia abajo
    ax.set_ylim(bottom=min(ax.get_ylim()[0], -10))
    fig.subplots_adjust(top=0.8, bottom=0.2)
    
    # Generar el PDF con la imagen de Matplotlib y la fecha y hora actual centradas
    nombre_archivo = f'Audiometria_{fecha_hora_actual}.pdf'
    c = canvas.Canvas(nombre_archivo)
    c.setFontSize(20)
    c.drawCentredString(300, 750, f'Audiometría realizada el {fecha_hora_actual}')
    plt.savefig('audiometria.png')
    c.drawInlineImage('audiometria.png', 100, 300, width=400, height=400)
    c.save()
