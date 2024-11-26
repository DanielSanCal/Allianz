import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def ejecutar_acciones():
    # Diccionario de símbolos a nombres completos y descripciones
    acciones_sp500 = {
        "AAPL": {"name": "Apple", "description": "Diseña y fabrica productos electrónicos como el iPhone, iPad y Mac."},
        "MSFT": {"name": "Microsoft", "description": "Proveedor líder de software, servicios en la nube y hardware."},
        "GOOGL": {"name": "Alphabet (Google)", "description": "Gigante de internet con foco en búsquedas, publicidad y tecnología."},
        "AMZN": {"name": "Amazon", "description": "Principal minorista en línea con servicios en la nube (AWS)."},
        "TSLA": {"name": "Tesla", "description": "Fabricante de vehículos eléctricos y sistemas de energía solar."},
        "NVDA": {"name": "NVIDIA", "description": "Desarrolla GPUs y tecnología de inteligencia artificial."},
        "META": {"name": "Meta Platforms (Facebook)", "description": "Opera redes sociales como Facebook, Instagram y WhatsApp."},
        "JPM": {"name": "JPMorgan Chase", "description": "Banco líder en servicios financieros globales."},
        "V": {"name": "Visa", "description": "Empresa global de pagos electrónicos."},
        "JNJ": {"name": "Johnson & Johnson", "description": "Multinacional de productos farmacéuticos y de cuidado personal."},
        "WMT": {"name": "Walmart", "description": "Cadena minorista más grande del mundo."},
        "PG": {"name": "Procter & Gamble", "description": "Fabricante de productos de consumo como detergentes y cosméticos."},
        "DIS": {"name": "Disney", "description": "Líder en entretenimiento y medios con parques temáticos y estudios."},
        "MA": {"name": "Mastercard", "description": "Empresa global de tecnología de pagos electrónicos."},
        "HD": {"name": "Home Depot", "description": "Principal minorista de mejoras para el hogar."},
        "XOM": {"name": "Exxon Mobil", "description": "Una de las mayores compañías de energía y petróleo del mundo."},
        "CVX": {"name": "Chevron", "description": "Multinacional energética con enfoque en petróleo y gas."},
        "PFE": {"name": "Pfizer", "description": "Empresa farmacéutica conocida por desarrollar vacunas y medicamentos."},
        "KO": {"name": "Coca-Cola", "description": "Líder mundial en bebidas no alcohólicas."},
        "PEP": {"name": "PepsiCo", "description": "Fabricante global de alimentos y bebidas."},
        "ADBE": {"name": "Adobe", "description": "Empresa líder en software de diseño y marketing digital."},
        "NFLX": {"name": "Netflix", "description": "Proveedor global de streaming de series y películas."},
        "NKE": {"name": "Nike", "description": "Fabricante líder de ropa y calzado deportivo."},
        "T": {"name": "AT&T", "description": "Empresa de telecomunicaciones y entretenimiento."},
        "INTC": {"name": "Intel", "description": "Fabricante líder de microprocesadores y semiconductores."},
        "CSCO": {"name": "Cisco", "description": "Proveedor de tecnología de redes y seguridad."},
        "CRM": {"name": "Salesforce", "description": "Líder en software de gestión de relaciones con clientes (CRM)."},
        "ORCL": {"name": "Oracle", "description": "Empresa de software y soluciones en la nube."},
        "IBM": {"name": "IBM", "description": "Proveedor de soluciones tecnológicas y consultoría."},
        "COST": {"name": "Costco", "description": "Minorista de membresía conocido por su valor y calidad."},
    }

    # Función para obtener datos de acciones con un periodo específico
    @st.cache_data
    def obtener_acciones_periodo(period):
        resultados = []
        for simbolo, datos in acciones_sp500.items():
            try:
                historial = yf.Ticker(simbolo).history(period=period)
                if not historial.empty:
                    rendimiento_anualizado = ((historial["Close"].iloc[-1] / historial["Close"].iloc[0]) - 1) * 100
                    resultados.append({
                        "Acción": simbolo,
                        "Nombre": datos["name"],
                        "Descripción": datos["description"],
                        "Rendimiento Anualizado (%)": rendimiento_anualizado,
                        "Datos": historial
                    })
            except Exception:
                continue
        return resultados

    # Página principal de la aplicación
    st.sidebar.title("Selecciona las Acciones")
    nombres_completos = [datos["name"] for datos in acciones_sp500.values()]
    seleccionadas_nombres = st.sidebar.multiselect("Selecciona una o más acciones", nombres_completos)
    periodo = st.sidebar.selectbox("Selecciona el período de análisis", ["5d", "1mo", "3mo", "6mo", "1y", "5y", "10y"])

   
    if seleccionadas_nombres:
        datos_seleccionados = [
            {"Símbolo": simbolo, "Nombre": datos["name"], "Descripción": datos["description"]}
            for simbolo, datos in acciones_sp500.items() if datos["name"] in seleccionadas_nombres
        ]
        st.write("### Detalles de Acciones")
        st.table(pd.DataFrame(datos_seleccionados))

        resumen_rendimientos = []
        resumen_volatilidad = []

        st.write("### Gráfica de Rendimiento")
        plt.figure(figsize=(10, 6))
        for seleccion in datos_seleccionados:
            simbolo = seleccion["Símbolo"]
            ticker = yf.Ticker(simbolo)
            datos = ticker.history(period=periodo)

            if not datos.empty:
                # Cálculos para la tabla de rendimiento (en porcentaje)
                datos['Rendimiento'] = (datos['Close'] / datos['Close'].iloc[0] - 1) * 100  # Ya en porcentaje
                resumen_rendimientos.append({
                    "Acción": seleccion["Nombre"],
                    "Rendimiento Promedio (%)": round(datos['Rendimiento'].mean(), 4),  # Redondeo a 2 decimales
                    "Rendimiento Máximo (%)": round(datos['Rendimiento'].max(), 4),
                    "Rendimiento Mínimo (%)": round(datos['Rendimiento'].min(), 4),
                })

                # Agregar rendimiento acumulado para la gráfica
                datos["Rendimiento Acumulado"] = (datos["Close"] / datos["Close"].iloc[0] - 1) * 100  # Ya en porcentaje
                plt.plot(datos.index, datos["Rendimiento Acumulado"], label=seleccion["Nombre"])

        # Configuración del eje de fechas para la gráfica
        if periodo in ["5y", "10y"]:
            plt.gca().xaxis.set_major_locator(mdates.YearLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        else:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

        plt.xlabel("Fecha")
        plt.ylabel("Rendimiento (%)")
        plt.title("Rendimiento de las Acciones Seleccionadas")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(plt)

        st.write("### Resumen de Rendimientos")
        st.table(pd.DataFrame(resumen_rendimientos))

        # Interpretación de rendimientos
        if st.button("Mostrar Interpretación de Rendimientos"):
            if resumen_rendimientos:
                mejor_rendimiento = max(resumen_rendimientos, key=lambda x: x["Rendimiento Promedio (%)"])
                menor_rendimiento = min(resumen_rendimientos, key=lambda x: x["Rendimiento Promedio (%)"])
                st.write(f"""
                **Interpretación de Rendimientos:**
                La acción con mayor rendimiento promedio es **{mejor_rendimiento['Acción']}** con un rendimiento promedio de **{mejor_rendimiento['Rendimiento Promedio (%)']:.2f}%**.
                Si tu prioridad es maximizar ganancias, esta sería una opción ideal.
                Por otro lado, la acción con menor rendimiento promedio es **{menor_rendimiento['Acción']}**, con un rendimiento promedio de **{menor_rendimiento['Rendimiento Promedio (%)']:.2f}%**.
                Esta podría ser una opción más conservadora si buscas menos exposición a riesgos altos.
                """)

        st.write("### Gráfica de Volatilidad")
        plt.figure(figsize=(10, 6))
        for seleccion in datos_seleccionados:
            simbolo = seleccion["Símbolo"]
            ticker = yf.Ticker(simbolo)
            datos = ticker.history(period=periodo)

            if not datos.empty:
                datos['Rendimiento'] = datos['Close'].pct_change() * 100  # Cálculo de rendimiento en porcentaje
                datos['Volatilidad'] = datos['Rendimiento'].rolling(window=21).std()

                resumen_volatilidad.append({
                    "Acción": seleccion["Nombre"],
                    "Volatilidad Promedio (%)": round(datos['Volatilidad'].mean(), 4),  # Redondeo a 2 decimales
                    "Volatilidad Máxima (%)": round(datos['Volatilidad'].max(), 4),
                    "Volatilidad Mínima (%)": round(datos['Volatilidad'].min(), 4),
                })

                # Agregar volatilidad para la gráfica
                plt.plot(datos.index, datos['Volatilidad'], label=seleccion["Nombre"])

        # Configuración del eje de fechas para la gráfica de volatilidad
        if periodo in ["5y", "10y"]:
            plt.gca().xaxis.set_major_locator(mdates.YearLocator())  # Dividir por años
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))  # Formato solo año
        else:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Dividir por meses
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))  # Formato mes y año
        
        plt.xlabel("Fecha")
        plt.ylabel("Volatilidad (%)")
        plt.title("Volatilidad de las Acciones Seleccionadas")
        plt.legend()
        plt.grid(True)
        
        plt.xticks(rotation=45)  # Girar las etiquetas para mejor legibilidad
        
        st.pyplot(plt)

        # Crear DataFrame para el resumen de volatilidad y mostrarlo
        volatility_df = pd.DataFrame(resumen_volatilidad)
        st.write("### Resumen de Volatilidad (Riesgo)")
        st.table(volatility_df)

        # Interpretación dinámica de volatilidad
        if st.button("Mostrar Interpretación de Volatilidad"):
            if resumen_volatilidad:
                mayor_volatilidad = max(resumen_volatilidad, key=lambda x: x["Volatilidad Promedio (%)"])
                menor_volatilidad = min(resumen_volatilidad, key=lambda x: x["Volatilidad Promedio (%)"])
                st.write(f"""
                **Interpretación de Volatilidad:**
                La acción más volátil es **{mayor_volatilidad['Acción']}** con una volatilidad promedio de **{mayor_volatilidad['Volatilidad Promedio (%)']:.2f}%**.
                Esto indica que sus precios tienden a fluctuar más, lo que podría representar mayores riesgos pero también mayores oportunidades.
                La acción menos volátil es **{menor_volatilidad['Acción']}**, con una volatilidad promedio de **{menor_volatilidad['Volatilidad Promedio (%)']:.2f}%**.
                Esta podría ser una opción para quienes buscan estabilidad en lugar de altas fluctuaciones.
                """)


        # Simulador de inversión
    # Simulador de inversión
        st.header("Simulador de Inversión")
        monto_total = st.number_input("Monto total a invertir", min_value=0.0, step=100.0)

        # Inicializamos los diccionarios para las asignaciones y el porcentaje total
        investment_percentages = {}
        total_allocated = 0.0

        # Suponiendo que 'datos_seleccionados' contiene la información de las acciones seleccionadas
        for seleccion in datos_seleccionados:
            simbolo = seleccion["Símbolo"]
            max_percentage = float(100.0 - total_allocated)
            percentage = st.slider(f"Asigna porcentaje para {seleccion['Nombre']} ({simbolo})", 
                                min_value=0.0, max_value=max_percentage, 
                                step=0.1, value=0.0, format="%.1f")
            investment_percentages[simbolo] = percentage
            total_allocated += percentage

        # Mostramos el total asignado
        st.write(f"Total asignado: {total_allocated:.2f}%")

        # Si el total asignado es exactamente 100%, procedemos con el cálculo de la inversión
        if total_allocated > 100:
            st.warning("La suma de los porcentajes no puede superar el 100%.")
        elif total_allocated < 100:
            st.warning("La suma de los porcentajes debe ser exactamente 100%.")
        else:
            # Número de años para la inversión
            years = st.number_input("Años de la inversión (1-60)", min_value=1, max_value=60)

            final_values = {}
            total_final_value = 0.0

            # Calcular el valor final para cada acción seleccionada
            for seleccion in datos_seleccionados:
                simbolo = seleccion["Símbolo"]
                porcentaje_asignado = investment_percentages[simbolo] / 100
                ticker = yf.Ticker(simbolo)
                datos = ticker.history(period="1y")  # Puedes ajustar el periodo aquí

                if not datos.empty:
                    # Calcular el rendimiento anualizado
                    rendimiento_anual = (datos["Close"].iloc[-1] / datos["Close"].iloc[0]) - 1
                    valor_invertido = monto_total * porcentaje_asignado
                    final_value = valor_invertido * ((1 + rendimiento_anual) ** years)  # Ajuste a lo largo de los años
                    final_values[simbolo] = final_value
                    total_final_value += final_value

            # Mostrar el valor final de la inversión para cada acción
            st.write("### Valores Finales de la Inversión por Acción")
            for simbolo, value in final_values.items():
                st.write(f"{simbolo}: ${value:,.2f}")

            # Mostrar el valor total final de la inversión
            st.write(f"### Valor Total Final de la Inversión: ${total_final_value:,.2f}")
