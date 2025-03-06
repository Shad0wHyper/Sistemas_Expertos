import rule_engine

# Crear base de datos de clientes
clientes = [
    {
        "nombre": "Mayabi",
        "edad": 22,
        "salud": "saludable",
        "historial_familiar": "false",
        "estilo_vida": "activo",
        "ocupacion": "oficina",
        "historial_seguro": "bueno"
    },
    {
        "nombre": "Carlos",
        "edad": 45,
        "salud": "diabetes",
        "historial_familiar": "true",
        "estilo_vida": "fumador",
        "ocupacion": "minero",
        "historial_seguro": "reclamos_frecuentes"
    },
{
        "nombre": "Jaime",
        "edad": 48,
        "salud": "saludable",
        "historial_familiar": "false",
        "estilo_vida": "deportista",
        "ocupacion": "oficina",
        "historial_seguro": "bueno"
    },
    {
        "nombre": "Ana",
        "edad": 51,
        "salud": "hipertension",
        "historial_familiar": "true",
        "estilo_vida": "alcoholico",
        "ocupacion": "piloto",
        "historial_seguro": "bueno"
    }
]

# Reglas de riesgo
reglas_riesgo = {
    "bajo": rule_engine.Rule(
        "(edad < 30) and "
        "(salud == 'saludable') and "
        "(historial_familiar == 'false') and "
        "(estilo_vida == 'activo') and "
        "(ocupacion == 'oficina') and "
        "(historial_seguro == 'bueno')"
    ),
    "alto": rule_engine.Rule(
        "(edad > 50) and ((salud in ['diabetes', 'hipertension', 'obesidad']) or "
        "(historial_familiar == 'true') or "
        "(estilo_vida in ['fumador', 'alcoholico']) or "
        "(ocupacion in ['piloto', 'bombero']))"
    ),
    "moderado": rule_engine.Rule(
        "(edad >= 30 and edad <= 50) or "
        "(salud in ['diabetes', 'hipertension', 'obesidad']) or "
        "(historial_familiar == 'true') or "
        "(estilo_vida in ['fumador', 'alcoholico'])"
    )
}

# Evaluar riesgo para cada cliente
for cliente in clientes:
    if reglas_riesgo["bajo"].matches(cliente):
        nivel_riesgo = "Bajo Riesgo"
    elif reglas_riesgo["alto"].matches(cliente):
        nivel_riesgo = "Alto Riesgo"
    elif reglas_riesgo["moderado"].matches(cliente):
        nivel_riesgo = "Moderado Riesgo"
    else:
        nivel_riesgo = "Desconocido"

    print(f"Cliente: {cliente['nombre']}, Nivel de Riesgo: {nivel_riesgo}")