from flask import Flask, render_template, request, jsonify
import rule_engine

app = Flask(__name__)

# Definir reglas para evaluar la viabilidad del préstamo
reglas_credito = {
    "bajo_riesgo": rule_engine.Rule("puntuacion_crediticia > 750"),
    "riesgo_moderado": rule_engine.Rule("puntuacion_crediticia >= 600 and puntuacion_crediticia <= 750"),
    "alto_riesgo": rule_engine.Rule("puntuacion_crediticia < 600"),
}

reglas_ingresos = {
    "bajo_riesgo": rule_engine.Rule("ingresos_mensuales >= 3 * cuota_prestamo"),
    "riesgo_moderado": rule_engine.Rule(
        "ingresos_mensuales >= 1.5 * cuota_prestamo and ingresos_mensuales < 3 * cuota_prestamo"),
    "alto_riesgo": rule_engine.Rule("ingresos_mensuales < 1.5 * cuota_prestamo"),
}

reglas_dti = {
    "bajo_riesgo": rule_engine.Rule("dti < 30"),
    "riesgo_moderado": rule_engine.Rule("dti >= 30 and dti <= 50"),
    "alto_riesgo": rule_engine.Rule("dti > 50"),
}

reglas_empleo = {
    "bajo_riesgo": rule_engine.Rule("empleo == 'fijo' and anios_experiencia > 5"),
    "riesgo_moderado": rule_engine.Rule("empleo == 'fijo' and anios_experiencia <= 5"),
    "alto_riesgo": rule_engine.Rule("empleo == 'temporal' or empleo == 'autonomo'"),
}

reglas_garantias = {
    "bajo_riesgo": rule_engine.Rule("garantias == 'alta'"),
    "riesgo_moderado": rule_engine.Rule("garantias == 'media'"),
    "alto_riesgo": rule_engine.Rule("garantias == 'baja'"),
}

reglas_prestamos_previos = {
    "bajo_riesgo": rule_engine.Rule("historial_prestamos == 'bueno'"),
    "riesgo_moderado": rule_engine.Rule("historial_prestamos == 'moderado'"),
    "alto_riesgo": rule_engine.Rule("historial_prestamos == 'malo'"),
}

# Definir reglas para la decisión final del préstamo
reglas_decision = {
    "Aprobado": rule_engine.Rule("puntuacion_total >= 0 and puntuacion_total <= 20"),
    "Aprobacion Condicional": rule_engine.Rule("puntuacion_total > 20 and puntuacion_total <= 40"),
    "Rechazado": rule_engine.Rule("puntuacion_total > 40"),
}


def calcular_puntuacion(cliente):
    puntuacion = 0

    # Evaluar cada criterio
    for nivel, regla in reglas_credito.items():
        if regla.matches(cliente):
            puntuacion += {"bajo_riesgo": 0, "riesgo_moderado": 10, "alto_riesgo": 20}[nivel]

    for nivel, regla in reglas_ingresos.items():
        if regla.matches(cliente):
            puntuacion += {"bajo_riesgo": 0, "riesgo_moderado": 10, "alto_riesgo": 20}[nivel]

    for nivel, regla in reglas_dti.items():
        if regla.matches(cliente):
            puntuacion += {"bajo_riesgo": 0, "riesgo_moderado": 10, "alto_riesgo": 20}[nivel]

    for nivel, regla in reglas_empleo.items():
        if regla.matches(cliente):
            puntuacion += {"bajo_riesgo": 0, "riesgo_moderado": 10, "alto_riesgo": 20}[nivel]

    for nivel, regla in reglas_garantias.items():
        if regla.matches(cliente):
            puntuacion += {"bajo_riesgo": 0, "riesgo_moderado": 5, "alto_riesgo": 10}[nivel]

    for nivel, regla in reglas_prestamos_previos.items():
        if regla.matches(cliente):
            puntuacion += {"bajo_riesgo": 0, "riesgo_moderado": 10, "alto_riesgo": 20}[nivel]

    return puntuacion


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/evaluar_prestamo", methods=["POST"])
def evaluar_prestamo():
    try:
        datos = request.json

        # Verificar si todos los campos están presentes y no vacíos
        campos_requeridos = ["nombre", "puntuacion_crediticia", "ingresos_mensuales", "cuota_prestamo", "dti", "empleo",
                             "anios_experiencia", "garantias", "historial_prestamos"]
        if any(campo not in datos or datos[campo] == "" for campo in campos_requeridos):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        # Convertir tipos de datos
        datos["puntuacion_crediticia"] = int(datos["puntuacion_crediticia"])
        datos["ingresos_mensuales"] = float(datos["ingresos_mensuales"])
        datos["cuota_prestamo"] = float(datos["cuota_prestamo"])
        datos["dti"] = float(datos["dti"])
        datos["anios_experiencia"] = int(datos["anios_experiencia"])

        # Calcular puntuación
        puntuacion_total = calcular_puntuacion(datos)
        datos["puntuacion_total"] = puntuacion_total

        # Determinar decisión final
        decision_final = "Desconocido"
        for decision, regla in reglas_decision.items():
            if regla.matches(datos):
                decision_final = decision
                break

        return jsonify({
            "nombre": datos["nombre"],
            "puntuacion_total": puntuacion_total,
            "decision": decision_final
        })

    except ValueError:
        return jsonify({"error": "Datos numéricos inválidos"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
