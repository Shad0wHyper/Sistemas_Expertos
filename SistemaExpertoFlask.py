from flask import Flask, render_template, request, jsonify
import rule_engine

app = Flask(__name__)

# Reglas para calcular la puntuación
reglas_edad = {
    "menor_25": rule_engine.Rule("edad < 25"),
    "26_a_35": rule_engine.Rule("edad >= 26 and edad <= 35"),
    "36_a_45": rule_engine.Rule("edad >= 36 and edad <= 45"),
    "46_a_55": rule_engine.Rule("edad >= 46 and edad <= 55"),
    "55_a_75": rule_engine.Rule("edad >= 55 and edad <= 75"),
    "75_a_140": rule_engine.Rule("edad >= 75 and edad <= 140"),
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
    "bajo": rule_engine.Rule("puntuacion_total >= 1 and puntuacion_total <= 34 or puntuacion_total <= 0"),
    "moderado": rule_engine.Rule("puntuacion_total >= 35 and puntuacion_total <= 54"),
    "alto": rule_engine.Rule("puntuacion_total >= 55 and puntuacion_total <= 74 or puntuacion_total > 75"),
}

def calcular_puntuacion(cliente):
    puntuacion = 0

    # Evaluar edad
    for nivel, regla in reglas_edad.items():
        if regla.matches(cliente):
            puntuacion += {
                "menor_25": 10, "26_a_35": 15, "36_a_45": 25,
                "46_a_55": 35, "55_a_75": 50, "75_a_140": 180
            }[nivel]

    # Evaluar salud
    for nivel, regla in reglas_salud.items():
        if regla.matches(cliente):
            puntuacion += {
                "saludable": 0, "hipertension": 15, "diabetes": 25, "obesidad": 35
            }[nivel]

    # Evaluar historial familiar
    for nivel, regla in reglas_historial_familiar.items():
        if regla.matches(cliente):
            puntuacion += {
                "sin_historial": 0, "con_historial": 20
            }[nivel]

    # Evaluar estilo de vida
    for nivel, regla in reglas_estilo_vida.items():
        if regla.matches(cliente):
            puntuacion += {
                "sedentario": 10, "activo": 5, "deportista": -10,
                "fumador": 20, "alcoholico": 25
            }[nivel]

    # Evaluar ocupación
    for nivel, regla in reglas_ocupacion.items():
        if regla.matches(cliente):
            puntuacion += {
                "oficina": 5, "bombero": 30, "minero": 40, "piloto": 35
            }[nivel]

    # Evaluar historial de seguro
    for nivel, regla in reglas_historial_seguro.items():
        if regla.matches(cliente):
            puntuacion += {
                "bueno": -10, "reclamos_frecuentes": 20, "malo": 30
            }[nivel]

    return puntuacion

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/calcular_riesgo", methods=["POST"])
def calcular_riesgo():
    try:
        datos = request.json

        # Verificar si todos los campos están presentes y no vacíos
        campos_requeridos = ["nombre", "edad", "salud", "historial_familiar", "estilo_vida", "ocupacion", "historial_seguro"]
        if any(campo not in datos or datos[campo] == "" for campo in campos_requeridos):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        # Convertir tipos de datos
        datos["edad"] = int(datos["edad"])
        datos["historial_familiar"] = datos["historial_familiar"].lower() == "true"

        # Calcular puntuación
        puntuacion_total = calcular_puntuacion(datos)
        datos["puntuacion_total"] = puntuacion_total

        # Determinar nivel de riesgo
        nivel_riesgo = "Desconocido"
        for nivel, regla in reglas_riesgo.items():
            if regla.matches(datos):
                nivel_riesgo = nivel.capitalize()
                break

        return jsonify({
            "nombre": datos["nombre"],
            "puntuacion_total": puntuacion_total,
            "nivel_riesgo": nivel_riesgo
        })

    except ValueError:
        return jsonify({"error": "Edad debe ser un número válido"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
