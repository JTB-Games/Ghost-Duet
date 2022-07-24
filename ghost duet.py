from cgitb import text
import aubio
import numpy as num
import pyaudio
from pysinewave import SineWave
import pygame
pygame.init()
red = (255,0,0)
(width, height) = (512, 512)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ghost Duet')
pygame.display.flip()
BUFFER_SIZE = 2048
CHANNELS = 1
FORMAT = pyaudio.paFloat32
METHOD = "default"
SAMPLE_RATE = 44100
HOP_SIZE = BUFFER_SIZE//2
PERIOD_SIZE_IN_FRAME = HOP_SIZE
sinewave = SineWave(pitch=12, pitch_per_second=12, decibels_per_second=12)
sinewave.play()
running = True
pA = pyaudio.PyAudio()
mic = pA.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=PERIOD_SIZE_IN_FRAME)
pDetection = aubio.pitch(METHOD, BUFFER_SIZE, HOP_SIZE, SAMPLE_RATE)
pDetection.set_unit("Hz")
pDetection.set_silence(-40)
strnote = ""
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    font = pygame.font.SysFont(None, 64)
    data = mic.read(PERIOD_SIZE_IN_FRAME)
    samples = num.fromstring(data,
        dtype=aubio.float_type)
    pitch = pDetection(samples)[0]
    volume = num.sum(samples**2)/len(samples)
    volume = "{:6f}".format(volume)
    screen.fill((0,0,0))
    note = 0
    if pitch > 0:
        note = int(round(12*num.log2(pitch/440.0)))
    if note == 0:
        strnote = "A"
    elif note == 1:
        strnote = "A#"
    elif note == 2:
        strnote = "B"
    elif note == 3:
        strnote = "C"
    elif note == 4:
        strnote = "C#"
    elif note == 5:
        strnote = "D"
    elif note == 6:
        strnote = "D#"
    elif note == 7:
        strnote = "E"
    elif note == 8:
        strnote = "F"
    elif note == 9:
        strnote = "F#"
    elif note == 10:
        strnote = "G"
    elif note == 11:
        strnote = "G#"
    elif note == -1:
        strnote = "G#"
    elif note == -2:
        strnote = "G"
    elif note == -3:
        strnote = "F#"
    elif note == -4:
        strnote = "F"
    elif note == -5:
        strnote = "E"
    elif note == -6:
        strnote = "D#"
    elif note == -7:
        strnote = "D"
    elif note == -8:
        strnote = "C#"
    elif note == -9:
        strnote = "C"
    elif note == -10:
        strnote = "B"
    elif note == -11:
        strnote = "A#"
    elif note == -12:
        strnote = "A"
    img = font.render(str(strnote), True, red)
    screen.blit(img, (64, 64))
    pygame.display.update()
    if float(volume) > 0.00075:
        sinewave.set_frequency(pitch)
