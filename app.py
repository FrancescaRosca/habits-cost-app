import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora de hábitos", layout="centered")

st.title("🧮 Calculadora de Coste Real de Hábitos")
st.markdown("Descubre el impacto acumulado de decisiones pequeñas en tu tiempo, dinero o energía.")

st.subheader("Introduce tu hábito:")

# Formulario
with st.form("hábito_formulario"):
    nombre = st.text_input("Nombre del hábito", placeholder="Ej. Café de máquina")
    tipo = st.selectbox("Tipo de impacto", ["Dinero (€)", "Tiempo (minutos)", "Energía mental"])
    frecuencia = st.number_input("¿Cuántas veces lo haces al día?", min_value=0.0, step=0.1)
    coste_unitario = st.number_input("Coste por vez (en la unidad seleccionada)", min_value=0.0, step=0.1)
    enviar = st.form_submit_button("Calcular")

# Procesamiento
if enviar:
    unidades = tipo.split()[0]  # "Dinero", "Tiempo", "Energía"
    periodos = {
        "1 semana": 7,
        "1 mes": 30,
        "1 año": 365,
        "5 años": 365 * 5
    }

    resultados = {
        periodo: frecuencia * coste_unitario * días
        for periodo, días in periodos.items()
    }

    st.subheader(f"Resultados para: **{nombre}**")

    for periodo, valor in resultados.items():
        st.write(f"🔸 En {periodo}: **{valor:.2f} {unidades}**")

    # Comparaciones posibles
    if tipo.startswith("Dinero"):
        st.subheader("💡 ¿Qué podrías hacer con ese dinero?")
        if resultados["1 año"] > 1000:
            st.write("📱 Comprar un móvil nuevo")
        if resultados["1 año"] > 2000:
            st.write("✈️ Hacer un viaje internacional")
        if resultados["5 años"] > 5000:
            st.write("🚗 Dar la entrada de un coche")

    elif tipo.startswith("Tiempo"):
        st.subheader("💡 ¿Qué podrías haber hecho con ese tiempo?")
        minutos = resultados["1 año"]
        horas = minutos / 60
        libros = int(horas / 6)
        st.write(f"📚 Leer unos {libros} libros al año (suponiendo 6h por libro)")
        st.write(f"🧘 Pasar {horas:.1f} horas cuidándote")

    # Gráfica acumulativa
    st.subheader("📈 Evolución acumulada")
    df = pd.DataFrame({
        "Periodo": list(resultados.keys()),
        "Coste acumulado": list(resultados.values())
    })

    fig, ax = plt.subplots()
    ax.bar(df["Periodo"], df["Coste acumulado"], color="#4E79A7")
    ax.set_ylabel(unidades)
    ax.set_title(f"Coste acumulado de {nombre}")
    st.pyplot(fig)
