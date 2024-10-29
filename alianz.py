import streamlit as st
import yfinance as yf
import pandas as pd
import pyarrow as pa
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np



st.title("Simulador de Rendimientos Allianz Optimax")

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
# Lista de nombres de los ETF para desplegar
etf_names = [etf["name"] for etf in etf_data]

# Crear una lista desplegable
selected_etf_name = st.selectbox("Selecciona un ETF", etf_names)

# Encontrar el ETF seleccionado en los datos y mostrar los detalles
selected_etf = next((etf for etf in etf_data if etf["name"] == selected_etf_name), None)

if selected_etf:
    st.write("### Detalles del ETF seleccionado")
    st.write(f"**Nombre**: {selected_etf['name']}")
    st.write(f"**Símbolo**: {selected_etf['symbol']}")
    st.write(f"**Descripción**: {selected_etf['description']}")

# Opción para seleccionar el período de tiempo
    st.write("### Selecciona el período de tiempo para los datos")
    periods = {
    "1 mes": "1mo",
    "3 meses": "3mo",
    "6 meses": "6mo",
    "1 año": "1y",
    "YTD": "ytd",
    "5 años": "5y",
    "10 años": "10y"
    }
    
    # Cambiado a selectbox para seleccionar un único período
selected_period = st.selectbox("Selecciona el período:", list(periods.keys()))

if selected_period:
        period_code = periods[selected_period]
        st.write(f"#### Rendimientos     históricos para el período: {selected_period}")
        data = yf.download(selected_etf["symbol"], period=period_code)

        if data.empty:
            st.write("No se encontraron datos para el período seleccionado.")
        else:
            monthly_data = data.resample('M').last()
            monthly_data['Rendimiento'] = monthly_data['Close'].pct_change() * 100  # Multiplicar por 100 para porcentajes
        

            ###############################GRÁFICA RTOS MENSUALES



        # Inicializar el estado de visibilidad de la gráfica de rendimientos mensuales
if "show_returns_graph" not in st.session_state:
    st.session_state.show_returns_graph = False

# Botón para alternar la visibilidad de la gráfica de rendimientos mensuales
if st.button("Mostrar/Ocultar Gráfica de Rendimientos Mensuales"):
    st.session_state.show_returns_graph = not st.session_state.show_returns_graph  # Cambiar el estado

# Mostrar la gráfica solo si el estado es True
if st.session_state.show_returns_graph:
    # Datos de ejemplo (reemplázalos con tus datos reales)
    # monthly_data = obtener_datos_etf(selected_etf['symbol'], "1y") # Ejemplo de llamada a función

    # Crear gráfica de rendimientos mensuales usando Matplotlib
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly_data.index, monthly_data['Rendimiento'], marker='o', linestyle='-', color='royalblue', markersize=8)

    # Mejorar estética de la gráfica
    ax.set_title("Rendimientos Mensuales", fontsize=16, fontweight='bold', color='darkslategray')
    ax.set_xlabel("Fecha", fontsize=12, fontweight='bold', color='dimgray')
    ax.set_ylabel("Rendimiento (%)", fontsize=12, fontweight='bold', color='dimgray')

    ax.set_facecolor('lightgray')  # Cambiar color de fondo
    ax.grid(color='white', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45)

    # Formatear el eje Y como porcentaje
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    plt.tight_layout()  # Ajustar para evitar recortes en los bordes
    st.pyplot(fig)
            ##### GRÁFICA RTOS MENSUALES

###################################RENTABILIDAD SIMPLE
# Obtener fechas de inicio y fin en el conjunto de datos
fecha_inicio = data.index[0].strftime("%B %Y")
fecha_fin = data.index[-1].strftime("%B %Y")
if selected_period:
    period_code = periods[selected_period]
    #st.write(f"#### Precios históricos para el periodo: {fecha_inicio} - {fecha_fin}")
    data = yf.download(selected_etf["symbol"], period=period_code)



    if data.empty or 'Close' not in data.columns:
        st.write("No hay datos disponibles para este ETF en el período seleccionado.")
    else:
        # Mostrar la gráfica de precios
        #st.line_chart(data['Close'])

        
    
        # Acceder a los precios inicial y final
        if len(data['Close']) >= 1:  # Asegurarse de que hay al menos un precio
            precio_inicial = data['Close'].iloc[0].item()  # Primer valor de cierre como escalar
            precio_final = data['Close'].iloc[-1].item()    # Último valor de cierre como escalar
            st.write(f"#### Datos financieros para el periodo: {fecha_inicio} - {fecha_fin}")
            # Mostrar precios en pantalla
            st.write(f"**Precio inicial: ${precio_inicial:.2f}**")
            st.write(f"**Precio final: ${precio_final:.2f}**")
            
            # Calcular y mostrar el crecimiento
            crecimiento = ((precio_final - precio_inicial) / precio_inicial) * 100
            st.write(f"**Crecimiento en el período seleccionado: {crecimiento:.2f}%**")
        else:
            st.write("No hay suficientes datos para mostrar precios.")
        #######################RENTABILIDAD SIMPLE
 ############################RENTABILIDAD GEOMETRICA
        # Inicializa las variables
rentabilidad_geom = 0.0
volatilidad = 0.0

# Calcular y mostrar rentabilidad geométrica y volatilidad en función del periodo
if selected_period in ["3 meses", "6 meses", "1 año", "YTD"]:
    if selected_period == "1 mes":
        # Calcular rendimientos diarios
        retornos = data['Close'].pct_change().dropna() + 1
    else:
        # Resamplear a fin de mes para calcular rendimientos mensuales
        data_mensual = data['Close'].resample('M').last()
        retornos = data_mensual.pct_change().dropna() + 1
    
    rentabilidad_geom = np.prod(retornos) ** (1 / len(retornos)) - 1
    volatilidad = retornos.std() * np.sqrt(12)  # Anualización

elif selected_period in ["3 años", "5 años", "10 años"]:
    # Resamplear a fin de año para calcular rendimientos anuales
    data_anual = data['Close'].resample('Y').last()
    retornos = data_anual.pct_change().dropna() + 1
    rentabilidad_geom = np.prod(retornos) ** (1 / len(retornos)) - 1
    volatilidad = data_anual.pct_change().dropna().std()  # Ya en términos anuales

# Convertir rentabilidad geométrica y volatilidad a flotante
rentabilidad_geom = float(rentabilidad_geom)
volatilidad = float(volatilidad)

# Mostrar rentabilidad geométrica y volatilidad en pantalla
st.write(f"**Rentabilidad geométrica ({selected_period}): {rentabilidad_geom * 100:.2f}%**")
st.write(f"**Volatilidad ({selected_period}): {volatilidad * 100:.2f}%**")

# Información general (la parte de información general no cambia)
stock_info = yf.Ticker(selected_etf["symbol"]).info


# Mostrar solo si el valor está disponible
if stock_info.get("longName", "N/A") != "N/A":
    st.write(f"**Nombre**: {stock_info['longName']}")
    
if stock_info.get("sector", "N/A") != "N/A":
    st.write(f"**Sector**: {stock_info['sector']}")
    
if stock_info.get("marketCap", "N/A") != "N/A":
    st.write(f"**Capitalización de mercado**: {stock_info['marketCap']}")

if stock_info.get("fiftyTwoWeekHigh", "N/A") != "N/A":
    st.write(f"**Máximo de 52 semanas**: {stock_info['fiftyTwoWeekHigh']}")

if stock_info.get("fiftyTwoWeekLow", "N/A") != "N/A":
    st.write(f"**Mínimo de 52 semanas**: {stock_info['fiftyTwoWeekLow']}")

if stock_info.get("trailingPE", "N/A") != "N/A":
    st.write(f"**P/E Ratio (Trailing)**: {stock_info['trailingPE']}")

if stock_info.get("forwardPE", "N/A") != "N/A":
    st.write(f"**P/E Ratio (Forward)**: {stock_info['forwardPE']}")

if stock_info.get("fiveYearAvgDividendYield", "N/A") != "N/A":
    st.write(f"**Tasa de crecimiento de dividendos a 5 años**: {stock_info['fiveYearAvgDividendYield']}")


        # Cargar y procesar los datos históricos
data = yf.download(selected_etf["symbol"], period=period_code)
if not data.empty:
    
    import streamlit as st
import matplotlib.pyplot as plt

# Inicializar el estado de visibilidad de la gráfica
if "show_graph" not in st.session_state:
    st.session_state.show_graph = False

# Botón para alternar la visibilidad de la gráfica
if st.button("Mostrar/Ocultar Gráfica de Precios Mensuales"):
    st.session_state.show_graph = not st.session_state.show_graph  # Cambiar el estado

# Mostrar la gráfica solo si el estado es True
if st.session_state.show_graph:
    # Datos de ejemplo (reemplázalos con tus datos reales)
    # monthly_data = obtener_datos_etf(selected_etf['symbol'], "1y") # Ejemplo de llamada a función

    # Graficar precios mensuales en dólares
    fig_price, ax_price = plt.subplots(figsize=(10, 5))
    ax_price.plot(monthly_data.index, monthly_data['Close'], marker='o', linestyle='-', color='green', markersize=8)

    # Mejorar estética de la gráfica
    ax_price.set_title("Precios Mensuales del ETF (USD)", fontsize=16, fontweight='bold', color='darkslategray')
    ax_price.set_xlabel("Fecha", fontsize=12, fontweight='bold', color='dimgray')
    ax_price.set_ylabel("Precio (USD)", fontsize=12, fontweight='bold', color='dimgray')

    ax_price.set_facecolor('lightgray')  # Cambiar color de fondo
    ax_price.grid(color='white', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45)

    # Ajustar para evitar recortes en los bordes
    plt.tight_layout()
    st.pyplot(fig_price)


    # Crear un DataFrame resampleado por mes y calcular el rendimiento mensual
    monthly_data = data.resample('M').last()
    monthly_data['Rendimiento'] = monthly_data['Close'].pct_change() * 100

    # Calcular el rendimiento promedio
    rendimiento_promedio = monthly_data['Rendimiento'].mean()
        

    

    



# Apartado para ingresar monto inicial
st.write("### Simulador de Inversión")
monto_inicial = st.number_input("Ingresa el monto inicial (en pesos):", min_value=0.0, format="%.2f")

# Inicializar variables de valor final
valor_final_simple = 0.0
valor_final_geom = 0.0

# Cálculos cuando se selecciona un período y hay un monto inicial
if selected_period and monto_inicial > 0:
    # Verifica que las variables estén definidas
    if 'crecimiento' in locals() and 'rentabilidad_geom' in locals():
        # Calcular rendimientos simples y geométricos
        rendimiento_simple = crecimiento / 100  # Convertir a decimal
        valor_final_simple = monto_inicial * (1 + rendimiento_simple)

        # Usar rentabilidad geométrica
        if selected_period in ["1 mes", "3 meses", "6 meses", "1 año", "YTD"]:
            valor_final_geom = monto_inicial * (1 + rentabilidad_geom)
        elif selected_period in ["5 años", "10 años"]:
            valor_final_geom = monto_inicial * (1 + rentabilidad_geom) ** (5 if selected_period == "5 años" else 10)

        # Mostrar resultados
        st.write(f"**Valor final con rendimiento simple tras {selected_period}: ${valor_final_simple:.2f}**")
        st.write(f"**Valor final con rentabilidad geométrica tras {selected_period}: ${valor_final_geom:.2f}**")
    else:
        st.write("Por favor, asegúrate de que los rendimientos simples y geométricos están calculados.")
else:
    st.write("Por favor, selecciona un período y un monto inicial mayor a cero para realizar la simulación.")


# Crear listas para almacenar los datos de rendimiento y volatilidad
etf_performance = []
etf_volatility = []

# Calcular rendimiento y volatilidad
for etf in etf_data:
    ticker = yf.Ticker(etf["symbol"])
    data = ticker.history(period="1y")
    
    if not data.empty:
        # Calcular rendimiento anualizado
        start_price = data["Close"].iloc[0]
        end_price = data["Close"].iloc[-1]
        annual_return = ((end_price / start_price) - 1) * 100
        etf_performance.append({"name": etf["name"], "symbol": etf["symbol"], "annual_return": annual_return})

        # Calcular volatilidad
        daily_returns = data['Close'].pct_change().dropna()
        volatility = daily_returns.std() * 252
        etf_volatility.append({"name": etf["name"], "symbol": etf["symbol"], "volatility": volatility})

# Crear DataFrames
etf_performance_df = pd.DataFrame(etf_performance).sort_values(by="annual_return", ascending=False).reset_index(drop=True)
etf_volatility_df = pd.DataFrame(etf_volatility).sort_values(by="volatility", ascending=False).reset_index(drop=True)

# Crear dos columnas en Streamlit
col1, col2 = st.columns(2)

# Mostrar la tabla de rendimiento en la primera columna
with col1:
    st.write("### Rendimiento anualizado de los ETFs (ordenado de mayor a menor)")
    st.dataframe(etf_performance_df)

# Mostrar la tabla de volatilidad en la segunda columna
with col2:
    st.write("### Volatilidad de los ETFs (ordenado de mayor a menor)")
    st.dataframe(etf_volatility_df)
