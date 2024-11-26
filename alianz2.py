import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def ejecutar_etfs():
    # Datos de los ETFs
    etf_data = [
        {"name": "AZ China", "symbol": "FXI", "description": "iShares China Large-Cap ETF que sigue a empresas chinas de gran capitalización."},
        {"name": "AZ MSCI Taiwan Index Fund", "symbol": "EWT", "description": "ETF que rastrea empresas de Taiwán incluidas en el índice MSCI Taiwan."},
        {"name": "AZ Russell 2000", "symbol": "IWM", "description": "ETF que sigue el índice Russell 2000 de empresas pequeñas de EE.UU."},
        {"name": "AZ Brasil", "symbol": "EWZ", "description": "iShares MSCI Brazil ETF que sigue el rendimiento de grandes y medianas empresas en Brasil."},
        {"name": "AZ MSCI United Kingdom", "symbol": "EWU", "description": "ETF que sigue el índice MSCI United Kingdom con exposición al mercado del Reino Unido."},
        {"name": "AZ DJ US Financial Sector", "symbol": "IYF", "description": "iShares U.S. Financials ETF que sigue el sector financiero de EE.UU."},
        {"name": "AZ BRIC", "symbol": "BKF", "description": "ETF que sigue el índice BRIC, que incluye Brasil, Rusia, India y China."},
        {"name": "AZ MSCI South Korea Index", "symbol": "EWY", "description": "ETF que rastrea el índice MSCI South Korea, con empresas surcoreanas."},
        {"name": "AZ Barclays Aggregate", "symbol": "AGG", "description": "iShares Core U.S. Aggregate Bond ETF que sigue el mercado de bonos de EE.UU."},
        {"name": "AZ Mercados Emergentes", "symbol": "EEM", "description": "iShares MSCI Emerging Markets ETF que sigue mercados emergentes globales."},
        {"name": "AZ MSCI EMU", "symbol": "EZU", "description": "ETF que sigue el índice MSCI EMU de empresas de la eurozona."},
        {"name": "AZ FTSE/Xinhua China 25", "symbol": "FXI", "description": "ETF que sigue las 25 principales empresas de China."},
        {"name": "AZ Oro", "symbol": "GLD", "description": "SPDR Gold Shares ETF que sigue el precio del oro."},
        {"name": "AZ Latixx Mex Cetetrac", "symbol": "N/A", "description": "ETF mexicano que sigue la evolución de cetes en México."},
        {"name": "AZ QQQ Nasdaq 100", "symbol": "QQQ", "description": "ETF que sigue el índice Nasdaq 100 de empresas tecnológicas de gran capitalización."},
        {"name": "AZ MSCI Asia ex-Japan", "symbol": "AAXJ", "description": "ETF que sigue el índice MSCI Asia ex-Japan, excluyendo empresas japonesas."},
        {"name": "AZ Latixx Mex M10trac", "symbol": "N/A", "description": "ETF que sigue el rendimiento de bonos de mediano plazo en México."},
        {"name": "AZ Barclays 1-3 Year TR", "symbol": "SHY", "description": "ETF de bonos del Tesoro a corto plazo (1-3 años) en EE.UU."},
        {"name": "AZ MSCI ACWI Index Fund", "symbol": "ACWI", "description": "ETF que sigue el índice MSCI ACWI, incluyendo empresas globales."},
        {"name": "AZ Latixx Mexico M5trac", "symbol": "N/A", "description": "ETF que sigue bonos de corto plazo en el mercado mexicano."},
        {"name": "AZ Silver Trust", "symbol": "SLV", "description": "iShares Silver Trust que sigue el precio de la plata."},
        {"name": "AZ MSCI Hong Kong Index", "symbol": "EWH", "description": "ETF que rastrea el índice MSCI Hong Kong, con empresas de Hong Kong."},
        {"name": "AZ Latixx Mex Uditrac", "symbol": "N/A", "description": "ETF que sigue el rendimiento de bonos a largo plazo en México ajustados por inflación."},
        {"name": "AZ SPDR S&P 500 ETF Trust", "symbol": "SPY", "description": "ETF que sigue el índice S&P 500 de empresas de gran capitalización en EE.UU."},
        {"name": "AZ MSCI Japan Index Fund", "symbol": "EWJ", "description": "ETF que sigue el índice MSCI Japan, con empresas japonesas."},
        {"name": "AZ BG EUR Govt Bond 1-3", "symbol": "BIL", "description": "ETF que sigue bonos del gobierno europeo a corto plazo (1-3 años)."},
        {"name": "AZ SPDR DJIA Trust", "symbol": "DIA", "description": "ETF que sigue el índice Dow Jones Industrial Average."},
        {"name": "AZ MSCI France Index Fund", "symbol": "EWQ", "description": "ETF que sigue el índice MSCI France, con empresas francesas."},
        {"name": "AZ DJ US Oil & Gas Expl", "symbol": "IEO", "description": "ETF que sigue el sector de exploración y producción de petróleo y gas en EE.UU."},
        {"name": "AZ Vanguard Emerging Market ETF", "symbol": "VWO", "description": "ETF de Vanguard que sigue los mercados emergentes."},
        {"name": "AZ MSCI Australia Index", "symbol": "EWA", "description": "ETF que sigue el índice MSCI Australia, con empresas australianas."},
        {"name": "AZ IPC Large Cap T R TR", "symbol": "N/A", "description": "ETF que sigue el índice IPC Large Cap de México."},
        {"name": "AZ Financial Select Sector SPDR", "symbol": "XLF", "description": "ETF que sigue el sector financiero de EE.UU."},
        {"name": "AZ MSCI Canada", "symbol": "EWC", "description": "ETF que sigue el índice MSCI Canada, con empresas canadienses."},
        {"name": "AZ S&P Latin America 40", "symbol": "ILF", "description": "ETF que sigue el índice S&P Latin America 40 de grandes empresas latinoamericanas."},
        {"name": "AZ Health Care Select Sector", "symbol": "XLV", "description": "ETF que sigue el sector de salud en EE.UU."},
        {"name": "AZ MSCI Germany Index", "symbol": "EWG", "description": "ETF que sigue el índice MSCI Germany, con empresas alemanas."},
        {"name": "AZ DJ US Home Construct", "symbol": "ITB", "description": "ETF que sigue el sector de construcción de viviendas en EE.UU."}
    ]

    # Página principal de la aplicación
    st.sidebar.title("Selecciona los ETFs")
    selected_etfs = st.sidebar.multiselect("Selecciona uno o más ETFs", [etf['name'] for etf in etf_data])

    period_options = ["5d", "1mo", "3mo", "6mo", "1y", "ytd", "3y", "5y", "10y"]
    selected_period = st.sidebar.selectbox("Selecciona el período de análisis", period_options)

    st.title("Información de los ETFs seleccionados")
    if selected_etfs:
        selected_data = [{"Nombre": etf['name'], "Símbolo": etf['symbol'], "Descripción": etf['description']}
                         for etf in etf_data if etf['name'] in selected_etfs]
        
        etf_df = pd.DataFrame(selected_data)
        st.table(etf_df)

        # Apartado de rendimiento
        st.write("### Gráfica de Rendimiento")
        plt.figure(figsize=(10, 6))
        
        summary_data = []  # Lista para almacenar los resúmenes

        for etf in etf_data:
            if etf['name'] in selected_etfs and etf['symbol'] != "N/A":
                ticker = yf.Ticker(etf['symbol'])
                
                # Obtener rango de fechas para los últimos 3 años si es el periodo seleccionado
                if selected_period == "3y":
                    end_date = dt.datetime.today()
                    start_date = end_date - dt.timedelta(days=3*365)  # Hace 3 años desde hoy
                    data = ticker.history(start=start_date, end=end_date)
                else:
                    data = ticker.history(period=selected_period)

                # Verificar si hay datos antes de graficar
                if not data.empty:
                    data['Rendimiento'] = (data['Close'] / data['Close'].iloc[0] - 1) * 100
                    plt.plot(data.index, data['Rendimiento'], label=etf['name'])

                    # Calcular rendimientos para la tabla resumen
                    rendimiento_promedio = data['Rendimiento'].mean()
                    rendimiento_anual = (data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100
                    rendimiento_maximo = data['Rendimiento'].max()
                    rendimiento_minimo = data['Rendimiento'].min()

                    # Agregar los resultados a la lista
                    summary_data.append({
                        "Acción": etf['name'],
                        "Rendimiento Promedio (%)": rendimiento_promedio,
                        "Rendimiento Anual (%)": rendimiento_anual,
                        "Rendimiento Máximo (%)": rendimiento_maximo,
                        "Rendimiento Mínimo (%)": rendimiento_minimo,
                    })

        # Mostrar la gráfica de rendimiento
        if selected_period in ["5y", "10y"]:
            plt.gca().xaxis.set_major_locator(mdates.YearLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        else:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        
        plt.xlabel("Fecha")
        plt.ylabel("Rendimiento (%)")
        plt.title("Rendimiento de los ETFs seleccionados")
        plt.legend()
        plt.grid(True)
        
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # Resumen de los rendimientos
        summary_df = pd.DataFrame(summary_data)
        st.write("### Resumen de Rendimientos")
        st.table(summary_df)

        # Interpretación de rendimientos
        if summary_data:
            if st.button("Mostrar Interpretación de Rendimientos"):
                mejor_rendimiento = max(summary_data, key=lambda x: x["Rendimiento Anual (%)"])
                menor_rendimiento = min(summary_data, key=lambda x: x["Rendimiento Anual (%)"])
                st.write(f"""
                **Interpretación de Rendimientos:**
                El ETF con mayor rendimiento anual es **{mejor_rendimiento['Acción']}** con un rendimiento anual de **{mejor_rendimiento['Rendimiento Anual (%)']:.2f}%**.
                Si buscas maximizar tus ganancias, este ETF podría ser una opción atractiva.
                Por otro lado, el ETF con menor rendimiento anual es **{menor_rendimiento['Acción']}** con un rendimiento anual de **{menor_rendimiento['Rendimiento Anual (%)']:.2f}%**.
                Este ETF podría ofrecer mayor estabilidad si prefieres un enfoque más conservador.
                """)

        # Apartado de volatilidad
        st.write("### Gráfica de Volatilidad (Periodo mínimo: 1 mes)")
        plt.figure(figsize=(10, 6))
        
        volatility_data = []  # Lista para almacenar los datos de volatilidad

        for etf in etf_data:
            if etf['name'] in selected_etfs and etf['symbol'] != "N/A":
                ticker = yf.Ticker(etf['symbol'])
                
                # Obtener rango de fechas para los últimos 3 años si es el periodo seleccionado
                if selected_period == "3y":
                    end_date = dt.datetime.today()
                    start_date = end_date - dt.timedelta(days=3*365)  # Hace 3 años desde hoy
                    data = ticker.history(start=start_date, end=end_date)
                else:
                    data = ticker.history(period=selected_period)

                # Verificar si hay datos antes de graficar
                if not data.empty:
                    data['Rendimiento'] = data['Close'].pct_change() * 100
                    data['Volatilidad'] = data['Rendimiento'].rolling(window=21).std()  # Desviación estándar mensual
                    plt.plot(data.index, data['Volatilidad'], label=etf['name'])

                    # Calcular volatilidad para la tabla resumen
                    volatilidad_promedio = data['Volatilidad'].mean()
                    volatilidad_maxima = data['Volatilidad'].max()
                    volatilidad_minima = data['Volatilidad'].min()

                    # Agregar los resultados a la lista
                    volatility_data.append({
                        "Acción": etf['name'],
                        "Volatilidad Promedio (%)": volatilidad_promedio,
                        "Volatilidad Máxima (%)": volatilidad_maxima,
                        "Volatilidad Mínima (%)": volatilidad_minima,
                    })

        # Mostrar la gráfica de volatilidad
        # Configuración del eje de fechas
        if selected_period in ["5y", "10y"]:
            plt.gca().xaxis.set_major_locator(mdates.YearLocator())  # Dividir por años
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y"))  # Formato solo año
        else:
            plt.gca().xaxis.set_major_locator(mdates.MonthLocator())  # Dividir por meses
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))  # Formato mes y año
        
        plt.xlabel("Fecha")
        plt.ylabel("Volatilidad (%)")
        plt.title("Volatilidad de los ETFs seleccionados")
        plt.legend()
        plt.grid(True)
        
        plt.xticks(rotation=45)  # Girar las etiquetas para mejor legibilidad
        
        st.pyplot(plt)

        # Crear DataFrame para el resumen de volatilidad y mostrarlo
        volatility_df = pd.DataFrame(volatility_data)
        st.write("### Resumen de Volatilidad (Riesgo)")
        st.table(volatility_df)

        # Interpretación dinámica de volatilidad
        if volatility_data:
            if st.button("Mostrar Interpretación de Volatilidad"):
                mayor_volatilidad = max(volatility_data, key=lambda x: x["Volatilidad Promedio (%)"])
                menor_volatilidad = min(volatility_data, key=lambda x: x["Volatilidad Promedio (%)"])
                st.write(f"""
                **Interpretación de Volatilidad:**
                El ETF más volátil es **{mayor_volatilidad['Acción']}** con una volatilidad promedio de **{mayor_volatilidad['Volatilidad Promedio (%)']:.2f}%**.
                Esto indica que sus precios fluctúan más, lo que puede representar mayores riesgos pero también mayores oportunidades de rendimiento.
                El ETF menos volátil es **{menor_volatilidad['Acción']}** con una volatilidad promedio de **{menor_volatilidad['Volatilidad Promedio (%)']:.2f}%**.
                Este ETF podría ser más adecuado si buscas una inversión más estable y con menor riesgo.
                """)

        # Simulador de inversión
        st.header("Simulador de inversión")
        investment_amount = st.number_input("Ingrese monto de la inversión", min_value=0.0, step=100.0)

        investment_percentages = {}
        total_allocated = 0.0

        # Mostrar opciones para cada ETF seleccionado
        for index, etf in enumerate(selected_data):
            symbol = etf['Símbolo']
            max_percentage = float(100.0 - total_allocated)
            percentage = st.slider(f"Porcentaje de la inversión para {etf['Nombre']} ({symbol})",
                                  min_value=0.0, max_value=max_percentage,
                                  step=0.1, value=0.0, format="%.1f")
            investment_percentages[symbol] = percentage
            total_allocated += percentage

        st.write(f"Total asignado: {total_allocated:.2f}%")

        if total_allocated > 100:
            st.warning("La suma de los porcentajes no puede superar el 100%.")
        elif total_allocated < 100:
            st.warning("La suma de los porcentajes debe ser exactamente 100%.")
        else:
            years = st.number_input("Años de la inversión (1-60)", min_value=1, max_value=60)

            final_values = {}
            total_final_value = 0.0

            for etf in selected_data:
                symbol = etf['Símbolo']
                rendimiento_anualizado = None
                for summary in summary_data:
                    if summary["Acción"] == etf['Nombre']:
                        rendimiento_anualizado = summary["Rendimiento Anual (%)"]
                        break

                if rendimiento_anualizado is not None:
                    allocated_amount = (investment_amount * investment_percentages[symbol]) / 100
                    final_value = allocated_amount * ((1 + rendimiento_anualizado / 100) ** years)
                    final_values[symbol] = final_value
                    total_final_value += final_value

            st.write("### Valores Finales de la Inversión por ETF")
            for symbol, value in final_values.items():
                st.write(f"{symbol}: ${value:,.2f}")
            
            st.write(f"### Valor Total Final de la Inversión: ${total_final_value:,.2f}")
