# -*- coding: utf-8 -*-
"""
Dashboard CRM Data Quality & Campaign Readiness
================================================
Projet de validation - Data Visualisation (M2).

Lancement :
    streamlit run streamlit_app.py

Données attendues (produites par le notebook) :
    data/processed/crm_quality_clean.csv
    data/processed/crm_quality_issues.csv
    reports/kpi_summary.csv  (optionnel)
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# --------------------------------------------------------------------------- #
# Configuration générale
# --------------------------------------------------------------------------- #
st.set_page_config(
    page_title="CRM Data Quality | Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_DIR = Path(__file__).parent / "data" / "processed"
REPORTS_DIR = Path(__file__).parent / "reports"
CLEAN_PATH = DATA_DIR / "crm_quality_clean.csv"
ISSUES_PATH = DATA_DIR / "crm_quality_issues.csv"

# Palette sémantique ---------------------------------------------------------
INDIGO = "#4F46E5"
GREEN = "#16A34A"
BLUE = "#2563EB"
AMBER = "#F59E0B"
RED = "#DC2626"
SLATE = "#64748B"
INK = "#0F172A"

QUALITY_ORDER = ["Excellent", "Correct", "À corriger", "Critique"]
QUALITY_COLORS = {
    "Excellent": GREEN,
    "Correct": BLUE,
    "À corriger": AMBER,
    "Critique": RED,
}
SEVERITY_ORDER = ["Haute", "Moyenne", "Faible"]
SEVERITY_COLORS = {"Haute": RED, "Moyenne": AMBER, "Faible": SLATE}

STATUS_LABELS = {
    "mql": "MQL", "sql": "SQL", "working": "Working", "converted": "Converted",
    "disqualified": "Disqualified", "new": "New", "nurture": "Nurture",
}

PLOTLY_FONT = dict(family="Inter, Segoe UI, sans-serif", color=INK, size=13)


# --------------------------------------------------------------------------- #
# Styles (CSS)
# --------------------------------------------------------------------------- #
def inject_css() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1500px;}
        #MainMenu, footer {visibility: hidden;}

        /* En-tête */
        .app-header {
            background: linear-gradient(110deg, #1E1B4B 0%, #4F46E5 55%, #6366F1 100%);
            color: #fff; padding: 1.4rem 1.8rem; border-radius: 16px;
            box-shadow: 0 10px 30px rgba(79,70,229,.25); margin-bottom: 1.2rem;
        }
        .app-header h1 {font-size: 1.55rem; margin: 0; font-weight: 700; letter-spacing:-.01em;}
        .app-header p {margin: .35rem 0 0; opacity: .9; font-size: .95rem;}

        /* Cartes KPI (st.metric) */
        div[data-testid="stMetric"] {
            background: #fff; border: 1px solid #E2E8F0; border-radius: 14px;
            padding: 0.9rem 1rem; box-shadow: 0 1px 3px rgba(15,23,42,.06);
            transition: transform .15s ease, box-shadow .15s ease;
            min-height: 132px; overflow: visible;
            display: flex; flex-direction: column; justify-content: flex-start;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px); box-shadow: 0 8px 22px rgba(15,23,42,.10);
        }
        /* Anti-troncature GLOBALE sur les cartes KPI (override forcé) */
        div[data-testid="stMetric"],
        div[data-testid="stMetric"] * {
            overflow: visible !important;
            text-overflow: clip !important;
            max-width: none !important;
        }
        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] * {
            white-space: normal !important;
        }
        div[data-testid="stMetricLabel"] p {
            font-size: .72rem !important; font-weight: 700; color: #64748B;
            text-transform: uppercase; letter-spacing: .02em;
            line-height: 1.15; min-height: 2.1em;
        }
        /* Valeur : sur une ligne mais jamais coupée (ex. 75,3/100) */
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] * {
            white-space: nowrap !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 1.5rem; font-weight: 800; color: #0F172A;
        }
        /* Delta : badge qui s'agrandit et passe à la ligne au lieu de tronquer */
        div[data-testid="stMetricDelta"],
        div[data-testid="stMetricDelta"] * {
            white-space: normal !important;
        }
        div[data-testid="stMetricDelta"] {
            font-size: .72rem; line-height: 1.1; height: auto !important;
        }
        div[data-testid="stMetricDelta"] svg {flex: 0 0 auto;}

        /* Onglets */
        button[data-baseweb="tab"] {font-size: 1rem; font-weight: 600;}
        .stTabs [data-baseweb="tab-list"] {gap: 6px;}

        /* Sidebar */
        section[data-testid="stSidebar"] {background: #0F172A;}
        section[data-testid="stSidebar"] * {color: #E2E8F0;}
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {color: #fff;}

        .insight {
            background:#F8FAFC; border-left:4px solid #4F46E5; border-radius:8px;
            padding:.7rem 1rem; font-size:.9rem; color:#334155; margin:.4rem 0 1rem;
        }
        h3.section {margin-top:.4rem; color:#1E293B; font-weight:700;}
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------- #
# Chargement des données
# --------------------------------------------------------------------------- #
@st.cache_data(show_spinner=False)
def load_data():
    if not CLEAN_PATH.exists():
        return None, None
    df = pd.read_csv(CLEAN_PATH)

    for col in ["lead_created_at", "lead_converted_at", "first_activity_date",
                "last_activity_date", "campaign_start_date", "campaign_end_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in ["email_valid", "phone_valid", "is_duplicate", "campaign_ready",
                "has_contact", "has_campaign", "has_source", "has_company",
                "has_activity", "duplicate_company_name"]:
        if col in df.columns:
            df[col] = df[col].astype(bool)

    df["is_converted"] = df["lead_converted_at"].notna()
    df["source_disp"] = df["source_final"].fillna("Non renseigné").str.title()
    df["channel_disp"] = df["campaign_channel"].fillna("Non renseigné").str.title()
    df["status_disp"] = df["lead_status_clean"].map(STATUS_LABELS).fillna(
        df["lead_status_clean"].fillna("Inconnu").str.title())
    df["month"] = df["lead_created_at"].dt.to_period("M").dt.to_timestamp()

    issues = pd.read_csv(ISSUES_PATH) if ISSUES_PATH.exists() else pd.DataFrame()
    return df, issues


def style_fig(fig, height=360, legend_bottom=False):
    fig.update_layout(
        height=height, font=PLOTLY_FONT,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        title=dict(font=dict(size=15, color=INK), x=0.01, xanchor="left"),
        hoverlabel=dict(font_size=12, bgcolor="white"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#EEF2F7", zeroline=False)
    if legend_bottom:
        fig.update_layout(legend=dict(orientation="h", y=-0.18, x=0,
                                      title_text=""))
    return fig


def pct(x):
    return f"{x*100:.1f} %".replace(".", ",")


def fr(x, dec=1):
    """Formate un nombre avec la virgule décimale française."""
    return f"{x:.{dec}f}".replace(".", ",")


def nb(x):
    """Formate un entier avec un séparateur de milliers (espace insécable)."""
    return f"{int(x):,}".replace(",", " ")


# --------------------------------------------------------------------------- #
# Application
# --------------------------------------------------------------------------- #
inject_css()
df, issues = load_data()

if df is None:
    st.error(
        "Fichier introuvable : `data/processed/crm_quality_clean.csv`.\n\n"
        "Exécute d'abord le notebook pour générer les exports."
    )
    st.stop()

# --- Sidebar : filtres ------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎛️ Filtres")
    st.caption("Affinez l'ensemble du tableau de bord.")

    dmin, dmax = df["lead_created_at"].min(), df["lead_created_at"].max()
    date_range = st.date_input(
        "Période de création du lead",
        value=(dmin.date(), dmax.date()),
        min_value=dmin.date(), max_value=dmax.date(),
    )

    sources = sorted(df["source_disp"].unique())
    sel_sources = st.multiselect("Source marketing", sources, default=[])

    channels = sorted(df["channel_disp"].unique())
    sel_channels = st.multiselect("Canal de campagne", channels, default=[])

    statuses = sorted(df["status_disp"].unique())
    sel_status = st.multiselect("Statut du lead", statuses, default=[])

    sel_quality = st.multiselect(
        "Niveau de qualité",
        [q for q in QUALITY_ORDER if q in df["quality_level"].unique()],
        default=[],
    )

    only_ready = st.checkbox("Uniquement les leads campaign-ready", value=False)

    st.divider()
    st.caption("Projet M2 · Données GTM (mini-gtm-data-platform)")

# --- Application des filtres ------------------------------------------------
f = df.copy()
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)
    f = f[(f["lead_created_at"] >= start) & (f["lead_created_at"] < end)]
if sel_sources:
    f = f[f["source_disp"].isin(sel_sources)]
if sel_channels:
    f = f[f["channel_disp"].isin(sel_channels)]
if sel_status:
    f = f[f["status_disp"].isin(sel_status)]
if sel_quality:
    f = f[f["quality_level"].isin(sel_quality)]
if only_ready:
    f = f[f["campaign_ready"]]

f_issues = issues[issues["lead_id"].isin(f["lead_id"])] if not issues.empty else issues

# --- En-tête ----------------------------------------------------------------
st.markdown(
    """
    <div class="app-header">
        <h1>📊 CRM Data Quality &amp; Campaign Readiness</h1>
        <p>Surveiller la fiabilité du CRM et prioriser les corrections pour des campagnes marketing efficaces.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if f.empty:
    st.warning("Aucun lead ne correspond aux filtres sélectionnés.")
    st.stop()

# --- Bandeau KPI ------------------------------------------------------------
n = len(f)
score_avg = f["quality_score"].mean()
ready_rate = f["campaign_ready"].mean()
email_rate = f["email_valid"].mean()
phone_rate = f["phone_valid"].mean()
phone_conv = f.loc[f["is_converted"], "phone_valid"].mean() if f["is_converted"].any() else 0
dup_n = int(f["is_duplicate"].sum())
issues_n = len(f_issues)

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Leads analysés", nb(n))
k2.metric("Score qualité moyen", f"{fr(score_avg)}/100")
k3.metric("Campaign-ready", pct(ready_rate))
k4.metric("Emails valides", pct(email_rate), f"-{int((~f['email_valid']).sum())} à corriger",
          delta_color="inverse")
k5.metric("Téléphones valides", pct(phone_rate), f"{pct(phone_conv)} si converti",
          delta_color="off")
k6.metric("Anomalies à traiter", nb(issues_n))

st.write("")

# --- Onglets ----------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["🏠 Direction", "📈 Sources", "🎯 Campagnes", "🛠️ Actions correctives"]
)

# =========================== PAGE 1 — DIRECTION ============================ #
with tab1:
    st.markdown('<h3 class="section">La base est-elle fiable ?</h3>', unsafe_allow_html=True)
    crit = int((f["quality_level"] == "Critique").sum())
    st.markdown(
        f'<div class="insight">🔎 <b>{pct(ready_rate)}</b> des {nb(n)} leads sont exploitables '
        f'pour une campagne, avec un score moyen de <b>{fr(score_avg)}/100</b>. '
        f'<b>{nb(crit)}</b> lead(s) critique(s) · <b>{nb(dup_n)}</b> doublon(s) exact(s).</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 1.3])
    with c1:
        # Jauge score global
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(score_avg, 1),
            number={"suffix": "/100", "font": {"size": 34}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1},
                "bar": {"color": INDIGO},
                "steps": [
                    {"range": [0, 40], "color": "#FEE2E2"},
                    {"range": [40, 60], "color": "#FEF3C7"},
                    {"range": [60, 80], "color": "#DBEAFE"},
                    {"range": [80, 100], "color": "#DCFCE7"},
                ],
                "threshold": {"line": {"color": INK, "width": 3}, "value": 60},
            },
        ))
        gauge.update_layout(title="Score qualité CRM global")
        st.plotly_chart(style_fig(gauge, 320), width="stretch")

    with c2:
        ql = (f["quality_level"].value_counts()
              .reindex(QUALITY_ORDER).dropna().reset_index())
        ql.columns = ["quality_level", "count"]
        donut = px.pie(
            ql, names="quality_level", values="count", hole=0.58,
            color="quality_level", color_discrete_map=QUALITY_COLORS,
            title="Répartition des leads par niveau de qualité",
        )
        donut.update_traces(textinfo="percent+label", sort=False)
        st.plotly_chart(style_fig(donut, 320, legend_bottom=True), width="stretch")

    c3, c4 = st.columns([1.4, 1])
    with c3:
        ts = (f.dropna(subset=["month"]).groupby("month")
              .agg(score=("quality_score", "mean"), leads=("lead_id", "count"))
              .reset_index())
        line = px.line(ts, x="month", y="score", markers=True,
                       title="Évolution du score qualité moyen dans le temps")
        line.update_traces(line_color=INDIGO, line_width=3,
                           marker=dict(size=6, color=INDIGO))
        line.add_hline(y=60, line_dash="dash", line_color=SLATE,
                       annotation_text="Seuil Correct (60)", annotation_position="top left")
        line.update_yaxes(title="Score moyen")
        line.update_xaxes(title="")
        st.plotly_chart(style_fig(line, 340), width="stretch")

    with c4:
        tops = (f.groupby("source_disp")
                .agg(score=("quality_score", "mean"))
                .reset_index().sort_values("score", ascending=True).tail(10))
        bar = px.bar(tops, x="score", y="source_disp", orientation="h",
                     title="Score qualité moyen par source", text_auto=".0f")
        bar.update_traces(marker_color=INDIGO)
        bar.update_xaxes(title="Score moyen")
        bar.update_yaxes(title="")
        st.plotly_chart(style_fig(bar, 340), width="stretch")

# ============================ PAGE 2 — SOURCES ============================= #
with tab2:
    st.markdown('<h3 class="section">Quelles sources produisent les leads les plus fiables ?</h3>',
                unsafe_allow_html=True)

    g = (f.groupby("source_disp").agg(
        leads=("lead_id", "count"),
        score=("quality_score", "mean"),
        ready=("campaign_ready", "mean"),
        email=("email_valid", "mean"),
        phone=("phone_valid", "mean"),
    ).reset_index())

    best = g.sort_values("score", ascending=False).iloc[0]
    worst = g.sort_values("score", ascending=False).iloc[-1]
    st.markdown(
        f'<div class="insight">🏆 Source la plus fiable : <b>{best["source_disp"]}</b> '
        f'({best["score"]:.0f}/100) · ⚠️ la plus faible : <b>{worst["source_disp"]}</b> '
        f'({worst["score"]:.0f}/100). Renforcer les premières, corriger les formulaires des secondes.</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        gs = g.sort_values("score", ascending=True)
        bar = px.bar(gs, x="score", y="source_disp", orientation="h",
                     color="score", color_continuous_scale=["#C7D2FE", INDIGO],
                     title="Score qualité moyen par source", text_auto=".1f")
        bar.update_yaxes(title="")
        bar.update_xaxes(title="Score moyen")
        bar.update_coloraxes(showscale=False)
        st.plotly_chart(style_fig(bar, 420), width="stretch")

    with c2:
        heat = g.set_index("source_disp")[["ready", "email", "phone"]] * 100
        heat = heat.round(0)
        heat.columns = ["Campaign-ready", "Email valide", "Tél. valide"]
        hm = px.imshow(
            heat, text_auto=".0f", aspect="auto",
            color_continuous_scale="RdYlGn", zmin=0, zmax=100,
            title="Taux de qualité par source (%)",
        )
        hm.update_xaxes(title="", side="bottom")
        hm.update_yaxes(title="")
        hm.update_coloraxes(showscale=False)
        st.plotly_chart(style_fig(hm, 420), width="stretch")

    sc = px.scatter(
        g, x="leads", y="score", size="leads", color="ready",
        color_continuous_scale="RdYlGn", hover_name="source_disp",
        title="Volume vs qualité par source (couleur = taux campaign-ready)",
        labels={"leads": "Nombre de leads", "score": "Score moyen", "ready": "Ready"},
    )
    sc.update_layout(coloraxis_colorbar=dict(title="Ready", tickformat=".0%"))
    st.plotly_chart(style_fig(sc, 380), width="stretch")

# =========================== PAGE 3 — CAMPAGNES ============================ #
with tab3:
    st.markdown('<h3 class="section">Quelles campagnes pilotent le mieux la qualité ?</h3>',
                unsafe_allow_html=True)

    topn = st.slider("Nombre de campagnes affichées (par volume)", 5, 25, 12)
    fc = f.dropna(subset=["campaign_name"])

    gc = (fc.groupby(["campaign_name", "channel_disp"]).agg(
        leads=("lead_id", "count"),
        score=("quality_score", "mean"),
        ready=("campaign_ready", "mean"),
        activities=("total_activities", "sum"),
    ).reset_index().sort_values("leads", ascending=False).head(topn))

    st.markdown(
        f'<div class="insight">📣 <b>{fc["campaign_name"].nunique()}</b> campagnes actives. '
        f'Les barres ci-dessous (top {topn} par volume) sont colorées par canal : '
        f'repérez les campagnes à fort volume mais faible score.</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1.3, 1])
    with c1:
        bar = px.bar(
            gc.sort_values("leads"), x="leads", y="campaign_name", orientation="h",
            color="score", color_continuous_scale="RdYlGn",
            title="Volume de leads par campagne (couleur = score qualité)",
            hover_data={"score": ":.1f", "ready": ":.0%"},
        )
        bar.update_yaxes(title="")
        bar.update_xaxes(title="Nombre de leads")
        bar.update_layout(coloraxis_colorbar=dict(title="Score"))
        st.plotly_chart(style_fig(bar, 480), width="stretch")

    with c2:
        gch = (f.groupby("channel_disp").agg(
            ready=("campaign_ready", "mean"), leads=("lead_id", "count")
        ).reset_index().sort_values("ready"))
        bch = px.bar(gch, x="ready", y="channel_disp", orientation="h",
                     title="Taux campaign-ready par canal", text_auto=".0%")
        bch.update_traces(marker_color=GREEN)
        bch.update_xaxes(title="", tickformat=".0%")
        bch.update_yaxes(title="")
        st.plotly_chart(style_fig(bch, 480), width="stretch")

# ====================== PAGE 4 — ACTIONS CORRECTIVES ======================= #
with tab4:
    st.markdown('<h3 class="section">Que faut-il corriger en priorité ?</h3>',
                unsafe_allow_html=True)

    if f_issues.empty:
        st.info("Aucune anomalie pour la sélection courante.")
    else:
        top_issue = f_issues["issue_type"].value_counts().idxmax()
        top_cnt = int(f_issues["issue_type"].value_counts().max())
        st.markdown(
            f'<div class="insight">🛠️ <b>{nb(len(f_issues))}</b> anomalies recensées. '
            f'Priorité n°1 : <b>{top_issue}</b> ({nb(top_cnt)} cas).</div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns([1.4, 1])
        with c1:
            it = f_issues["issue_type"].value_counts().reset_index()
            it.columns = ["issue_type", "count"]
            bar = px.bar(it.sort_values("count"), x="count", y="issue_type",
                         orientation="h", title="Anomalies par type", text_auto=True)
            bar.update_traces(marker_color=INDIGO)
            bar.update_yaxes(title="")
            bar.update_xaxes(title="Nombre de leads concernés")
            st.plotly_chart(style_fig(bar, 380), width="stretch")

        with c2:
            sv = (f_issues["severity"].value_counts()
                  .reindex(SEVERITY_ORDER).dropna().reset_index())
            sv.columns = ["severity", "count"]
            pie = px.pie(sv, names="severity", values="count", hole=0.5,
                         color="severity", color_discrete_map=SEVERITY_COLORS,
                         title="Répartition par sévérité")
            pie.update_traces(textinfo="percent+label", sort=False)
            st.plotly_chart(style_fig(pie, 380, legend_bottom=True), width="stretch")

        # Détail des erreurs téléphone
        ph = f_issues[f_issues["field_name"] == "phone"]
        if not ph.empty and ph["issue_detail"].notna().any():
            pd_det = ph["issue_detail"].fillna("Non précisé").value_counts().reset_index()
            pd_det.columns = ["issue_detail", "count"]
            bph = px.bar(pd_det.sort_values("count"), x="count", y="issue_detail",
                         orientation="h", title="Détail des problèmes de téléphone",
                         text_auto=True)
            bph.update_traces(marker_color=AMBER)
            bph.update_yaxes(title="")
            bph.update_xaxes(title="")
            st.plotly_chart(style_fig(bph, 300), width="stretch")

        st.markdown("#### 📋 Liste opérationnelle des corrections")
        fc1, fc2 = st.columns(2)
        sev_pick = fc1.multiselect("Sévérité", SEVERITY_ORDER, default=SEVERITY_ORDER)
        type_pick = fc2.multiselect(
            "Type d'anomalie", sorted(f_issues["issue_type"].unique()),
            default=sorted(f_issues["issue_type"].unique()),
        )
        table = f_issues[
            f_issues["severity"].isin(sev_pick) & f_issues["issue_type"].isin(type_pick)
        ][["lead_id", "issue_type", "field_name", "severity",
           "recommended_action", "issue_detail"]]

        st.dataframe(table, width="stretch", height=340, hide_index=True)
        st.download_button(
            "⬇️ Télécharger la liste filtrée (CSV)",
            table.to_csv(index=False).encode("utf-8"),
            file_name="actions_correctives.csv", mime="text/csv",
        )

st.caption(
    "Source : bundle GTM relationnel · Pipeline d'audit, nettoyage et scoring qualité "
    "(notebook). Le téléphone n'est disponible qu'après conversion (≈ 73 % chez les convertis)."
)
