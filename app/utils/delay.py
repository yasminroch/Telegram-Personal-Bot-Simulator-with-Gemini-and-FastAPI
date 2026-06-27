import random

def calcular_delay(fragmento: str) -> float:
    palavras = len(fragmento.split())
    base = 0.8 + (palavras * 0.12)
    return min(base + random.uniform(-0.2, 0.4), 3.5)
