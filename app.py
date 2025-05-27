import streamlit as st
import pandas as pd
import pickle

st.info("✅ App iniciada (inicio del script)")


@st.cache_resource
def cargar_modelo():
    with open("modelo_xgb.pkl", "rb") as f:
        modelo = pickle.load(f)
    return modelo

modelo = cargar_modelo()

st.info("✅ Modelo cargado correctamente")


st.title("Predicción de ingreso mensual")

# 1. Edad (slider)
EDAD = st.number_input("Edad", min_value=15, max_value=90, value=17, step=1)


# 2. Género (lista, one-hot)
generos = ["Mujer", "Hombre", "Hombre trans", "Mujer trans"]
genero_seleccionado = st.selectbox("Género", generos)

GENERO_HOMBRE = 1 if genero_seleccionado == "Hombre" else 0
GENERO_MUJER = 1 if genero_seleccionado == "Mujer" else 0
GENERO_HOMBRE_TRANS = 1 if genero_seleccionado == "Hombre trans" else 0
GENERO_MUJER_TRANS = 1 if genero_seleccionado == "Mujer trans" else 0

# 3. Estrato socioeconómico
estratos = {
    "2": 2, "1": 1, "3": 3, "4": 4, "5": 5, "6": 6,
    "No Aplica": 0,
    "No sabe": 9
}
estrato_seleccionado = st.selectbox("Estrato socioeconómico", list(estratos.keys()))
ESTRATO = estratos[estrato_seleccionado]

# 4. Departamento (mostrar nombre, enviar código)
dptos = {
    88: "SAN_ANDRES",
    5:  "ANTIOQUIA",
    8:  "ATLANTICO",
    11: "BOGOTA",
    13: "BOLIVAR",
    15: "BOYACA",
    17: "CALDAS",
    18: "CAQUETA",
    19: "CAUCA",
    20: "CESAR",
    23: "CORDOBA",
    25: "CUNDINAMARCA",
    27: "CHOCO",
    41: "HUILA",
    44: "GUAJIRA",
    47: "MAGDALENA",
    50: "META",
    52: "NARIÑO",
    54: "NORTE_DE_SANTANDER",
    63: "QUINDIO",
    66: "RISARALDA",
    68: "SANTANDER",
    70: "SUCRE",
    73: "TOLIMA",
    76: "VALLE_DEL_CAUCA",
    81: "ARAUCA",
    85: "CASANARE",
    86: "PUTUMAYO",
    91: "AMAZONAS",
    94: "GUAINIA",
    95: "GUAVIARE",
    97: "VAUPES",
    99: "VICHADA"
}
nombre_dpto = st.selectbox("Departamento", list(dptos.values()))
# Obtener código según nombre
DPTO = [codigo for codigo, nombre in dptos.items() if nombre == nombre_dpto][0]

# 5. Área de residencia (radio)
area = st.radio("Área de residencia", ["Urbano", "Rural"])
URBANO_RURAL_URBANO = 1 if area == "Urbano" else 0
URBANO_RURAL_RURAL = 1 if area == "Rural" else 0

# 6. Etnia (selección única, one-hot)
etnias = ["Indígena", "Rom", "Raizal", "Palenquero", "Afrodescendiente", "Ninguno"]
etnia_seleccionada = st.selectbox("Etnia", etnias)

ETNIA_INDIGENA = 1 if etnia_seleccionada == "Indígena" else 0
ETNIA_ROM = 1 if etnia_seleccionada == "Rom" else 0
ETNIA_RAIZAL = 1 if etnia_seleccionada == "Raizal" else 0
ETNIA_PALENQUERO = 1 if etnia_seleccionada == "Palenquero" else 0
ETNIA_AFRODESCENDIENTE = 1 if etnia_seleccionada == "Afrodescendiente" else 0
ETNIA_NINGUNO = 1 if etnia_seleccionada == "Ninguno" else 0

# 7. Grupo indígena (one-hot)
grupos_indigenas = ["Otro", "Embera", "Inga", "Kichwa", "Misak", "Nasa", "Wayuu", "Zenu", "AWA", "Ninguno"]
grupo_indigena_sel = st.selectbox("Grupo indígena", grupos_indigenas)

GRUPO_INDIGENA_AWA = 1 if grupo_indigena_sel == "AWA" else 0
GRUPO_INDIGENA_EMBERA = 1 if grupo_indigena_sel == "Embera" else 0
GRUPO_INDIGENA_INGA = 1 if grupo_indigena_sel == "Inga" else 0
GRUPO_INDIGENA_KICHWA = 1 if grupo_indigena_sel == "Kichwa" else 0
GRUPO_INDIGENA_MISAK = 1 if grupo_indigena_sel == "Misak" else 0
GRUPO_INDIGENA_NASA = 1 if grupo_indigena_sel == "Nasa" else 0
GRUPO_INDIGENA_WAYUU = 1 if grupo_indigena_sel == "Wayuu" else 0
GRUPO_INDIGENA_ZENU = 1 if grupo_indigena_sel == "Zenu" else 0
GRUPO_INDIGENA_OTRO = 1 if grupo_indigena_sel == "Otro" else 0
GRUPO_INDIGENA_NINGUNO = 1 if grupo_indigena_sel == "Ninguno" else 0

# 8. Nivel educativo máximo alcanzado
niveles_educativos = {
    3: "Básica secundaria",
    0: "Ningún nivel",
    1: "Preescolar",
    2: "Básica primaria",
    4: "Bachillerato clásico",
    5: "Bachillerato técnico",
    6: "Normalista",
    7: "Técnica profesional",
    8: "Tecnológica",
    9: "Universitaria",
    10: "Especialización",
    11: "Maestría",
    12: "Doctorado",
    -1: "No sabe"
}
nivel_educativo_sel = st.selectbox("Nivel educativo máximo alcanzado", list(niveles_educativos.values()))
# Mapear la selección al número
nivel_educativo_map = {v:k for k,v in niveles_educativos.items()}
MAXIMO_NIVEL_EDUCATIVO = nivel_educativo_map[nivel_educativo_sel]

# 9. ¿Sabe leer? (sí/no)
SABE_LEER = 1 if st.selectbox("¿Sabe leer?", ["Sí", "No"]) == "Sí" else 0

# 10. ¿Actualmente estudia? (sí/no)
ACTUALMENTE_ESTUDIA = 1 if st.selectbox("¿Actualmente estudia?", ["Sí", "No"]) == "Sí" else 0

# 11. Sector amplio de trabajo
diccionario_sector_amplio = {
    19.0: "OTRAS ACTIVIDADES DE SERVICIOS",
    0.0: "NO APLICA",
    1.0: "AGRICULTURA, GANADERÍA, CAZA, SILVICULTURA Y PESCA",
    2.0: "EXPLOTACIÓN DE MINAS Y CANTERAS",
    3.0: "INDUSTRIAS MANUFACTURERAS",
    4.0: "SUMINISTRO DE ELECTRICIDAD, GAS, VAPOR Y AIRE ACONDICIONADO",
    5.0: "SUMINISTRO DE AGUA; EVACUACIÓN DE AGUAS RESIDUALES, GESTIÓN DE DESECHOS Y ACTIVIDADES DE SANEAMIENTO AMBIENTAL",
    6.0: "CONSTRUCCIÓN",
    7.0: "COMERCIO AL POR MAYOR Y AL POR MENOR; REPARACIÓN DE VEHÍCULOS AUTOMOTORES Y MOTOCICLETAS",
    8.0: "TRANSPORTE Y ALMACENAMIENTO",
    9.0: "ALOJAMIENTO Y SERVICIOS DE COMIDA",
    10.0: "INFORMACIÓN Y COMUNICACIONES",
    11.0: "ACTIVIDADES FINANCIERAS Y DE SEGUROS",
    12.0: "ACTIVIDADES INMOBILIARIAS",
    13.0: "ACTIVIDADES PROFESIONALES, CIENTÍFICAS Y TÉCNICAS",
    14.0: "ACTIVIDADES DE SERVICIOS ADMINISTRATIVOS Y DE APOYO",
    15.0: "ADMINISTRACIÓN PÚBLICA Y DEFENSA; PLANES DE SEGURIDAD SOCIAL DE AFILIACIÓN OBLIGATORIA",
    16.0: "EDUCACIÓN",
    17.0: "ACTIVIDADES DE ATENCIÓN DE LA SALUD HUMANA Y DE ASISTENCIA SOCIAL",
    18.0: "ACTIVIDADES ARTÍSTICAS, DE ENTRETENIMIENTO Y RECREACIÓN",
    20.0: "ACTIVIDADES DE LOS HOGARES COMO EMPLEADORES; ACTIVIDADES NO DIFERENCIADAS DE LOS HOGARES COMO PRODUCTORES DE BIENES Y SERVICIOS PARA USO PROPIO",
    21.0: "ACTIVIDADES DE ORGANIZACIONES Y ÓRGANOS EXTRATERRITORIALES",
    97.0: "ACTIVIDADES NO ESPECIFICADAS",
    98.0: "ACTIVIDADES NO CLASIFICADAS",
    99.0: "NO INFORMADO"
}
sector_sel = st.selectbox("Sector amplio de trabajo", list(diccionario_sector_amplio.values()))
# Mapear al número
sector_map = {v:k for k,v in diccionario_sector_amplio.items()}
SECTOR_AMPLIO = sector_map[sector_sel]

# 12. Posición ocupacional (one-hot)
posiciones = [
    "Empleado empresa particular",
    "Empleado del gobierno",
    "Empleado doméstico",
    "Trabajador sin remuneración"
]
posicion_sel = st.selectbox("Posición ocupacional", posiciones)

POSICION_OCUPACIONAL_EMPLEADO_EMPRESA_PARTICULAR = 1 if posicion_sel == "Empleado empresa particular" else 0
POSICION_OCUPACIONAL_EMPLEADO_DEL_GOBIERNO = 1 if posicion_sel == "Empleado del gobierno" else 0
POSICION_OCUPACIONAL_EMPLEADO_DOMESTICO = 1 if posicion_sel == "Empleado doméstico" else 0
POSICION_OCUPACIONAL_TRABAJADOR_SIN_REMUNERACION = 1 if posicion_sel == "Trabajador sin remuneración" else 0

# 13. Tipo de contrato (one-hot)
tipos_contrato = ["Verbal", "Escrito", "No sabe"]
tipo_contrato_sel = st.selectbox("Tipo de contrato", tipos_contrato)

CONTRATO_VERBAL = 1 if tipo_contrato_sel == "Verbal" else 0
CONTRATO_ESCRITO = 1 if tipo_contrato_sel == "Escrito" else 0
CONTRATO_NO_SABE = 1 if tipo_contrato_sel == "No sabe" else 0

# 14. Término del contrato (one-hot)
terminos_contrato = ["Indefinido", "Fijo", "No sabe"]
termino_contrato_sel = st.selectbox("Término del contrato", terminos_contrato)

TERMINO_CONTRATO_INDEFINIDO = 1 if termino_contrato_sel == "Indefinido" else 0
TERMINO_CONTRATO_FIJO = 1 if termino_contrato_sel == "Fijo" else 0
TERMINO_CONTRATO_NO_SABE = 1 if termino_contrato_sel == "No sabe" else 0

# 15. ¿Su entidad de trabajo cuenta con seguridad social? (one-hot)
seguridad_social_opts = ["No", "Si", "No sabe"]
seguridad_social_sel = st.selectbox("¿Su entidad de trabajo cuenta con seguridad social?", seguridad_social_opts)

ENTIDAD_SEGURIDAD_SOCIAL_SALUD_SI = 1 if seguridad_social_sel == "Sí" else 0
ENTIDAD_SEGURIDAD_SOCIAL_SALUD_NO = 1 if seguridad_social_sel == "No" else 0
ENTIDAD_SEGURIDAD_SOCIAL_SALUD_NO_SABE = 1 if seguridad_social_sel == "No sabe" else 0

# 16. Tiempo trabajando en empresa actual (meses)
TIEMPO_TRABAJANDO_EMPRESA_ACTUAL = st.number_input("Tiempo trabajando en la empresa actual (meses)", min_value=0, max_value=1000, value=12, step=1)

# 17. Horas de trabajo a la semana
HORAS_TRABAJO = st.number_input("Horas de trabajo a la semana", min_value=0, max_value=168, value=20, step=1)

# 18. ¿Está conforme con su tipo de contrato? (sí/no)
CONFORME_TIPO_CONTRATO = 1 if st.selectbox("¿Está conforme con su tipo de contrato?", ["Sí", "No"]) == "Sí" else 0

# 19. Vacaciones pagas (sí/no)
VACACIONES_SUELDO = 1 if st.selectbox("Vacaciones pagas", ["No", "Si"]) == "Sí" else 0

# 20. Prima navideña (sí/no)
PRIMA_NAVIDAD = 1 if st.selectbox("Prima navideña", ["No", "Si"]) == "Sí" else 0

# 21. Cesantías (sí/no)
CESANTIA = 1 if st.selectbox("Cesantías", ["No", "Si"]) == "Sí" else 0

# 22. Licencia de enfermedad pagada (sí/no)
LICENCIA_ENFERMEDAD_PAGADA = 1 if st.selectbox("Licencia de enfermedad pagada", ["No", "Si"]) == "Sí" else 0

# 23. Prima de servicios (sí/no)
PRIMA_SERVICIOS = 1 if st.selectbox("Prima de servicios", ["No", "Si"]) == "Sí" else 0

# 24. La vivienda en la que vive es: one-hot
tipos_tenencia = [
    "No sabe", "Propia paga", "Propia pagando", "Arriendo", "Usufructo",
    "Posesión sin título", "Otro"
]
tenencia_sel = st.selectbox("La vivienda en la que vive es", tipos_tenencia)

TENENCIA_VIVIENDA_PROPIA_PAGA = 1 if tenencia_sel == "Propia paga" else 0
TENENCIA_VIVIENDA_PROPIA_PAGANDO = 1 if tenencia_sel == "Propia pagando" else 0
TENENCIA_VIVIENDA_ARRIENDO = 1 if tenencia_sel == "Arriendo" else 0
TENENCIA_VIVIENDA_USUFRUCTO = 1 if tenencia_sel == "Usufructo" else 0
TENENCIA_VIVIENDA_POSESION_SIN_TITULO = 1 if tenencia_sel == "Posesión sin título" else 0
TENENCIA_VIVIENDA_OTRO = 1 if tenencia_sel == "Otro" else 0
TENENCIA_VIVIENDA_NO_SABE = 1 if tenencia_sel == "No sabe" else 0

# 25. Tipo de vivienda: one-hot
tipos_vivienda = [
    "Casa", "Apartamento", "Cuarto/inquilinato",
    "Cuarto otra estructura", "Vivienda indígena", "Otro"
]
tipo_vivienda_sel = st.selectbox("Tipo de vivienda", tipos_vivienda)

TIPO_VIVIENDA_CASA = 1 if tipo_vivienda_sel == "Casa" else 0
TIPO_VIVIENDA_APARTAMENTO = 1 if tipo_vivienda_sel == "Apartamento" else 0
TIPO_VIVIENDA_CUARTO_INQUILINATO = 1 if tipo_vivienda_sel == "Cuarto/inquilinato" else 0
TIPO_VIVIENDA_CUARTO_OTRA_ESTRUCTURA = 1 if tipo_vivienda_sel == "Cuarto otra estructura" else 0
TIPO_VIVIENDA_VIVIENDA_INDIGENA = 1 if tipo_vivienda_sel == "Vivienda indígena" else 0
TIPO_VIVIENDA_OTRO = 1 if tipo_vivienda_sel == "Otro" else 0

# 26. Acceso a servicios públicos (sí/no)
ELECTRICIDAD = 1 if st.selectbox("Electricidad", ["Sí", "No"]) == "Sí" else 0
GAS_NATURAL = 1 if st.selectbox("Gas natural", ["Sí", "No"]) == "Sí" else 0
ACUEDUCTO = 1 if st.selectbox("Acueducto", ["Sí", "No"]) == "Sí" else 0
ALCANTARILLADO = 1 if st.selectbox("Alcantarillado", ["Sí", "No"]) == "Sí" else 0
RECOLECCION_BASURA = 1 if st.selectbox("Recolección de basura", ["Sí", "No"]) == "Sí" else 0

# Lista de fuentes de agua potable
fuentes_agua_potable = [
    "Acueducto tubería",
    "Otra fuente tubería",
    "Pozo con bomba",
    "Pozo sin bomba",
    "Aguas lluvias",
    "Río o similares",
    "Pila pública",
    "Carro tanque",
    "Aguatero",
    "Agua embotellada"
]

fuente_agua_sel = st.selectbox("Fuente de agua potable principal", fuentes_agua_potable)

# Crear variables binarias
AGUA_POTABLE_ACUEDUCTO_TUBERIA = 1 if fuente_agua_sel == "Acueducto tubería" else 0
AGUA_POTABLE_OTRA_FUENTE_TUBERIA = 1 if fuente_agua_sel == "Otra fuente tubería" else 0
AGUA_POTABLE_POZO_BOMBA = 1 if fuente_agua_sel == "Pozo con bomba" else 0
AGUA_POTABLE_POZO_SIN_BOMBA = 1 if fuente_agua_sel == "Pozo sin bomba" else 0
AGUA_POTABLE_AGUAS_LLUVIAS = 1 if fuente_agua_sel == "Aguas lluvias" else 0
AGUA_POTABLE_RIO_SIMILARES = 1 if fuente_agua_sel == "Río o similares" else 0
AGUA_POTABLE_PILA_PUBLICA = 1 if fuente_agua_sel == "Pila pública" else 0
AGUA_POTABLE_CARRO_TANQUE = 1 if fuente_agua_sel == "Carro tanque" else 0
AGUA_POTABLE_AGUATERO = 1 if fuente_agua_sel == "Aguatero" else 0
AGUA_POTABLE_AGUA_EMBOTELLADA = 1 if fuente_agua_sel == "Agua embotellada" else 0

# 28. Total personas en su hogar (numérico)
TOTAL_PERSONAS_HOGAR = st.number_input("Total personas en su hogar", min_value=1, max_value=20, value=8, step=1)

# 29. Actividades en su hogar (sí/no)
LIMPIEZA_EN_SU_HOGAR = 1 if st.selectbox("Limpieza en su hogar", ["Sí", "No"]) == "Sí" else 0
CUIDADO_NINOS_SU_HOGAR = 1 if st.selectbox("Cuidado niños en su hogar", ["Sí", "No"]) == "Sí" else 0
CUIDADO_MAYORES_SU_HOGAR = 1 if st.selectbox("Cuidado mayores en su hogar", ["Sí", "No"]) == "Sí" else 0
APOYO_TAREAS_SU_HOGAR = 1 if st.selectbox("Apoyo en tareas del hogar", ["Sí", "No"]) == "Sí" else 0

# 30. Días y horas dedicados a tareas domésticas (numéricos)
LIMPIEZA_EN_SU_HOGAR_DIAS = st.number_input("Días limpieza en hogar", min_value=0, max_value=31, value=5, step=1)
LIMPIEZA_EN_SU_HOGAR_HORAS_DIA = st.number_input("Horas limpieza por día", min_value=0, max_value=24, value=2, step=1)
CUIDADO_MAYORES_SU_HOGAR_DIAS = st.number_input("Días cuidando mayores", min_value=0, max_value=31, value=5, step=1)
CUIDADO_MAYORES_SU_HOGAR_HORAS_DIA = st.number_input("Horas cuidando mayores por día", min_value=0, max_value=24, value=1, step=1)
CUIDADO_NINOS_SU_HOGAR_DIAS = st.number_input("Días cuidando niños", min_value=0, max_value=31, value=5, step=1)
CUIDADO_NINOS_SU_HOGAR_HORAS_DIA = st.number_input("Horas cuidando niños por día", min_value=0, max_value=24, value=1, step=1)

# 31. Actividad mayoritaria (one-hot)
actividades_mayor = ["Estudiando", "Trabajando", "Buscando trabajo", "Oficios del hogar", "Otro"]
actividad_sel = st.selectbox("Actividad mayoritaria", actividades_mayor)

ACTIVIDAD_MAYOR_TIEMPO_TRABAJANDO = 1 if actividad_sel == "Trabajando" else 0
ACTIVIDAD_MAYOR_TIEMPO_BUSCANDO_TRABAJO = 1 if actividad_sel == "Buscando trabajo" else 0
ACTIVIDAD_MAYOR_TIEMPO_ESTUDIANDO = 1 if actividad_sel == "Estudiando" else 0
ACTIVIDAD_MAYOR_TIEMPO_OFICIOS_DEL_HOGAR = 1 if actividad_sel == "Oficios del hogar" else 0
ACTIVIDAD_MAYOR_TIEMPO_OTRO = 1 if actividad_sel == "Otro" else 0

# 32. Atracción por (one-hot)
atracciones = ["Ambos", "Hombres", "Mujeres", "Otro"]
atraccion_sel = st.selectbox("Atracción por", atracciones)

ATRACCION_POR_HOMBRES = 1 if atraccion_sel == "Hombres" else 0
ATRACCION_POR_MUJERES = 1 if atraccion_sel == "Mujeres" else 0
ATRACCION_POR_AMBOS = 1 if atraccion_sel == "Ambos" else 0
ATRACCION_POR_OTRO = 1 if atraccion_sel == "Otro" else 0

# 33. Sexo de nacimiento
sexo_nacimiento_sel = st.selectbox("Sexo de nacimiento", ["Mujer", "Hombre"])
SEXO_NACIMIENTO_HOMBRE = 1 if sexo_nacimiento_sel == "Hombre" else 0
SEXO_NACIMIENTO_MUJER = 1 if sexo_nacimiento_sel == "Mujer" else 0

# 34. ¿Es campesino? (one-hot)
campesino_opts = ["No", "Si", "No sabe"]
campesino_sel = st.selectbox("¿Es campesino?", campesino_opts)

CAMPESINO_SI = 1 if campesino_sel == "Sí" else 0
CAMPESINO_NO = 1 if campesino_sel == "No" else 0
CAMPESINO_NO_SABE = 1 if campesino_sel == "No sabe" else 0



data = {
    "EDAD": EDAD,
    "ESTRATO": ESTRATO,
    "ELECTRICIDAD": ELECTRICIDAD,
    "GAS_NATURAL": GAS_NATURAL,
    "DPTO": DPTO,
    "ACUEDUCTO": ACUEDUCTO,
    "ALCANTARILLADO": ALCANTARILLADO,
    "RECOLECCION_BASURA": RECOLECCION_BASURA,
    "TOTAL_PERSONAS_HOGAR": TOTAL_PERSONAS_HOGAR,
    "MAXIMO_NIVEL_EDUCATIVO": MAXIMO_NIVEL_EDUCATIVO,
    "SABE_LEER": SABE_LEER,
    "HORAS_TRABAJO": HORAS_TRABAJO,
    "CONFORME_TIPO_CONTRATO": CONFORME_TIPO_CONTRATO,
    "VACACIONES_SUELDO": VACACIONES_SUELDO,
    "PRIMA_NAVIDAD": PRIMA_NAVIDAD,
    "CESANTIA": CESANTIA,
    "LICENCIA_ENFERMEDAD_PAGADA": LICENCIA_ENFERMEDAD_PAGADA,
    "TIEMPO_TRABAJANDO_EMPRESA_ACTUAL": TIEMPO_TRABAJANDO_EMPRESA_ACTUAL,
    "PRIMA_SERVICIOS": PRIMA_SERVICIOS,
    "SECTOR_AMPLIO": SECTOR_AMPLIO,
    "ACTUALMENTE_ESTUDIA": ACTUALMENTE_ESTUDIA,
    "LIMPIEZA_EN_SU_HOGAR": LIMPIEZA_EN_SU_HOGAR,
    "CUIDADO_NINOS_SU_HOGAR": CUIDADO_NINOS_SU_HOGAR,
    "CUIDADO_MAYORES_SU_HOGAR": CUIDADO_MAYORES_SU_HOGAR,
    "APOYO_TAREAS_SU_HOGAR": APOYO_TAREAS_SU_HOGAR,
    "LIMPIEZA_EN_SU_HOGAR_DIAS": LIMPIEZA_EN_SU_HOGAR_DIAS,
    "LIMPIEZA_EN_SU_HOGAR_HORAS_DIA": LIMPIEZA_EN_SU_HOGAR_HORAS_DIA,
    "CUIDADO_MAYORES_SU_HOGAR_DIAS": CUIDADO_MAYORES_SU_HOGAR_DIAS,
    "CUIDADO_MAYORES_SU_HOGAR_HORAS_DIA": CUIDADO_MAYORES_SU_HOGAR_HORAS_DIA,
    "CUIDADO_NINOS_SU_HOGAR_DIAS": CUIDADO_NINOS_SU_HOGAR_DIAS,
    "CUIDADO_NINOS_SU_HOGAR_HORAS_DIA": CUIDADO_NINOS_SU_HOGAR_HORAS_DIA,
    "AGUA_POTABLE_ACUEDUCTO_TUBERIA": AGUA_POTABLE_ACUEDUCTO_TUBERIA,
    "AGUA_POTABLE_OTRA_FUENTE_TUBERIA": AGUA_POTABLE_OTRA_FUENTE_TUBERIA,
    "AGUA_POTABLE_POZO_BOMBA": AGUA_POTABLE_POZO_BOMBA,
    "AGUA_POTABLE_POZO_SIN_BOMBA": AGUA_POTABLE_POZO_SIN_BOMBA,
    "AGUA_POTABLE_AGUAS_LLUVIAS": AGUA_POTABLE_AGUAS_LLUVIAS,
    "AGUA_POTABLE_RIO_SIMILARES": AGUA_POTABLE_RIO_SIMILARES,
    "AGUA_POTABLE_PILA_PUBLICA": AGUA_POTABLE_PILA_PUBLICA,
    "AGUA_POTABLE_CARRO_TANQUE": AGUA_POTABLE_CARRO_TANQUE,
    "AGUA_POTABLE_AGUATERO": AGUA_POTABLE_AGUATERO,
    "AGUA_POTABLE_AGUA_EMBOTELLADA": AGUA_POTABLE_AGUA_EMBOTELLADA,
    "GENERO_HOMBRE": GENERO_HOMBRE,
    "GENERO_MUJER": GENERO_MUJER,
    "GENERO_HOMBRE_TRANS": GENERO_HOMBRE_TRANS,
    "GENERO_MUJER_TRANS": GENERO_MUJER_TRANS,
    "ENTIDAD_SEGURIDAD_SOCIAL_SALUD_SI": ENTIDAD_SEGURIDAD_SOCIAL_SALUD_SI,
    "ENTIDAD_SEGURIDAD_SOCIAL_SALUD_NO": ENTIDAD_SEGURIDAD_SOCIAL_SALUD_NO,
    "ENTIDAD_SEGURIDAD_SOCIAL_SALUD_NO_SABE": ENTIDAD_SEGURIDAD_SOCIAL_SALUD_NO_SABE,
    "URBANO_RURAL_URBANO": URBANO_RURAL_URBANO,
    "URBANO_RURAL_RURAL": URBANO_RURAL_RURAL,
    "TENENCIA_VIVIENDA_PROPIA_PAGA": TENENCIA_VIVIENDA_PROPIA_PAGA,
    "TENENCIA_VIVIENDA_PROPIA_PAGANDO": TENENCIA_VIVIENDA_PROPIA_PAGANDO,
    "TENENCIA_VIVIENDA_ARRIENDO": TENENCIA_VIVIENDA_ARRIENDO,
    "TENENCIA_VIVIENDA_USUFRUCTO": TENENCIA_VIVIENDA_USUFRUCTO,
    "TENENCIA_VIVIENDA_POSESION_SIN_TITULO": TENENCIA_VIVIENDA_POSESION_SIN_TITULO,
    "TENENCIA_VIVIENDA_OTRO": TENENCIA_VIVIENDA_OTRO,
    "TENENCIA_VIVIENDA_NO_SABE": TENENCIA_VIVIENDA_NO_SABE,
    "ETNIA_INDIGENA": ETNIA_INDIGENA,
    "ETNIA_ROM": ETNIA_ROM,
    "ETNIA_RAIZAL": ETNIA_RAIZAL,
    "ETNIA_PALENQUERO": ETNIA_PALENQUERO,
    "ETNIA_AFRODESCENDIENTE": ETNIA_AFRODESCENDIENTE,
    "ETNIA_NINGUNO": ETNIA_NINGUNO,
    "ACTIVIDAD_MAYOR_TIEMPO_TRABAJANDO": ACTIVIDAD_MAYOR_TIEMPO_TRABAJANDO,
    "ACTIVIDAD_MAYOR_TIEMPO_BUSCANDO_TRABAJO": ACTIVIDAD_MAYOR_TIEMPO_BUSCANDO_TRABAJO,
    "ACTIVIDAD_MAYOR_TIEMPO_ESTUDIANDO": ACTIVIDAD_MAYOR_TIEMPO_ESTUDIANDO,
    "ACTIVIDAD_MAYOR_TIEMPO_OFICIOS_DEL_HOGAR": ACTIVIDAD_MAYOR_TIEMPO_OFICIOS_DEL_HOGAR,
    "ACTIVIDAD_MAYOR_TIEMPO_OTRO": ACTIVIDAD_MAYOR_TIEMPO_OTRO,
    "TIPO_VIVIENDA_CASA": TIPO_VIVIENDA_CASA,
    "TIPO_VIVIENDA_APARTAMENTO": TIPO_VIVIENDA_APARTAMENTO,
    "TIPO_VIVIENDA_CUARTO_INQUILINATO": TIPO_VIVIENDA_CUARTO_INQUILINATO,
    "TIPO_VIVIENDA_CUARTO_OTRA_ESTRUCTURA": TIPO_VIVIENDA_CUARTO_OTRA_ESTRUCTURA,
    "TIPO_VIVIENDA_VIVIENDA_INDIGENA": TIPO_VIVIENDA_VIVIENDA_INDIGENA,
    "TIPO_VIVIENDA_OTRO": TIPO_VIVIENDA_OTRO,
    "TERMINO_CONTRATO_INDEFINIDO": TERMINO_CONTRATO_INDEFINIDO,
    "TERMINO_CONTRATO_FIJO": TERMINO_CONTRATO_FIJO,
    "TERMINO_CONTRATO_NO_SABE": TERMINO_CONTRATO_NO_SABE,
    "ATRACCION_POR_HOMBRES": ATRACCION_POR_HOMBRES,
    "ATRACCION_POR_MUJERES": ATRACCION_POR_MUJERES,
    "ATRACCION_POR_AMBOS": ATRACCION_POR_AMBOS,
    "ATRACCION_POR_OTRO": ATRACCION_POR_OTRO,
    "GRUPO_INDIGENA_AWA": GRUPO_INDIGENA_AWA,
    "GRUPO_INDIGENA_EMBERA": GRUPO_INDIGENA_EMBERA,
    "GRUPO_INDIGENA_INGA": GRUPO_INDIGENA_INGA,
    "GRUPO_INDIGENA_KICHWA": GRUPO_INDIGENA_KICHWA,
    "GRUPO_INDIGENA_MISAK": GRUPO_INDIGENA_MISAK,
    "GRUPO_INDIGENA_NASA": GRUPO_INDIGENA_NASA,
    "GRUPO_INDIGENA_NINGUNO": GRUPO_INDIGENA_NINGUNO,
    "GRUPO_INDIGENA_OTRO": GRUPO_INDIGENA_OTRO,
    "GRUPO_INDIGENA_WAYUU": GRUPO_INDIGENA_WAYUU,
    "GRUPO_INDIGENA_ZENU": GRUPO_INDIGENA_ZENU,
    "POSICION_OCUPACIONAL_EMPLEADO_EMPRESA_PARTICULAR": POSICION_OCUPACIONAL_EMPLEADO_EMPRESA_PARTICULAR,
    "POSICION_OCUPACIONAL_EMPLEADO_DEL_GOBIERNO": POSICION_OCUPACIONAL_EMPLEADO_DEL_GOBIERNO,
    "POSICION_OCUPACIONAL_EMPLEADO_DOMESTICO": POSICION_OCUPACIONAL_EMPLEADO_DOMESTICO,
    "POSICION_OCUPACIONAL_TRABAJADOR_SIN_REMUNERACION": POSICION_OCUPACIONAL_TRABAJADOR_SIN_REMUNERACION,
    "CAMPESINO_SI": CAMPESINO_SI,
    "CAMPESINO_NO": CAMPESINO_NO,
    "CAMPESINO_NO_SABE": CAMPESINO_NO_SABE,
    "CONTRATO_VERBAL": CONTRATO_VERBAL,
    "CONTRATO_ESCRITO": CONTRATO_ESCRITO,
    "CONTRATO_NO_SABE": CONTRATO_NO_SABE,
}

df_input = pd.DataFrame([data])

# Ajustar columnas que falten o estén demás según modelo
columnas_esperadas = modelo.get_booster().feature_names

for col in columnas_esperadas:
    if col not in df_input.columns:
        df_input[col] = 0

df_input = df_input[columnas_esperadas]

# Botón para predecir
if st.button("Predecir ingreso mensual"):
    try:
        pred = modelo.predict(df_input)
        st.success(f"Ingreso mensual predicho: ${pred[0]:,.0f} COP")
    except Exception as e:
        st.error(f"Error en la predicción: {e}")



st.markdown("---")  # Separador visual

st.markdown(
    """
    <div style="font-size:14px; color: #555; padding: 10px;">
        <h4>Sobre esta aplicación</h4>
        <p><strong>Autores:</strong> Juan David Cetina Gómez, Mariana Salas Gutiérrez, Katherin Juliana Moreno Carvajal</p>
        <p><strong>Descripción:</strong> Esta aplicación predice el ingreso mensual basado en datos socioeconómicos usando un modelo XGBoost entrenado con la encuesta GEIH Colombia.</p>
        <p><strong>Limitaciones del modelo:</strong> Esta predicción se basa en patrones históricos y no garantiza exactitud en casos individuales. El modelo puede presentar sesgos inherentes a los datos de entrenamiento.</p>
        <p>Besitos, 5.0 Profe.</p>
        <p>© 2025 Todos los derechos reservados.</p>
    </div>
    """,
    unsafe_allow_html=True
)
