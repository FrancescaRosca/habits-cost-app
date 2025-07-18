import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="The Real Cost", layout="centered")

st.title("El coste de tus hábitos")
st.markdown("Descubre el impacto acumulado de pequeños gastos, hábitos o elecciones cotidianas")

def obtener_unidad(tipo):
    if "Dinero" in tipo:
        return "€"
    elif "Tiempo" in tipo:
        return "minutos"
    elif "Energía" in tipo:
        return "pts de energía"
    else:
        return tipo

st.subheader("Introduce los detalles:")

with st.form("formulario_coste"):
    nombre = st.text_input("¿Qué estás calculando?", placeholder="Ej. Café de máquina")
    tipo = st.selectbox("¿A cambio de qué?", ["Dinero (€)", "Tiempo (minutos)", "Energía mental"])

    if "Dinero" in tipo:
        freq_label = "¿Cuántas unidades compras o consumes?"
    elif "Tiempo" in tipo:
        freq_label = "¿Cuántas veces haces esto?"
    else:
        freq_label = "¿Con qué frecuencia ocurre esto?"

    frecuencia = st.number_input(freq_label, min_value=0, step=1, format="%d")

    frecuencia_tipo = st.selectbox(
        "¿Con qué frecuencia ocurre?",
        ["a diario", "semanalmente", "menusualmente", "anualmente"]
    )

    coste_unitario = st.number_input("¿Cuánto cuesta cada vez?", min_value=0.0, step=0.1)

    duración = st.selectbox("¿Durante cuánto tiempo quieres calcularlo?", ["1 semana", "1 mes", "1 año", "5 años"])

    enviar = st.form_submit_button("Calcular")

# Nota y explicación del modelo de cálculo
st.caption("📌 Calculamos con medias exactas: 30,42 días por mes, 52 semanas por año...")

with st.expander("ℹ️ ¿Cómo se calculan los periodos?"):
    st.markdown("""
Usamos medias exactas en lugar de redondeos para que los resultados sean más realistas:

- 1 año tiene **365 días**, que son **52,14 semanas**
- 1 mes tiene **365 / 12 ≈ 30,42 días**
- Por tanto, 1 mes equivale a **~4,35 semanas**
- Esto evita errores acumulados en cálculos anuales o a largo plazo
""")

if enviar:
    unidad = obtener_unidad(tipo)

    # Frecuencias reales por periodo
    factor_periodo = {
        "1 semana": {
            "al día": 7,
            "a la semana": 1,
            "al mes": 1 / 4.35,
            "al año": 1 / 52.14
        },
        "1 mes": {
            "al día": 30.42,
            "a la semana": 4.35,
            "al mes": 1,
            "al año": 1 / 12
        },
        "1 año": {
            "al día": 365,
            "a la semana": 52.14,
            "al mes": 12,
            "al año": 1
        },
        "5 años": {
            "al día": 365 * 5,
            "a la semana": 52.14 * 5,
            "al mes": 12 * 5,
            "al año": 5
        }
    }

    resultados = {}
    for periodo in ["a diario", "semanalmente", "menusualmente", "anualmente"]:
        ocurrencias = frecuencia * factor_periodo[periodo][frecuencia_tipo]
        total = ocurrencias * coste_unitario
        resultados[periodo] = total

    st.subheader(f"📊 Resultados para: **{nombre}**")

    for periodo, valor in resultados.items():
        if unidad == "€":
            st.write(f"🔸 En {periodo}: **{valor:,.2f} €**")
        else:
            st.write(f"🔸 En {periodo}: **{int(valor)} {unidad}**")

    if "Dinero" in tipo:
        st.subheader("💡 ¿Qué podrías hacer con ese dinero?")
        if resultados["1 año"] > 1000:
            st.write("📱 Comprar un móvil nuevo")
        if resultados["1 año"] > 2000:
            st.write("✈️ Hacer un viaje internacional")
        if resultados["5 años"] > 5000:
            st.write("🚗 Dar la entrada de un coche")
    elif "Tiempo" in tipo:
        st.subheader("💡 ¿Qué podrías haber hecho con ese tiempo?")
        horas = resultados["1 año"] / 60
        libros = int(horas / 6)
        st.write(f"📚 Leer unos {libros} libros al año (suponiendo 6h por libro)")
        st.write(f"🧘 Pasar {horas:.1f} horas en autocuidado")

    st.subheader("📈 Evolución acumulada")
    df = pd.DataFrame({
        "Periodo": list(resultados.keys()),
        "Coste acumulado": list(resultados.values())
    })

    fig, ax = plt.subplots()
    ax.bar(df["Periodo"], df["Coste acumulado"], color="#4E79A7")
    ax.set_ylabel(unidad)
    ax.set_title(f"Coste acumulado de {nombre}")
    st.pyplot(fig)
