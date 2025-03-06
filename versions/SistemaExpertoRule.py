import rule_engine

# Definir las reglas para cada condición
reglas_edad = {
    "menor_25": rule_engine.Rule("edad < 25"),
    "26_a_35": rule_engine.Rule("edad >= 26 and edad <= 35"),
    "36_a_45": rule_engine.Rule("edad >= 36 and edad <= 45"),
    "46_a_55": rule_engine.Rule("edad >= 46 and edad <= 55"),
    "55_a_75": rule_engine.Rule("edad >= 55 and edad <= 75"),
    "75_a_110": rule_engine.Rule("edad >= 75 and edad <= 110"),
}

reglas_salud = {
    "saludable": rule_engine.Rule("salud == 'saludable'"),
    "hipertension": rule_engine.Rule("salud == 'hipertension'"),
    "diabetes": rule_engine.Rule("salud == 'diabetes'"),
    "obesidad": rule_engine.Rule("salud == 'obesidad'"),
}

reglas_historial_familiar = {
    "sin_historial": rule_engine.Rule("historial_familiar == 'false'"),
    "con_historial": rule_engine.Rule("historial_familiar == 'true'"),
}

reglas_estilo_vida = {
    "sedentario": rule_engine.Rule("estilo_vida == 'sedentario'"),
    "activo": rule_engine.Rule("estilo_vida == 'activo'"),
    "deportista": rule_engine.Rule("estilo_vida == 'deportista'"),
    "fumador": rule_engine.Rule("estilo_vida == 'fumador'"),
    "alcoholico": rule_engine.Rule("estilo_vida == 'alcoholico'"),
}

reglas_ocupacion = {
    "oficina": rule_engine.Rule("ocupacion == 'oficina'"),
    "bombero": rule_engine.Rule("ocupacion == 'bombero'"),
    "minero": rule_engine.Rule("ocupacion == 'minero'"),
    "piloto": rule_engine.Rule("ocupacion == 'piloto'"),
}

reglas_historial_seguro = {
    "bueno": rule_engine.Rule("historial_seguro == 'bueno'"),
    "reclamos_frecuentes": rule_engine.Rule("historial_seguro == 'reclamos_frecuentes'"),
    "malo": rule_engine.Rule("historial_seguro == 'malo'"),
}

# Definir las reglas para el nivel de riesgo
reglas_riesgo = {
    "bajo": rule_engine.Rule("puntuacion_total >= 1 and puntuacion_total <= 34 or puntuacion_total < 0"),
    "moderado": rule_engine.Rule("puntuacion_total >= 35 and puntuacion_total <= 54"),
    "alto": rule_engine.Rule("puntuacion_total >= 55 and puntuacion_total <= 74 or puntuacion_total > 75"),
}

# Función para calcular la puntuación total basada en las reglas
def calcular_puntuacion(cliente):
    puntuacion = 0

    # Aplicar reglas de edad
    for nivel, regla in reglas_edad.items():
        if regla.matches(cliente):
            if nivel == "menor_25":
                puntuacion += 10
            elif nivel == "26_a_35":
                puntuacion += 15
            elif nivel == "36_a_45":
                puntuacion += 25
            elif nivel == "46_a_55":
                puntuacion += 35
            elif nivel == "55_a_75":
                puntuacion += 50
            elif nivel == "75_a_110":
                puntuacion += 180

    # Aplicar reglas de salud
    reglas_salud = {
        "saludable": rule_engine.Rule("salud == 'saludable'"),
        "hipertension": rule_engine.Rule("salud == 'hipertension'"),
        "diabetes": rule_engine.Rule("salud == 'diabetes'"),
        "obesidad": rule_engine.Rule("salud == 'obesidad'"),
    }

    reglas_historial_familiar = {
        "sin_historial": rule_engine.Rule("historial_familiar == 'false'"),
        "con_historial": rule_engine.Rule("historial_familiar == 'true'"),
    }

    reglas_estilo_vida = {
        "sedentario": rule_engine.Rule("estilo_vida == 'sedentario'"),
        "activo": rule_engine.Rule("estilo_vida == 'activo'"),
        "deportista": rule_engine.Rule("estilo_vida == 'deportista'"),
        "fumador": rule_engine.Rule("estilo_vida == 'fumador'"),
        "alcoholico": rule_engine.Rule("estilo_vida == 'alcoholico'"),
    }

    reglas_ocupacion = {
        "oficina": rule_engine.Rule("ocupacion == 'oficina'"),
        "bombero": rule_engine.Rule("ocupacion == 'bombero'"),
        "minero": rule_engine.Rule("ocupacion == 'minero'"),
        "piloto": rule_engine.Rule("ocupacion == 'piloto'"),
    }

    reglas_historial_seguro = {
        "bueno": rule_engine.Rule("historial_seguro == 'bueno'"),
        "reclamos_frecuentes": rule_engine.Rule("historial_seguro == 'reclamos_frecuentes'"),
        "malo": rule_engine.Rule("historial_seguro == 'malo'"),
    }

    # Definir las reglas para el nivel de riesgo
    reglas_riesgo = {
        "bajo": rule_engine.Rule("puntuacion_total >= 1 and puntuacion_total <= 34 or puntuacion_total < 0"),
        "moderado": rule_engine.Rule("puntuacion_total >= 35 and puntuacion_total <= 54"),
        "alto": rule_engine.Rule("puntuacion_total >= 55 and puntuacion_total <= 74 or puntuacion_total > 75"),
    }

# Lista de clientes
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

# Calcular la puntuación y determinar el nivel de riesgo para cada cliente
for cliente in clientes:
    puntuacion_total = calcular_puntuacion(cliente)
    cliente["puntuacion_total"] = puntuacion_total

    nivel_riesgo = "Desconocido"
    for nivel, regla in reglas_riesgo.items():
        if regla.matches(cliente):
            nivel_riesgo = nivel.capitalize()
            break

    print(f"Cliente: {cliente['nombre']}, Puntuación Total: {puntuacion_total}, Nivel de Riesgo: {nivel_riesgo}")