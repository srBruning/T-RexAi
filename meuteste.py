from ai.neuronio import RedeNeural
import random


def tt():
    red = RedeNeural()
    c = 100
    while  c >4:
        print(red.getSaida())
        red = RedeNeural()
        red.setEntrada([200, 40, 15, 31, 6, 15])
        red.calcularSaida()
        c = sum(red.getSaida())
