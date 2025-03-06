import rule_engine

reglas_riesgo = {
    "bajo": rule_engine.Rule(
        "puntuacion_total >= 1 and puntuacion_total <= 34 or puntuacion_total <0"
    ),
    "moderado": rule_engine.Rule(
        "puntuacion_total >= 35 and puntuacion_total <= 54"
    ),
    "alto": rule_engine.Rule(
        "puntuacion_total >= 55 and puntuacion_total <= 74 or puntuacion_total > 75"
    ),
}


def calcular_puntuacion(cliente):
    puntuacion = 0


    if cliente["edad"] < 25:
        puntuacion += 10
    elif 26 <= cliente["edad"] <= 35:
        puntuacion += 15
    elif 36 <= cliente["edad"] <= 45:
        puntuacion += 25
    elif 46 <= cliente["edad"] <= 55:
        puntuacion += 35
    elif 55 <= cliente["edad"] <= 75:
        puntuacion += 50
    elif 75 <= cliente["edad"] <= 110:
        puntuacion += 180


    if cliente["salud"] == "saludable":
        puntuacion -= 20
    elif cliente["salud"] == "hipertension":
        puntuacion += 10
    elif cliente["salud"] == "diabetes":
        puntuacion += 25
    elif cliente["salud"] == "obesidad":
        puntuacion += 15


    if cliente["historial_familiar"] == "false":
        puntuacion -= 10
    else:
        puntuacion += 10


    if cliente["estilo_vida"] == "sedentario":
        puntuacion += 5
    elif cliente["estilo_vida"] == "activo":
        puntuacion -= 5
    elif cliente["estilo_vida"] == "deportista":
        puntuacion -= 15
    elif cliente["estilo_vida"] == "fumador":
        puntuacion += 15
    elif cliente["estilo_vida"] == "alcoholico":
        puntuacion += 15


    if cliente["ocupacion"] == "oficina":
        puntuacion -= 5
    elif cliente["ocupacion"] == "bombero":
        puntuacion += 10
    elif cliente["ocupacion"] == "minero":
        puntuacion += 15
    elif cliente["ocupacion"] == "piloto":
        puntuacion += 10


    if cliente["historial_seguro"] == "bueno":
        puntuacion -= 10
    elif cliente["historial_seguro"] == "reclamos_frecuentes":
        puntuacion += 5
    elif cliente["historial_seguro"] == "malo":
        puntuacion += 15

    return puntuacion


clientes = [
    {
        "nombre": "Juan Pérez",
        "edad": 31,
        "salud": "hipertension",
        "historial_familiar": "false",
        "estilo_vida": "activo",
        "ocupacion": "oficina",
        "historial_seguro": "malo"
    }
]

for cliente in clientes:
    puntuacion_total = calcular_puntuacion(cliente)
    cliente["puntuacion_total"] = puntuacion_total

    nivel_riesgo = "Desconocido"
    for nivel, regla in reglas_riesgo.items():
        if regla.matches(cliente):
            nivel_riesgo = nivel.capitalize()
            break

    print(f"Cliente: {cliente['nombre']}, Puntuación Total: {puntuacion_total}, Nivel de Riesgo: {nivel_riesgo}")