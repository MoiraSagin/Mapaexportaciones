import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import pycountry
import json

with open("colombia.geojson", "r", encoding="utf-8") as f:
    geo_colombia = json.load(f)

st.set_page_config(
    page_title="Mapa de Exportaciones Colombia (2025)",
    layout="wide"
)

st.title("Mapa de Exportaciones Colombia (2025)")
st.sidebar.header("Filtros")

# =========================
# CARGAR DATOS
# =========================

@st.cache_data
def cargar_datos():

    mundo_anual = pd.read_csv("mundo_resumen.csv")
    colombia_anual = pd.read_csv("colombia_resumen.csv")

    mundo_mensual = pd.read_csv("mundo_mensual.csv")
    colombia_mensual = pd.read_csv("colombia_mensual.csv")

    mundo_ciiu = pd.read_csv("mundo_ciiu.csv")
    colombia_ciiu = pd.read_csv("colombia_ciiu.csv")

    mundo_tecnologia = pd.read_csv("mundo_tecnologia.csv")
    colombia_tecnologia = pd.read_csv("colombia_tecnologia.csv")

    return (
        mundo_anual,
        colombia_anual,
        mundo_mensual,
        colombia_mensual,
        mundo_ciiu,
        colombia_ciiu,
        mundo_tecnologia,
        colombia_tecnologia
    )

(
    mundo_anual,
    colombia_anual,
    mundo_mensual,
    colombia_mensual,
    mundo_ciiu,
    colombia_ciiu,
    mundo_tecnologia,
    colombia_tecnologia
) = cargar_datos()


# =========================
# FUNCIONES
# =========================

def obtener_iso3(nombre):
    equivalencias = {
    "UNITED STATES": "USA",
    "RUSSIA": "RUS",
    "SOUTH KOREA": "KOR",
    "NORTH KOREA": "PRK",
    "UNITED KINGDOM": "GBR",
    "CZECH REPUBLIC": "CZE",
    "VIETNAM": "VNM",
    "IRAN": "IRN",
    "SYRIA": "SYR",
    "VENEZUELA": "VEN",
    "BOLIVIA": "BOL",
    "TANZANIA": "TZA",
    "MOLDOVA": "MDA",
    "PALESTINE": "PSE",

    # NUEVOS
    "ANTIGUA Y BARBUDA": "ATG",
    "BAHREIN": "BHR",
    "BRUNEI": "BRN",
    "COTE D'IVOIRE": "CIV",
    "JORDANIA": "JOR",
    "LIBIA": "LBY",
    "MACEDONIA": "MKD",
    "MALDIVAS": "MDV",
    "DEMOCRATIC REPUBLIC OF THE CONGO": "COD",
    "TADJIKISTAN": "TJK",
    "TANZANIA REP UNIDA DE": "TZA",
    "TURKEY": "TUR",

    "SUECIA": "SWE",
    "SUIZA": "CHE",
    "SURINAM": "SUR",
    "TAILANDIA": "THA",
    "TRINIDAD Y TOBAGO": "TTO",
    "TURQUIA": "TUR",
    "UCRANIA": "UKR",
    "ALEMANIA": "DEU",
    "ARABIA SAUDITA": "SAU",
    "ARGELIA": "DZA",
    "AUSTRALIA": "AUS",
    "AUSTRIA": "AUT",
    "BELGICA": "BEL",
    "BRASIL": "BRA",
    "CANADA": "CAN",
    "CHILE": "CHL",
    "CHINA": "CHN",
    "ECUADOR": "ECU",
    "ESPANA": "ESP",
    "ESTADOS UNIDOS": "USA",
    "FRANCIA": "FRA",
    "INDIA": "IND",
    "ITALIA": "ITA",
    "JAPON": "JPN",
    "MEXICO": "MEX",
    "PAISES BAJOS": "NLD",
    "PERU": "PER",
    "REINO UNIDO": "GBR",
    "REPUBLICA DOMINICANA": "DOM",
    "RUSIA": "RUS",
    "VENEZUELA": "VEN",
    "COREA DEL SUR": "KOR",
    "COREA DEL NORTE": "PRK",
    "TAIWAN": "TWN",
    "VIETNAM": "VNM",
    "IRAN": "IRN",
    "EGIPTO": "EGY",
    "DINAMARCA": "DNK",
    "ESLOVAQUIA": "SVK",
    "ESLOVENIA": "SVN",
    "CROACIA": "HRV",
    "BOSNIA Y HERZEGOVINA": "BIH",
    "CAMBOYA": "KHM",
    "BELICE": "BLZ",
    "CHIPRE": "CYP",
    "COSTA DE MARFIL": "CIV"
}
    nombre = str(nombre).strip().upper()

    if nombre in equivalencias:
        return equivalencias[nombre]

    try:
        return pycountry.countries.lookup(nombre).alpha_3
    except:
        return None
def limpiar_nombre(x):
    return (
        str(x)
        .upper()
        .replace("Á", "A")
        .replace("É", "E")
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("Ú", "U")
        .replace("Ü", "U")
        .replace("Ñ", "N")
        .strip()
    )

# =========================
# SELECTORES
# =========================

tipo_mapa = st.sidebar.selectbox(
    "Selecciona el mapa",
    ["Mapa mundial", "Mapa Colombia - Departamentos"]
)
periodo = st.sidebar.selectbox(
    "Selecciona periodo",
    ["Anual", "Mensual"]
)
meses = {
    "Enero": 1,
    "Febrero": 2,
    "Marzo": 3,
    "Abril": 4,
    "Mayo": 5,
    "Junio": 6,
    "Julio": 7,
    "Agosto": 8,
    "Septiembre": 9,
    "Octubre": 10,
    "Noviembre": 11,
    "Diciembre": 12
}

if periodo == "Mensual":

    mes_label = st.sidebar.selectbox(
        "Selecciona mes",
        list(meses.keys())
    )

    mes = meses[mes_label]

lista_ciiu = sorted(
    mundo_ciiu["CIIU"]
    .dropna()
    .astype(str)
    .unique()
)

lista_ciiu = ["Todos"] + lista_ciiu

ciiu_seleccionado = st.sidebar.selectbox(
    "Selecciona CIIU",
    lista_ciiu
)

lista_tecnologia = sorted(
    mundo_tecnologia["Nivel tecnologico"]
    .dropna()
    .astype(str)
    .unique()
)

lista_tecnologia = ["Todos"] + lista_tecnologia

tecnologia_seleccionada = st.sidebar.selectbox(
    "Selecciona nivel tecnológico",
    lista_tecnologia
)

top_n = st.sidebar.slider(
    "Cantidad de países/departamentos",
    min_value=5,
    max_value=50,
    value=10,
    step=5
)
if ciiu_seleccionado != "Todos" and tecnologia_seleccionada != "Todos":
    st.warning("Por ahora selecciona CIIU o nivel tecnológico, no ambos al mismo tiempo.")
    st.stop()
# =========================
# SELECCIONAR BASE
# =========================

if ciiu_seleccionado != "Todos":

    mundo = mundo_ciiu.copy()
    colombia = colombia_ciiu.copy()

    mundo = mundo[mundo["CIIU"] == ciiu_seleccionado]
    colombia = colombia[colombia["CIIU"] == ciiu_seleccionado]

    if periodo == "Anual":

        mundo = mundo.groupby(
            ["Pais", "Pais_join", "CIIU"],
            as_index=False
        ).agg({
            "fob_total": "sum",
            "kg_total": "sum"
        })

        colombia = colombia.groupby(
            ["Departamento", "Departamento_join", "CIIU"],
            as_index=False
        ).agg({
            "fob_total": "sum",
            "kg_total": "sum"
        })

elif tecnologia_seleccionada != "Todos":

    mundo = mundo_tecnologia.copy()
    colombia = colombia_tecnologia.copy()

    mundo = mundo[mundo["Nivel tecnologico"] == tecnologia_seleccionada]
    colombia = colombia[colombia["Nivel tecnologico"] == tecnologia_seleccionada]

    if periodo == "Anual":

        mundo = mundo.groupby(
            ["Pais", "Pais_join", "Nivel tecnologico"],
            as_index=False
        ).agg({
            "fob_total": "sum",
            "kg_total": "sum"
        })

        colombia = colombia.groupby(
            ["Departamento", "Departamento_join", "Nivel tecnologico"],
            as_index=False
        ).agg({
            "fob_total": "sum",
            "kg_total": "sum"
        })

else:

    if periodo == "Anual":

        mundo = mundo_anual.copy()
        colombia = colombia_anual.copy()

    else:

        mundo = mundo_mensual.copy()
        colombia = colombia_mensual.copy()

# =========================
# APLICAR FILTRO MENSUAL
# =========================

if periodo == "Mensual":

    mundo = mundo[mundo["Mes"] == mes]

    colombia_mes = colombia[colombia["Mes"] == mes]

    departamentos_base = colombia_anual[
        ["Departamento", "Departamento_join"]
    ].drop_duplicates()

    colombia = departamentos_base.merge(
        colombia_mes,
        on=["Departamento", "Departamento_join"],
        how="left"
    )

    colombia["fob_total"] = colombia["fob_total"].fillna(0)
    colombia["kg_total"] = colombia["kg_total"].fillna(0)

# =========================
# PREPARAR MUNDO
# =========================

mundo["iso3"] = mundo["Pais_join"].apply(obtener_iso3)

mundo = mundo.dropna(subset=["iso3"])

# =========================
# PREPARAR COLOMBIA
# =========================

colombia["Departamento_join"] = colombia["Departamento_join"].apply(limpiar_nombre)
colombia["Departamento_join"] = colombia["Departamento_join"].replace({
    "BOGOTA D.C.": "SANTAFE DE BOGOTA D.C",
    "BOGOTA": "SANTAFE DE BOGOTA D.C"
})
for feature in geo_colombia["features"]:
    nombre = feature["properties"].get("NOMBRE_DPT", "")
    feature["properties"]["Departamento_join"] = limpiar_nombre(nombre)
    if feature["properties"]["Departamento_join"] in ["SANTAFE DE BOGOTA D.C.", "BOGOTA D.C.", "BOGOTA"]:
        feature["properties"]["Departamento_join"] = "SANTAFE DE BOGOTA D.C"

# =========================
# MÉTRICAS
# =========================

col1, col2, col3 = st.columns(3)

if tipo_mapa == "Mapa mundial":

    total_fob = mundo["fob_total"].sum()
    total_paises = mundo["Pais"].nunique()
    promedio = total_fob / total_paises

    col1.metric(
        "Exportaciones totales FOB",
        f"${total_fob:,.0f}"
    )

    col2.metric(
        "Número de países con importaciones",
        total_paises
    )

    col3.metric(
        "Promedio por país",
        f"${promedio:,.0f}"
    )

else:

    total_fob = colombia["fob_total"].sum()
    total_deptos = colombia[colombia["fob_total"] > 0]["Departamento"].nunique()
    promedio = total_fob / total_deptos

    col1.metric(
        "Exportaciones totales FOB",
        f"${total_fob:,.0f}"
    )

    col2.metric(
        "Departamentos con exportaciones",
        total_deptos
    )

    col3.metric(
        "Promedio por departamento",
        f"${promedio:,.0f}"
    )
# =========================
# MAPA MUNDIAL
# =========================

if tipo_mapa == "Mapa mundial":

    opciones_mundo = {
        "FOB total": "fob_total",
        "KG netos total": "kg_total"
    }

    variable_label = st.sidebar.selectbox(
        "Selecciona variable",
        list(opciones_mundo.keys())
    )

    variable = opciones_mundo[variable_label]

    # Hover dinámico: solo usa columnas que existan
    hover_cols_mundo = {
        "fob_total": ":,.0f",
        "kg_total": ":,.0f"
    }

    if "CIIU" in mundo.columns:
        hover_cols_mundo["CIIU"] = True

    if "fob_ciiu" in mundo.columns:
        hover_cols_mundo["fob_ciiu"] = ":,.0f"
    mundo["valor_mapa"] = np.log1p(mundo[variable])

    custom_cols_mundo = [
    "fob_total",
    "kg_total"
]
    if "Nivel tecnologico" in mundo.columns:
        custom_cols_mundo.append("Nivel tecnologico")

    if "CIIU" in mundo.columns:
        custom_cols_mundo.append("CIIU")

    if "fob_ciiu" in mundo.columns:
        custom_cols_mundo.append("fob_ciiu")
    fig = px.choropleth(
        mundo,
        locations="iso3",
        color="valor_mapa",
        hover_name="Pais",
        custom_data=custom_cols_mundo,
        color_continuous_scale="Reds",
        projection="natural earth"
    )

    fig.update_layout(height=700)
    fig.update_coloraxes(
    colorbar_title=f"{variable_label}<br>(escala log)",

    colorbar=dict(
        tickvals=[10, 15, 20],
        ticktext=["1 mil", "1 millón", "100 millones"]
    )
)
    fig.update_coloraxes(
    colorbar_title="Intensidad exportadora"
)
    if "Nivel tecnologico" in mundo.columns:

        fig.update_traces(
        hovertemplate=
        "<b>%{hovertext}</b><br><br>" +
        "FOB total: $%{customdata[0]:,.0f}<br>" +
        "KG netos: %{customdata[1]:,.0f}<br>" +
        "Nivel tecnológico: %{customdata[2]}" +
        "<extra></extra>"
    )

    else:

        fig.update_traces(
        hovertemplate=
        "<b>%{hovertext}</b><br><br>" +
        "FOB total: $%{customdata[0]:,.0f}<br>" +
        "KG netos: %{customdata[1]:,.0f}<br>" +
        "CIIU principal: %{customdata[2]}<br>" +
        "FOB CIIU: $%{customdata[3]:,.0f}" +
        "<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"Top {top_n} países por FOB")

    top_paises = mundo.sort_values(
    "fob_total",
    ascending=False
).head(top_n)

    columnas_mundo = [
    "Pais",
    "fob_total",
    "kg_total",
    "CIIU",
    "fob_ciiu"
]

    columnas_mundo = [c for c in columnas_mundo if c in top_paises.columns]

    top_paises_mostrar = top_paises[columnas_mundo].rename(columns={
    "Pais": "País",
    "fob_total": "FOB total",
    "kg_total": "KG netos",
    "CIIU": "CIIU principal",
    "fob_ciiu": "FOB CIIU principal"
})

    st.dataframe(
    top_paises_mostrar,
    use_container_width=True,
    hide_index=True
)

# =========================
# MAPA COLOMBIA
# =========================

else:

    opciones_colombia = {
        "FOB total": "fob_total",
        "KG netos total": "kg_total"
    }

    variable_colombia_label = st.sidebar.selectbox(
        "Selecciona variable departamental",
        list(opciones_colombia.keys())
    )

    variable_colombia = opciones_colombia[variable_colombia_label]

    # Hover dinámico: solo usa columnas que existan
    hover_cols_colombia = {
        "fob_total": ":,.0f",
        "kg_total": ":,.0f"
    }

    if "Nivel tecnologico" in colombia.columns:
        hover_cols_colombia["Nivel tecnologico"] = True

    if "Pais" in colombia.columns:
        hover_cols_colombia["Pais"] = True

    if "CIIU" in colombia.columns:
        hover_cols_colombia["CIIU"] = True

    if "fob_ciiu" in colombia.columns:
        hover_cols_colombia["fob_ciiu"] = ":,.0f"
    colombia["valor_mapa"] = np.log1p(colombia[variable_colombia])

    custom_cols_colombia = [
    "fob_total",
    "kg_total"
]

    if "Nivel tecnologico" in colombia.columns:
        custom_cols_colombia.append("Nivel tecnologico")

    if "Pais" in colombia.columns:
        custom_cols_colombia.append("Pais")

    if "CIIU" in colombia.columns:
        custom_cols_colombia.append("CIIU")

    if "fob_ciiu" in colombia.columns:
        custom_cols_colombia.append("fob_ciiu")
    fig = px.choropleth(
        colombia,
        geojson=geo_colombia,
        locations="Departamento_join",
        featureidkey="properties.Departamento_join",
        color="valor_mapa",
        hover_name="Departamento",
        custom_data=custom_cols_colombia,
        color_continuous_scale="Reds"
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig.update_layout(height=700)
    fig.update_coloraxes(
    colorbar_title=f"{variable_colombia_label}<br>(escala log)",

    colorbar=dict(
        tickvals=[10, 15, 20],
        ticktext=["1 mil", "1 millón", "100 millones"]
    )
)
    if "Pais" in colombia.columns and "CIIU" in colombia.columns and "fob_ciiu" in colombia.columns:

        fig.update_traces(
        hovertemplate=
        "<b>%{hovertext}</b><br><br>" +
        "FOB total: $%{customdata[0]:,.0f}<br>" +
        "KG netos: %{customdata[1]:,.0f}<br>" +
        "Nivel tecnológico: %{customdata[2]}<br>" +
        "País destino principal: %{customdata[3]}<br>" +
        "CIIU principal: %{customdata[4]}<br>" +
        "FOB CIIU: $%{customdata[5]:,.0f}" +
        "<extra></extra>"
    )

    elif "Nivel tecnologico" in colombia.columns:

        fig.update_traces(
        hovertemplate=
        "<b>%{hovertext}</b><br><br>" +
        "FOB total: $%{customdata[0]:,.0f}<br>" +
        "KG netos: %{customdata[1]:,.0f}<br>" +
        "Nivel tecnológico: %{customdata[2]}" +
        "<extra></extra>"
    )

    elif "CIIU" in colombia.columns:

        fig.update_traces(
        hovertemplate=
        "<b>%{hovertext}</b><br><br>" +
        "FOB total: $%{customdata[0]:,.0f}<br>" +
        "KG netos: %{customdata[1]:,.0f}<br>" +
        "CIIU: %{customdata[2]}" +
        "<extra></extra>"
    )

    else:

        fig.update_traces(
        hovertemplate=
        "<b>%{hovertext}</b><br><br>" +
        "FOB total: $%{customdata[0]:,.0f}<br>" +
        "KG netos: %{customdata[1]:,.0f}" +
        "<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"Top {top_n} departamentos por FOB")

    top_col = colombia.sort_values(
    "fob_total",
    ascending=False
).head(top_n)

    columnas_colombia = [
    "Departamento",
    "fob_total",
    "kg_total",
    "Nivel tecnologico",
    "Pais",
    "CIIU",
    "fob_ciiu"
]

    columnas_colombia = [c for c in columnas_colombia if c in top_col.columns]

    top_col_mostrar = top_col[columnas_colombia].rename(columns={
    "fob_total": "FOB total",
    "kg_total": "KG netos",
    "Nivel tecnologico": "Nivel tecnológico",
    "Pais": "País destino principal",
    "CIIU": "CIIU principal",
    "fob_ciiu": "FOB CIIU principal"
})

    st.dataframe(
    top_col_mostrar,
    use_container_width=True,
    hide_index=True
)