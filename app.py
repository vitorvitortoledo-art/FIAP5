from __future__ import annotations

import pandas as pd
import streamlit as st

from src.analytics import (
    aggregate_by_day_hour,
    aggregate_by_hour,
    aggregate_time_series,
    calculate_kpis,
    compare_binary_group,
    congestion_distribution,
    correlation_matrix,
    critical_intersections,
    metric_by_category,
    ranking_by_group,
    strongest_correlations,
    vehicle_composition,
)
from src.charts import (
    PLOTLY_CONFIG,
    bar_chart,
    boxplot,
    composition_pie,
    congestion_donut,
    correlation_heatmap,
    heatmap_day_hour,
    histogram,
    line_time_series,
    map_intersections,
    multi_line_time_series,
)
from src.config import THEME
from src.data_cleaning import build_data_dictionary, build_data_quality_report, find_iqr_outliers, prepare_data
from src.data_loader import DataLoadError, load_data
from src.insights import build_insights, summarize_dataset


st.set_page_config(
    page_title="Smart City — Traffic & Mobility",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner="Preparando dados e indicadores...")
def load_project_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = load_data()
    prepared = prepare_data(raw)
    return raw, prepared


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        :root {{
            --page-bg: {THEME['page_bg']};
            --card-bg: {THEME['card_bg']};
            --surface: {THEME['surface']};
            --primary: {THEME['primary']};
            --success: {THEME['success']};
            --warning: {THEME['warning']};
            --danger: {THEME['danger']};
            --text: {THEME['text']};
            --muted: {THEME['muted']};
            --border: {THEME['border']};
        }}
        .stApp {{
            background:
                radial-gradient(circle at 18% 8%, rgba(56, 189, 248, 0.12), transparent 28%),
                radial-gradient(circle at 85% 12%, rgba(34, 197, 94, 0.07), transparent 24%),
                linear-gradient(135deg, #0B1120 0%, #101827 48%, #0B1120 100%);
            color: var(--text);
        }}
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0F172A 0%, #0B1120 100%);
            border-right: 1px solid rgba(56, 189, 248, 0.16);
        }}
        [data-testid="stMetric"] {{
            background: linear-gradient(145deg, rgba(17, 24, 39, 0.96), rgba(31, 41, 55, 0.72));
            border: 1px solid rgba(56, 189, 248, 0.16);
            border-radius: 18px;
            padding: 18px 18px 14px;
            box-shadow: 0 14px 32px rgba(0, 0, 0, 0.24);
        }}
        [data-testid="stMetricLabel"] p {{
            color: var(--muted) !important;
            font-size: 0.82rem;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }}
        [data-testid="stMetricValue"] {{
            color: var(--text) !important;
            font-weight: 800;
        }}
        h1, h2, h3 {{ color: var(--text); letter-spacing: -0.025em; }}
        h1 {{ font-size: 2.6rem !important; }}
        h2 {{ margin-top: 1.6rem !important; }}
        .hero {{
            padding: 28px 30px;
            border-radius: 26px;
            border: 1px solid rgba(56, 189, 248, 0.20);
            background:
                linear-gradient(135deg, rgba(56, 189, 248, 0.13), rgba(34, 197, 94, 0.06)),
                linear-gradient(145deg, rgba(17, 24, 39, 0.98), rgba(31, 41, 55, 0.72));
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.28);
            margin-bottom: 1.2rem;
        }}
        .hero .eyebrow {{
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-size: 0.78rem;
            font-weight: 800;
            margin-bottom: 0.45rem;
        }}
        .hero .title {{
            color: var(--text);
            font-size: clamp(2rem, 5vw, 4.2rem);
            line-height: 0.95;
            font-weight: 900;
            letter-spacing: -0.06em;
            margin: 0;
        }}
        .hero .subtitle {{
            color: var(--muted);
            max-width: 920px;
            font-size: 1.05rem;
            margin-top: 1rem;
        }}
        .panel {{
            padding: 20px;
            border-radius: 20px;
            background: rgba(17, 24, 39, 0.92);
            border: 1px solid rgba(56, 189, 248, 0.13);
            box-shadow: 0 18px 42px rgba(0,0,0,0.22);
            margin-bottom: 1rem;
        }}
        .insight-card {{
            padding: 18px;
            border-radius: 18px;
            background: linear-gradient(145deg, rgba(17,24,39,0.96), rgba(31,41,55,0.72));
            border-left: 4px solid var(--primary);
            border-top: 1px solid rgba(56, 189, 248, 0.12);
            border-right: 1px solid rgba(56, 189, 248, 0.12);
            border-bottom: 1px solid rgba(56, 189, 248, 0.12);
            margin-bottom: 12px;
        }}
        .insight-card.warning {{ border-left-color: var(--warning); }}
        .insight-card.critical {{ border-left-color: var(--danger); }}
        .insight-card.info {{ border-left-color: var(--primary); }}
        .insight-title {{ color: var(--text); font-weight: 800; font-size: 1.02rem; margin-bottom: 4px; }}
        .insight-indicator {{ color: var(--primary); font-weight: 800; font-size: 0.95rem; margin-bottom: 7px; }}
        .insight-body {{ color: var(--muted); font-size: 0.92rem; line-height: 1.45; }}
        .small-muted {{ color: var(--muted); font-size: 0.9rem; }}
        .status-ok {{ color: var(--success); font-weight: 800; }}
        .status-bad {{ color: var(--danger); font-weight: 800; }}
        div[data-testid="stDataFrame"] {{ border: 1px solid rgba(56, 189, 248, 0.14); border-radius: 14px; }}
        .stButton > button {{
            width: 100%;
            background: rgba(56, 189, 248, 0.10);
            color: var(--text);
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 12px;
            font-weight: 700;
        }}
        .stButton > button:hover {{
            background: rgba(56, 189, 248, 0.18);
            border-color: var(--primary);
            color: var(--text);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_int(value: float | int) -> str:
    return f"{int(round(value)):,}".replace(",", ".")


def format_float(value: float, decimals: int = 2) -> str:
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def render_hero() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Urban Intelligence Platform</div>
            <div class="title">Smart City<br/>Traffic & Mobility</div>
            <div class="subtitle">
                Dashboard analítico de mobilidade urbana baseado exclusivamente nos registros reais do CSV do projeto,
                com filtros globais, KPIs dinâmicos, padrões temporais, pontos críticos e diagnóstico de qualidade dos dados.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_cards(insights: list[dict]) -> None:
    for insight in insights:
        severity = insight.get("severity", "info")
        st.markdown(
            f"""
            <div class="insight-card {severity}">
                <div class="insight-title">{insight.get('title', '')}</div>
                <div class="insight-indicator">{insight.get('indicator', '')}</div>
                <div class="insight-body">{insight.get('body', '')}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_kpis(df: pd.DataFrame) -> None:
    kpis = calculate_kpis(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Veículos observados", format_int(kpis["total_vehicles"]))
    c2.metric("Velocidade média", f"{format_float(kpis['avg_speed'], 1)} km/h")
    c3.metric("Congestionamento médio", f"{format_float(kpis['avg_congestion'], 1)}/100")
    c4.metric("Registros severos", f"{format_float(kpis['severe_share'], 1)}%")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Interseções", format_int(kpis["unique_intersections"]))
    c6.metric("Zonas urbanas", format_int(kpis["unique_zones"]))
    c7.metric("Fila média", format_float(kpis["avg_queue"], 1))
    c8.metric("Espera média", format_float(kpis["avg_wait"], 1))


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()
    date_range = st.session_state.get("filter_date_range")
    if "timestamp" in filtered.columns and date_range:
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start, end = date_range
            filtered = filtered[
                (filtered["timestamp"].dt.date >= start) & (filtered["timestamp"].dt.date <= end)
            ]

    for col in ["city_zone", "road_type", "congestion_level", "peak_period", "weather_condition", "road_condition", "iot_sensor_health"]:
        selected = st.session_state.get(f"filter_{col}", [])
        if selected and col in filtered.columns:
            filtered = filtered[filtered[col].astype(str).isin(selected)]

    for col in ["vehicle_count", "average_speed", "congestion_score"]:
        bounds = st.session_state.get(f"filter_range_{col}")
        if bounds and col in filtered.columns:
            filtered = filtered[filtered[col].between(bounds[0], bounds[1])]

    return filtered


def reset_filters() -> None:
    for key in list(st.session_state.keys()):
        if key.startswith("filter_") or key in {"explorer_search", "explorer_columns"}:
            del st.session_state[key]


def sidebar_filters(df: pd.DataFrame) -> str:
    st.sidebar.markdown("## 🚦 Controle")
    page = st.sidebar.radio(
        "Página",
        [
            "Overview / Visão Geral",
            "Traffic Analytics",
            "Mobility Insights",
            "Data Explorer",
            "Data Quality",
        ],
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("## Filtros globais")
    if st.sidebar.button("Limpar filtros"):
        reset_filters()
        st.rerun()

    if "timestamp" in df.columns and df["timestamp"].notna().any():
        min_date = df["timestamp"].min().date()
        max_date = df["timestamp"].max().date()
        st.sidebar.date_input(
            "Intervalo de datas",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="filter_date_range",
        )

    for col in ["city_zone", "road_type", "congestion_level", "peak_period", "weather_condition", "road_condition", "iot_sensor_health"]:
        if col in df.columns:
            options = sorted(df[col].astype(str).dropna().unique().tolist())
            st.sidebar.multiselect(
                col,
                options=options,
                default=[],
                key=f"filter_{col}",
                help="Sem seleção = todos os valores.",
            )

    st.sidebar.markdown("### Ranges numéricos")
    for col in ["vehicle_count", "average_speed", "congestion_score"]:
        if col in df.columns:
            min_value = float(df[col].min())
            max_value = float(df[col].max())
            if min_value < max_value:
                st.sidebar.slider(
                    col,
                    min_value=min_value,
                    max_value=max_value,
                    value=(min_value, max_value),
                    key=f"filter_range_{col}",
                )
            else:
                st.sidebar.caption(f"{col}: valor fixo {format_float(min_value)}")

    return page


def render_filter_context(raw: pd.DataFrame, filtered: pd.DataFrame) -> None:
    start = filtered["timestamp"].min() if "timestamp" in filtered.columns and not filtered.empty else None
    end = filtered["timestamp"].max() if "timestamp" in filtered.columns and not filtered.empty else None
    period = f"{start:%d/%m/%Y %H:%M} — {end:%d/%m/%Y %H:%M}" if start is not None and pd.notna(start) else "Sem registros"
    st.markdown(
        f"<div class='small-muted'>Registros filtrados: <b>{format_int(len(filtered))}</b> de <b>{format_int(len(raw))}</b> · Período: <b>{period}</b></div>",
        unsafe_allow_html=True,
    )


def page_overview(df: pd.DataFrame, raw: pd.DataFrame) -> None:
    render_hero()
    render_filter_context(raw, df)
    st.write("")
    if df.empty:
        st.warning("Nenhum registro encontrado para os filtros selecionados.")
        return

    render_kpis(df)
    st.write("")

    time_df = aggregate_time_series(df, "D")
    col1, col2 = st.columns((1.55, 1))
    with col1:
        st.plotly_chart(line_time_series(time_df, "vehicle_count", "Volume médio diário de veículos", "Veículos médios"), use_container_width=True, config=PLOTLY_CONFIG)
    with col2:
        st.plotly_chart(congestion_donut(congestion_distribution(df)), use_container_width=True, config=PLOTLY_CONFIG)

    col3, col4 = st.columns(2)
    with col3:
        zone = ranking_by_group(df, "city_zone", "vehicle_count", 8)
        st.plotly_chart(bar_chart(zone, "city_zone", "vehicle_count", "Zonas por volume médio", y_label="Veículos médios"), use_container_width=True, config=PLOTLY_CONFIG)
    with col4:
        road = ranking_by_group(df, "road_type", "congestion_score", 8)
        st.plotly_chart(bar_chart(road, "road_type", "congestion_score", "Tipo de via por congestionamento médio", y_label="Score médio"), use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("## Insights executivos")
    render_insight_cards(build_insights(df))


def page_traffic_analytics(df: pd.DataFrame, raw: pd.DataFrame) -> None:
    st.title("Traffic Analytics")
    render_filter_context(raw, df)
    if df.empty:
        st.warning("Nenhum registro encontrado para os filtros selecionados.")
        return

    daily = aggregate_time_series(df, "D")
    st.plotly_chart(multi_line_time_series(daily, ["vehicle_count", "congestion_score", "queue_length"], "Evolução diária de volume, congestionamento e filas"), use_container_width=True, config=PLOTLY_CONFIG)

    col1, col2 = st.columns(2)
    with col1:
        hourly = aggregate_by_hour(df)
        st.plotly_chart(bar_chart(hourly, "hour", "vehicle_count", "Volume médio por hora", y_label="Veículos médios"), use_container_width=True, config=PLOTLY_CONFIG)
    with col2:
        heat = aggregate_by_day_hour(df, "vehicle_count")
        st.plotly_chart(heatmap_day_hour(heat, "vehicle_count", "Heatmap de volume médio — hora × dia"), use_container_width=True, config=PLOTLY_CONFIG)

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(boxplot(df, "peak_period", "vehicle_count", "Distribuição de veículos por período"), use_container_width=True, config=PLOTLY_CONFIG)
    with col4:
        st.plotly_chart(boxplot(df, "road_type", "average_speed", "Velocidade média por tipo de via"), use_container_width=True, config=PLOTLY_CONFIG)

    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(histogram(df, "congestion_score", "Distribuição do score de congestionamento"), use_container_width=True, config=PLOTLY_CONFIG)
    with col6:
        rush = compare_binary_group(df, "rush_hour", "vehicle_count")
        rush_df = pd.DataFrame(
            [
                {"Grupo": "Rush hour", "Volume médio": rush.get("active_mean", 0)},
                {"Grupo": "Fora de rush hour", "Volume médio": rush.get("inactive_mean", 0)},
            ]
        )
        st.plotly_chart(bar_chart(rush_df, "Grupo", "Volume médio", "Comparação rush hour vs demais horários"), use_container_width=True, config=PLOTLY_CONFIG)


def page_mobility_insights(df: pd.DataFrame, raw: pd.DataFrame) -> None:
    st.title("Mobility Insights")
    render_filter_context(raw, df)
    if df.empty:
        st.warning("Nenhum registro encontrado para os filtros selecionados.")
        return

    col1, col2 = st.columns((1, 1.2))
    with col1:
        st.markdown("### Leitura executiva")
        render_insight_cards(build_insights(df))
    with col2:
        critical = critical_intersections(df, 15)
        st.plotly_chart(bar_chart(critical, "intersection_id", "criticality_index", "Top interseções por índice de criticidade", orientation="h", y_label="Índice"), use_container_width=True, config=PLOTLY_CONFIG)

    col3, col4 = st.columns(2)
    with col3:
        map_df = critical_intersections(df, 100)
        st.plotly_chart(map_intersections(map_df), use_container_width=True, config=PLOTLY_CONFIG)
    with col4:
        comp = vehicle_composition(df)
        st.plotly_chart(composition_pie(comp), use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("### Correlação entre métricas")
    st.caption("Correlação mede associação linear no recorte filtrado e não implica causalidade.")
    corr = correlation_matrix(df)
    col5, col6 = st.columns((1.2, 1))
    with col5:
        st.plotly_chart(correlation_heatmap(corr), use_container_width=True, config=PLOTLY_CONFIG)
    with col6:
        st.dataframe(strongest_correlations(corr), use_container_width=True, hide_index=True)

    st.markdown("### Outliers por IQR")
    outlier_cols = [col for col in ["vehicle_count", "queue_length", "average_wait_time", "emission_estimate", "fuel_waste_estimate"] if col in df.columns]
    st.dataframe(find_iqr_outliers(df, outlier_cols), use_container_width=True, hide_index=True)


def page_data_explorer(df: pd.DataFrame, raw: pd.DataFrame) -> None:
    st.title("Data Explorer")
    render_filter_context(raw, df)

    search = st.text_input("Busca textual em IDs e categorias", key="explorer_search")
    view_df = df.copy()
    if search:
        text_cols = [col for col in view_df.columns if str(view_df[col].dtype) in {"object", "category"} or col.endswith("_id")]
        if text_cols:
            mask = pd.Series(False, index=view_df.index)
            for col in text_cols:
                mask = mask | view_df[col].astype(str).str.contains(search, case=False, na=False)
            view_df = view_df[mask]

    default_columns = [col for col in ["timestamp", "city_zone", "road_id", "intersection_id", "road_type", "vehicle_count", "average_speed", "congestion_score", "congestion_level"] if col in view_df.columns]
    selected_columns = st.multiselect(
        "Colunas exibidas",
        options=list(view_df.columns),
        default=default_columns or list(view_df.columns[:12]),
        key="explorer_columns",
    )

    st.caption(f"Registros na tabela: {format_int(len(view_df))}")
    if view_df.empty:
        st.warning("Nenhum registro encontrado para a busca/filtros atuais.")
        return

    shown = view_df[selected_columns] if selected_columns else view_df
    st.dataframe(shown, use_container_width=True, height=560)

    csv = shown.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Baixar dados filtrados em CSV",
        csv,
        file_name="smart_city_traffic_mobility_filtrado.csv",
        mime="text/csv",
    )

    with st.expander("Resumo do recorte filtrado"):
        for item in summarize_dataset(view_df):
            st.markdown(f"- {item}")


def page_data_quality(df: pd.DataFrame, raw: pd.DataFrame) -> None:
    st.title("Data Quality")
    render_filter_context(raw, df)

    raw_report = build_data_quality_report(raw)
    filtered_report = build_data_quality_report(df)

    st.markdown("### Qualidade do CSV original")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Linhas originais", format_int(raw_report["rows"]))
    c2.metric("Colunas originais", format_int(raw_report["columns"]))
    c3.metric("Valores ausentes", format_int(raw_report["missing_total"]))
    c4.metric("Duplicatas", format_int(raw_report["duplicate_rows"]))

    schema = raw_report["schema"]
    st.markdown("### Status do esquema original")
    schema_status = "OK" if schema["schema_ok"] else "Atenção"
    status_html = (
        '<span class="status-ok">OK</span>'
        if schema_status == "OK"
        else '<span class="status-bad">Atenção</span>'
    )
    st.markdown(f"**Status:** {status_html}", unsafe_allow_html=True)
    if schema["missing_columns"]:
        st.error(f"Colunas esperadas ausentes: {', '.join(schema['missing_columns'])}")
    if schema["unexpected_columns"]:
        st.warning(f"Colunas não previstas no esquema original: {', '.join(schema['unexpected_columns'])}")

    col0a, col0b = st.columns(2)
    with col0a:
        st.markdown("### Validações do CSV original")
        validations = pd.DataFrame(
            [{"Validação": key, "Status": "OK" if value else "Atenção"} for key, value in raw_report["validations"].items()]
        )
        st.dataframe(validations, use_container_width=True, hide_index=True, height=360)
    with col0b:
        st.markdown("### Recorte filtrado preparado")
        c5, c6 = st.columns(2)
        c5.metric("Linhas filtradas", format_int(filtered_report["rows"]))
        c6.metric("Colunas em memória", format_int(filtered_report["columns"]))
        st.caption(
            "O recorte preparado inclui colunas derivadas para análise; por isso pode ter mais colunas do que o CSV original."
        )
        filtered_validations = pd.DataFrame(
            [{"Validação": key, "Status": "OK" if value else "Atenção"} for key, value in filtered_report["validations"].items()]
        )
        st.dataframe(filtered_validations, use_container_width=True, hide_index=True, height=254)

    st.markdown("### Valores ausentes por coluna no CSV original")
    nulls = raw_report["nulls_by_column"].reset_index()
    nulls.columns = ["Coluna", "Nulos"]
    st.plotly_chart(bar_chart(nulls, "Coluna", "Nulos", "Nulos por coluna"), use_container_width=True, config=PLOTLY_CONFIG)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Dicionário de dados")
        st.dataframe(build_data_dictionary(df), use_container_width=True, hide_index=True, height=520)
    with col2:
        st.markdown("### Cardinalidade e tipos do CSV original")
        card = pd.DataFrame(
            {
                "Coluna": raw_report["cardinality"].index,
                "Cardinalidade": raw_report["cardinality"].values,
                "Tipo": raw_report["dtypes"].values,
            }
        ).sort_values("Cardinalidade", ascending=False)
        st.dataframe(card, use_container_width=True, hide_index=True, height=520)

    st.info("O CSV original é preservado. Conversões e colunas derivadas são criadas apenas em memória para análise no dashboard.")


def main() -> None:
    inject_css()
    try:
        raw_df, df = load_project_data()
    except DataLoadError as exc:
        st.error(str(exc))
        st.stop()
    except Exception as exc:
        st.error("Não foi possível carregar ou preparar os dados do projeto.")
        st.caption(str(exc))
        st.stop()

    page = sidebar_filters(df)
    filtered = apply_filters(df)

    if page == "Overview / Visão Geral":
        page_overview(filtered, df)
    elif page == "Traffic Analytics":
        page_traffic_analytics(filtered, df)
    elif page == "Mobility Insights":
        page_mobility_insights(filtered, df)
    elif page == "Data Explorer":
        page_data_explorer(filtered, df)
    elif page == "Data Quality":
        page_data_quality(filtered, raw_df)


if __name__ == "__main__":
    main()
