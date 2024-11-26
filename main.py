import streamlit as st
from alianz2 import ejecutar_etfs  # Cambia el nombre si usas otro
from acciones2 import ejecutar_acciones  # Cambia el nombre si usas otro

# Verificar si ya se completó la página de bienvenida
if 'welcome' not in st.session_state:
    st.session_state['welcome'] = False

# Si aún no se ha completado la página de bienvenida
if not st.session_state['welcome']:
    # URL de la imagen
    image_url = "https://lh3.googleusercontent.com/a/ACg8ocJRBWqWITdSZLCQpa9b-htwGwyA_KwQ_PQbAWgXP-b7x8mv7ug0INBi1YEZbuse4oKDTiYlptGQ_uX275FjzP5Yl2YRDiDp=s411-c-no"
    st.markdown(f'<div style="text-align: center;"><img src="{image_url}" width="300"></div>', unsafe_allow_html=True)
    # Mostrar la imagen

    st.title("Bienvenido a DiviGrowth")

    st.write("""
        **DiviGrowth** es una empresa que se dedica a ayudarte a hacer crecer tu capital. 
        Nuestro objetivo es ofrecerte herramientas de fácil acceso para que puedas evaluar las mejores opciones de inversión disponibles. 
        Ya sea que busques diversificar tu portafolio o encontrar la opción más rentable para ti, 
        en DiviGrowth encontrarás las herramientas necesarias para tomar decisiones informadas y rentables. 
        Con nuestro simulador, podrás experimentar y aprender sobre las distintas alternativas de inversión, 
        ¡y comenzar a dar los primeros pasos hacia el crecimiento de tu patrimonio!
    """)

    # Entrada de nombre y número
    nombre = st.text_input("Introduce tu nombre")
    numero = st.text_input("Introduce tu número celular", type="default")

    # Selector de inversión antes de continuar
    inversion_seleccionada = st.radio("¿En qué estás interesado invertir?", ("Acciones", "ETFs"))

    # Mostrar la descripción automáticamente según la opción seleccionada
    if inversion_seleccionada == "Acciones":
        st.write("""
            Las **Acciones** son una parte de la propiedad de una empresa. Al comprar una acción, te conviertes en accionista de la compañía, y tu participación puede aumentar o disminuir dependiendo de su desempeño en el mercado.
        """)
    elif inversion_seleccionada == "ETFs":
        st.write("""
            **ETFs (Fondos Cotizados en Bolsa)** son fondos de inversión que contienen una variedad de activos (como acciones, bonos, etc.), y se pueden comprar y vender en la bolsa de valores como si fueran acciones individuales. Son más diversificados que las acciones individuales.
        """)
    st.write("""
        Si hay algún instrumento en específico que no esté dentro del simulador que te interese,
             puedes contactarte con danielsandoval@gmail.com
    """)
    # Botón para continuar
    if st.button("Continuar") and nombre and numero:
        st.session_state['nombre'] = nombre
        st.session_state['numero'] = numero
        st.session_state['inversion_seleccionada'] = inversion_seleccionada  # Guardamos la selección
        st.session_state['welcome'] = True  # Marcamos que la página de bienvenida se completó
        # Usamos una actualización de la página con la opción seleccionada sin rerun.
else:
    # Página principal con opciones de inversión ya seleccionadas
    st.title("Simulador de Inversión")

    # Obtener la inversión seleccionada
    inversion_seleccionada = st.session_state['inversion_seleccionada']

    # Mostrar el análisis correspondiente según la selección
    if inversion_seleccionada == "ETFs":
        st.subheader("Análisis de ETFs")
        ejecutar_etfs()  # Ejecuta el código de ETFs

    elif inversion_seleccionada == "Acciones":
        st.subheader("Análisis de Acciones")
        ejecutar_acciones()  # Ejecuta el código de Acciones
