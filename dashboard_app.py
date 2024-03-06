from datetime import date

import altair as alt
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from src.data import load_daily_data_chamados, load_last_seven_days_data_chamados
from src.plot import bar_plot

PROJ_ID = st.secrets["ENV"]["project_id"]

## SET CONFIGS
st.set_page_config(page_title=PROJ_ID, layout=st.secrets["APP"]["layout"])

## SET TITLE
st.title(st.secrets["APP"]["page_title"])

## LOAD DATA
@st.cache_data
def load_dataframes(ref_date: date):
    last_seven_days_df = load_last_seven_days_data_chamados(
        project_id=PROJ_ID, ref_date=ref_date
    )
    daily_chamados_df = load_daily_data_chamados(project_id=PROJ_ID, ref_date=ref_date)
    return last_seven_days_df, daily_chamados_df


## Define callback
def save_date():
    st.session_state.ref_date = st.session_state.date_input


## SET DATE
with st.container():
    st.subheader("Selecione uma data para gerar os dados")
    ref_date = st.date_input(
        label="data de referência:",
        value="today",
        key="date_input",
        min_value=date(2022, 1, 1),
        format="DD.MM.YYYY",
        on_change=save_date,
    )

if "ref_date" not in st.session_state.keys():
    st.status("Esperando definir data ... ")

else:
    ref_date = st.session_state.ref_date
    with st.status(
        f"Carregando dados para {ref_date.day}/{ref_date.month}/{ref_date.year}"
    ):
        last_seven_days_df, daily_chamados_df = load_dataframes(ref_date=ref_date)
    with st.container():
        col1, col2 = st.columns([0.3, 0.7], gap="large")
        col1.subheader(
            f"Quantidade total de chamados em {ref_date.day}/{ref_date.month}/{ref_date.year}"
        )
        calculate_change = (
            last_seven_days_df.loc[0]["qtd_chamados"]
            / last_seven_days_df.loc[1]["qtd_chamados"]
        ) - 1.0
        col1.metric(
            label="Total",
            value=daily_chamados_df.shape[0],
            delta=np.round(calculate_change * 100.0, 2),
        )

        col2.subheader("Quantidade de chamados dos últimos 7 dias")
        bar_qtd_chamados = bar_plot(
            dataframe=last_seven_days_df,
            x="data_inicio:T",
            y="qtd_chamados:Q",
            mark_bar_kw={"color": "blue"},
        )
        line_qtd_chamados = (
            alt.Chart(last_seven_days_df.sort_values(by="data_inicio", ascending=True))
            .mark_line(color="gray", point=True)
            .transform_window(
                window=[{"op": "mean", "field": "qtd_chamados", "as": "media_movel"}],
                frame=[None, 0],
            )
            .encode(
                x=alt.X("data_inicio:T", title="Data"),
                y="media_movel:Q",
            )
        )
        col2.altair_chart(
            altair_chart=(bar_qtd_chamados + line_qtd_chamados),
            use_container_width=True,
            theme="streamlit",
        )

    with st.container():
        col1, col2 = st.columns([0.6, 0.4], gap="large")
        col1.subheader("Status dos chamados do dia")
        s_qtd_status_chamados = daily_chamados_df["status"].value_counts(
            ascending=False
        )
        s_qtd_status_chamados.index.name = "Status"
        df_qtd_status_chamados = s_qtd_status_chamados.reset_index(name="Quantidade")
        bar_daily_status_chamados = bar_plot(
            dataframe=df_qtd_status_chamados,
            x="Quantidade:Q",
            y=alt.Y("Status:N", sort="-x"),
            mark_bar_kw={"color": "blue"},
            config_xaxis={"labelFontSize": 8.0},
        )
        col1.altair_chart(
            altair_chart=bar_daily_status_chamados,
            use_container_width=True,
            theme="streamlit",
        )

        col2.subheader("Quantidade de chamados atendidos e não atendidos")
        s_daily_qtd_atendimento = daily_chamados_df["situacao"].value_counts(
            ascending=False
        )
        s_daily_qtd_atendimento.index.name = "Situação"
        df_daily_qtd_atendimento = s_daily_qtd_atendimento.reset_index(
            name="Quantidade"
        )
        bar_daily_atendimento_chamados = bar_plot(
            dataframe=df_daily_qtd_atendimento,
            x="Situação:N",
            y="Quantidade:Q",
            mark_bar_kw={"color": "blue"},
            config_xaxis={"labelAngle": 45.0},
        )
        col2.altair_chart(
            altair_chart=bar_daily_atendimento_chamados,
            use_container_width=True,
            theme="streamlit",
        )

    with st.container():
        st.subheader("Os 5 tipos de chamados mais abertos")
        s_daily_qtd_tipos_chamados_abertos = (
            daily_chamados_df[daily_chamados_df["status"] == "Aberto"][
                "tipo"
            ].value_counts(ascending=False, normalize=True)[:5]
            * 100.0
        )
        s_daily_qtd_tipos_chamados_abertos.index.name = "Tipo"
        df_daily_qtd_tipos_chamados_abertos = (
            s_daily_qtd_tipos_chamados_abertos.reset_index(name="Quantidade (%)")
        )
        df_color_pies_qtd_tipos = pd.DataFrame(
            data={
                "Tipo": df_daily_qtd_tipos_chamados_abertos["Tipo"],
                "Colors": pd.Series(
                    ["#aae1f2", "#a0b19e", "#f6f4f6", "#22595c", "#8c737c"]
                ),
            }
        )
        df_daily_qtd_tipos_chamados_abertos = df_daily_qtd_tipos_chamados_abertos.join(
            df_color_pies_qtd_tipos.set_index("Tipo"), on="Tipo", how="inner"
        )
        base_daily_qtd_tipos_chamados_abertos = alt.Chart(
            df_daily_qtd_tipos_chamados_abertos
        ).encode(
            theta="Quantidade (%):Q",
            color=alt.Color(
                field="Tipo", type="nominal", scale={"range": {"field": "Colors"}}
            ),
        )
        pie_chart_qtd_tipos_chamados = base_daily_qtd_tipos_chamados_abertos.mark_arc(
            innerRadius=50
        )
        st.altair_chart(
            altair_chart=(pie_chart_qtd_tipos_chamados),
            use_container_width=True,
            theme="streamlit",
        )

    with st.container():
        col1, col2 = st.columns([0.6, 0.4], gap="large")
        col1.subheader("Distribuição de chamados abertos por bairros")
        s_daily_qtd_chamados_abertos_por_bairro = daily_chamados_df[
            daily_chamados_df["status"] == "Aberto"
        ]["nome_bairro"].value_counts()
        s_daily_qtd_chamados_abertos_por_bairro.index.name = "nome_bairro"
        df_daily_qtd_chamados_abertos_por_bairro = (
            s_daily_qtd_chamados_abertos_por_bairro.reset_index(name="Quantidade")
        )

        # Geolocation plot para bairros
        s_bairro_geometry = (
            daily_chamados_df[daily_chamados_df["status"] == "Aberto"]
            .groupby(by="nome_bairro")["geometry_bairro"]
            .first()
        )
        df_daily_qtd_chamados_abertos_por_bairro = (
            df_daily_qtd_chamados_abertos_por_bairro.join(
                s_bairro_geometry, on="nome_bairro", how="inner"
            )
        )
        df_daily_qtd_chamados_abertos_por_bairro["geometry_bairro"] = (
            gpd.GeoSeries.from_wkt(
                df_daily_qtd_chamados_abertos_por_bairro["geometry_bairro"]
            )
        )
        gpd_daily_qtd_chamados_abertos_por_bairro = gpd.GeoDataFrame(
            df_daily_qtd_chamados_abertos_por_bairro, geometry="geometry_bairro"
        )
        fig, ax = plt.subplots(1, 1)
        gpd_daily_qtd_chamados_abertos_por_bairro.plot(
            column="Quantidade",
            cmap="Blues",
            ax=ax,
            edgecolor="black",
            legend=True,
            legend_kwds={"label": "Quantidade (%)", "orientation": "horizontal"},
        )
        col1.pyplot(fig)

        # Gráfico em barra com os bairros com mais chamados
        col2.subheader("Os 10 bairros com maior quantidade de chamados abertos")
        bar_qtd_bairros = bar_plot(
            dataframe=df_daily_qtd_chamados_abertos_por_bairro[
                ["nome_bairro", "Quantidade"]
            ].sort_values(by="Quantidade", ascending=False)[:10],
            x="Quantidade:Q",
            y=alt.Y("nome_bairro:N", sort="-x", title="Bairros"),
            mark_bar_kw={"color": "blue"},
        )
        col2.altair_chart(bar_qtd_bairros, use_container_width=True, theme="streamlit")
