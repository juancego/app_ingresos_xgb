import gradio as gr
import pandas as pd
import joblib

# Carga el modelo XGBoost entrenado
modelo = joblib.load("modelo_xgb.pkl")

def predecir_ingreso(
    sexo,
    edad,
    etnia,
    region,
    nivel_educativo,
    tipo_institucion,
    ocupacion,
    tipo_contrato,
    horas_trabajadas,
    tamano_hogar,
    zona
):
    # Crear DataFrame con la entrada del usuario
    entrada = pd.DataFrame([{
        "SEXO": sexo,
        "EDAD": edad,
        "ETNIA": etnia,
        "REGION": region,
        "NIVEL_EDUCATIVO": nivel_educativo,
        "TIPO_INSTITUCION": tipo_institucion,
        "OCUPACION": ocupacion,
        "TIPO_CONTRATO": tipo_contrato,
        "HORAS_TRABAJADAS": horas_trabajadas,
        "TAMANO_HOGAR": tamano_hogar,
        "ZONA": zona
    }])

    # IMPORTANTE:
    # Debes hacer aquí el mismo preprocesamiento que hiciste en el notebook
    # Si tu modelo requiere codificación o escalamiento, hazlo aquí antes de predecir
    # Ejemplo simple: codificar manualmente variables categóricas (esto depende de tu modelo)
    
    # Ejemplo rápido para variables categóricas que el modelo espera numéricas
    # Cambia según tus etiquetas y encoding original:
    map_sexo = {"Mujer":0, "Hombre":1}
    map_etnia = {"Ninguno":0, "Afrocolombiano":1, "Indígena":2, "Rom":3, "Otro":4}
    map_region = {"Caribe":0, "Andina":1, "Pacífica":2, "Orinoquía":3, "Amazonía":4, "Bogotá":5}
    map_nivel_educativo = {"Primaria":0, "Secundaria":1, "Técnico":2, "Universitario":3, "Posgrado":4}
    map_tipo_institucion = {"Pública":0, "Privada":1}
    map_ocupacion = {"Empleado":0, "Cuenta propia":1, "Obrero":2, "Servicio doméstico":3, "Otro":4}
    map_tipo_contrato = {"Término fijo":0, "Término indefinido":1, "Prestación de servicios":2, "Informal":3}
    map_zona = {"Urbana":0, "Rural":1}

    entrada['SEXO'] = entrada['SEXO'].map(map_sexo)
    entrada['ETNIA'] = entrada['ETNIA'].map(map_etnia)
    entrada['REGION'] = entrada['REGION'].map(map_region)
    entrada['NIVEL_EDUCATIVO'] = entrada['NIVEL_EDUCATIVO'].map(map_nivel_educativo)
    entrada['TIPO_INSTITUCION'] = entrada['TIPO_INSTITUCION'].map(map_tipo_institucion)
    entrada['OCUPACION'] = entrada['OCUPACION'].map(map_ocupacion)
    entrada['TIPO_CONTRATO'] = entrada['TIPO_CONTRATO'].map(map_tipo_contrato)
    entrada['ZONA'] = entrada['ZONA'].map(map_zona)

    # Ahora predice
    prediccion = modelo.predict(entrada)[0]
    return f"💰 Ingreso mensual estimado: ${prediccion:,.0f} COP"

# Definir interfaz Gradio
iface = gr.Interface(
    fn=predecir_ingreso,
    inputs=[
        gr.Radio(["Mujer", "Hombre"], label="Sexo"),
        gr.Slider(18, 65, step=1, label="Edad"),
        gr.Dropdown(["Ninguno", "Afrocolombiano", "Indígena", "Rom", "Otro"], label="Grupo Étnico"),
        gr.Dropdown(["Caribe", "Andina", "Pacífica", "Orinoquía", "Amazonía", "Bogotá"], label="Región"),
        gr.Dropdown(["Primaria", "Secundaria", "Técnico", "Universitario", "Posgrado"], label="Nivel educativo"),
        gr.Radio(["Pública", "Privada"], label="Tipo de institución"),
        gr.Dropdown(["Empleado", "Cuenta propia", "Obrero", "Servicio doméstico", "Otro"], label="Ocupación"),
        gr.Dropdown(["Término fijo", "Término indefinido", "Prestación de servicios", "Informal"], label="Tipo de contrato"),
        gr.Slider(0, 80, step=1, label="Horas trabajadas por semana"),
        gr.Slider(1, 10, step=1, label="Tamaño del hogar"),
        gr.Radio(["Urbana", "Rural"], label="Zona"),
    ],
    outputs=gr.Textbox(label="Predicción de ingreso mensual"),
    title="Predicción Ingreso Laboral Colombia - Modelo XGBoost",
    description="Predicción basada en modelo XGBoost entrenado con datos GEIH 2021-2024",
)

if __name__ == "__main__":
    iface.launch(share=True, inbrowser=True)

