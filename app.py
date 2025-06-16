import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Los costes de tus hábitos", layout="centered")

st.title("🧮 Calculadora de costes reales de hábitos")
st.markdown("Descubre el impacto acumulado de decisiones pequeñas en tu tiempo, dinero o energía.")

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

# Formulario a rellenar por el usuario
with st.form("hábito_formulario"):
    nombre = st.text_input("¿Qué estás calculando?", placeholder="Ej. Café de máquina")
    tipo = st.selectbox("¿A cambio de qué?", ["Dinero (€)", "Tiempo (minutos)", "Energía mental"])
    
    if "Dinero" in tipo:
        freq_label = "¿Cuántas unidades compras o consumes al día?"
    elif "Tiempo" in tipo:
        freq_label = "¿Cuántas veces haces esto al día?"
    else:
        freq_label = "¿Con qué frecuencia al día ocurre esto?"

    frecuencia = st.number_input("¿Cuántas veces lo haces al día?", min_value=0, step=1, format="%d")
    coste_unitario = st.number_input("Coste por vez (en la unidad seleccionada)", min_value=0.0, step=0.1)
    duración = st.selectbox("¿Durante cuánto tiempo quieres calcularlo?", ["1 semana", "1 mes", "1 año", "5 años"])
    enviar = st.form_submit_button("Calcular")

# Procesamiento de la información para la devolución de resultados
if enviar:
    unidad = obtener_unidad(tipo)

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
        st.write(f"📚 Leer unos {libros} libros al año (a una media de 6h por libro)")
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