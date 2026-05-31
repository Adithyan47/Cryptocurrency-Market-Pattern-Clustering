"""
CryptoSeg — Cryptocurrency Market Pattern Clustering & Behavioral Segmentation
7-Tab Production Dashboard  |  Principal UI/UX + Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG — must be the very first Streamlit call
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="CryptoSeg",
    page_icon="🔮",
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
:root {
    --bg-base:#060912;--bg-card:#0f1629;--bg-card-hover:#141d35;
    --glass-bg:rgba(15,22,41,0.72);--glass-border:rgba(99,179,237,0.13);
    --glass-glow:rgba(56,189,248,0.45);
    --accent-cyan:#38bdf8;--accent-purple:#a78bfa;--accent-neon:#4ade80;
    --accent-yellow:#facc15;--accent-orange:#fb923c;--accent-pink:#f472b6;
    --accent-red:#f87171;--text-primary:#e2e8f0;--text-secondary:#94a3b8;
    --text-muted:#475569;--font-main:'Space Grotesk',sans-serif;
    --font-mono:'JetBrains Mono',monospace;--radius-card:14px;--radius-lg:18px;
}
html,body,[class*="css"]{font-family:var(--font-main)!important;background-color:var(--bg-base)!important;color:var(--text-primary)!important;}
.main .block-container{padding:1.5rem 2.5rem 3rem!important;max-width:1700px;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#08091a 0%,#0b0f22 100%)!important;border-right:1px solid var(--glass-border)!important;}
[data-testid="stSidebar"] .block-container{padding:2rem 1.25rem!important;}

/* Metric card */
.metric-card{background:var(--glass-bg);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid var(--glass-border);border-radius:var(--radius-card);padding:1.35rem 1.5rem;position:relative;overflow:hidden;transition:transform .28s cubic-bezier(.4,0,.2,1),box-shadow .28s cubic-bezier(.4,0,.2,1),border-color .28s ease;cursor:default;}
.metric-card::before{content:'';position:absolute;inset:0;border-radius:var(--radius-card);padding:1px;background:linear-gradient(135deg,rgba(56,189,248,.22),transparent 55%);-webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);-webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none;}
.metric-card:hover{transform:translateY(-4px);border-color:var(--glass-glow);box-shadow:0 0 0 1px rgba(99,179,237,.18),0 8px 32px rgba(56,189,248,.14),0 16px 48px rgba(0,0,0,.5);}
.metric-label{font-size:.68rem;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--text-muted);margin-bottom:.5rem;font-family:var(--font-mono);}
.metric-value{font-size:1.8rem;font-weight:700;letter-spacing:-.025em;line-height:1;margin-bottom:.28rem;}
.metric-sub{font-size:.73rem;color:var(--text-muted);font-family:var(--font-mono);line-height:1.4;}
.metric-positive{color:var(--accent-neon);}.metric-neutral{color:var(--accent-cyan);}
.metric-warning{color:var(--accent-yellow);}.metric-danger{color:var(--accent-orange);}

/* Screener */
.screener-card{background:var(--glass-bg);backdrop-filter:blur(12px);border:1px solid var(--glass-border);border-radius:var(--radius-card);padding:0;overflow:hidden;margin-bottom:.55rem;transition:transform .22s ease,border-color .22s ease,box-shadow .22s ease;}
.screener-card:hover{transform:translateX(4px);border-color:var(--glass-glow);box-shadow:0 4px 24px rgba(56,189,248,.1);}
.screener-row{display:flex;align-items:center;gap:.8rem;padding:.8rem 1rem;}
.screener-rank{font-size:.68rem;font-weight:700;font-family:var(--font-mono);color:var(--text-muted);min-width:20px;text-align:center;}
.screener-symbol{font-size:.85rem;font-weight:700;color:var(--text-primary);flex:1;}
.screener-value{font-size:.8rem;font-weight:600;font-family:var(--font-mono);}
.screener-accent-bar{height:3px;border-radius:0 0 var(--radius-card) var(--radius-card);}
.screener-header{background:var(--glass-bg);backdrop-filter:blur(10px);border:1px solid var(--glass-border);border-radius:var(--radius-lg);padding:1.4rem 1.5rem 1rem;margin-bottom:1rem;text-align:center;}
.screener-header-icon{font-size:2rem;margin-bottom:.4rem;}
.screener-header-title{font-size:1rem;font-weight:700;color:var(--text-primary);margin-bottom:.3rem;}
.screener-header-sub{font-size:.72rem;color:var(--text-muted);font-family:var(--font-mono);}

/* Tribe card */
.tribe-card{background:var(--glass-bg);backdrop-filter:blur(12px);border:1px solid var(--glass-border);border-radius:var(--radius-lg);padding:1.5rem;margin-bottom:.5rem;transition:all .25s ease;}
.tribe-card:hover{border-color:var(--glass-glow);box-shadow:0 4px 24px rgba(56,189,248,.08);transform:translateY(-2px);}
.tribe-header{display:flex;align-items:center;gap:.75rem;margin-bottom:1.2rem;}
.tribe-badge{font-size:1.4rem;}.tribe-title{font-size:1.05rem;font-weight:700;color:var(--text-primary);}
.tribe-count{font-size:.72rem;color:var(--text-muted);font-family:var(--font-mono);margin-top:.1rem;}
.tribe-stat-row{display:flex;justify-content:space-between;align-items:center;padding:.45rem 0;border-bottom:1px solid rgba(255,255,255,.04);}
.tribe-stat-row:last-child{border-bottom:none;}
.tribe-stat-key{font-size:.78rem;color:var(--text-secondary);font-family:var(--font-mono);}
.tribe-stat-val{font-size:.85rem;font-weight:600;font-family:var(--font-mono);}

/* Consensus */
.consensus-card{background:var(--glass-bg);backdrop-filter:blur(12px);border:1px solid var(--glass-border);border-radius:var(--radius-card);padding:1.2rem 1.4rem;text-align:center;transition:all .25s ease;}
.consensus-card:hover{border-color:var(--glass-glow);box-shadow:0 0 20px rgba(56,189,248,.1);}
.consensus-model{font-size:.68rem;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);font-family:var(--font-mono);margin-bottom:.6rem;}
.consensus-cluster{font-size:2.2rem;font-weight:700;letter-spacing:-.03em;line-height:1;margin-bottom:.4rem;}
.consensus-label{font-size:.7rem;color:var(--text-muted);font-family:var(--font-mono);}

/* Anomaly */
.anomaly-card{background:linear-gradient(135deg,rgba(248,113,113,.07) 0%,rgba(15,22,41,.9) 60%);backdrop-filter:blur(14px);border:1px solid rgba(248,113,113,.28);border-radius:var(--radius-lg);padding:1.6rem;position:relative;overflow:hidden;transition:all .28s ease;}
.anomaly-card:hover{border-color:rgba(248,113,113,.55);box-shadow:0 0 32px rgba(248,113,113,.12),0 8px 32px rgba(0,0,0,.4);transform:translateY(-3px);}
.anomaly-label{font-size:.68rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:rgba(248,113,113,.7);font-family:var(--font-mono);margin-bottom:.45rem;}
.anomaly-value{font-size:1.7rem;font-weight:700;color:#f87171;letter-spacing:-.02em;line-height:1;margin-bottom:.25rem;}
.anomaly-sub{font-size:.72rem;color:var(--text-muted);font-family:var(--font-mono);}

/* Info box */
.info-box{background:linear-gradient(135deg,rgba(56,189,248,.05) 0%,rgba(167,139,250,.05) 100%);border:1px solid rgba(56,189,248,.18);border-radius:var(--radius-card);padding:.9rem 1.3rem;margin-bottom:1.2rem;font-size:.865rem;color:var(--text-secondary);line-height:1.65;}
.info-box strong{color:var(--accent-cyan);font-weight:600;}
.info-box.warn{background:linear-gradient(135deg,rgba(251,146,60,.06) 0%,rgba(15,22,41,.9) 100%);border-color:rgba(251,146,60,.22);}
.info-box.warn strong{color:var(--accent-orange);}
.info-box.success{background:linear-gradient(135deg,rgba(74,222,128,.06) 0%,rgba(15,22,41,.9) 100%);border-color:rgba(74,222,128,.22);}
.info-box.success strong{color:var(--accent-neon);}

/* Page title */
.page-title{font-size:2.4rem;font-weight:700;letter-spacing:-.03em;background:linear-gradient(135deg,#e2e8f0 0%,#38bdf8 50%,#a78bfa 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.15;margin-bottom:.4rem;}
.page-subtitle{font-size:.88rem;color:var(--text-muted);font-family:var(--font-mono);letter-spacing:.04em;margin-bottom:2rem;}

/* Section heading */
.section-heading{font-size:1.05rem;font-weight:700;color:var(--text-primary);letter-spacing:-.01em;margin:1.2rem 0 1rem;display:flex;align-items:center;gap:.5rem;}
.section-heading::after{content:'';flex:1;height:1px;background:var(--glass-border);margin-left:.75rem;}

/* Sidebar stat */
.sidebar-stat{background:rgba(56,189,248,.07);border:1px solid rgba(56,189,248,.15);border-radius:10px;padding:.8rem 1rem;text-align:center;margin-bottom:.55rem;}
.sidebar-stat-label{font-size:.63rem;letter-spacing:.12em;text-transform:uppercase;color:var(--text-muted);font-family:var(--font-mono);margin-bottom:.25rem;}
.sidebar-stat-value{font-size:1.55rem;font-weight:700;color:var(--accent-cyan);line-height:1;}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:transparent!important;border-bottom:1px solid var(--glass-border)!important;gap:0!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--text-muted)!important;border:none!important;padding:.6rem 1.35rem!important;font-family:var(--font-main)!important;font-weight:500!important;font-size:.87rem!important;letter-spacing:.01em!important;transition:color .2s ease!important;}
.stTabs [data-baseweb="tab"]:hover{color:var(--text-primary)!important;background:rgba(56,189,248,.04)!important;}
.stTabs [aria-selected="true"]{color:var(--accent-cyan)!important;border-bottom:2px solid var(--accent-cyan)!important;background:transparent!important;}

/* Selectbox */
.stSelectbox>div>div{background:var(--bg-card)!important;border:1px solid var(--glass-border)!important;border-radius:10px!important;color:var(--text-primary)!important;font-family:var(--font-main)!important;}
.stSelectbox>div>div:focus-within{border-color:var(--glass-glow)!important;box-shadow:0 0 0 3px rgba(56,189,248,.1)!important;}

/* Radio */
.stRadio>div{gap:.4rem!important;}
.stRadio [data-testid="stMarkdownContainer"] p{font-size:.875rem!important;color:var(--text-secondary)!important;}

/* Dataframe */
.stDataFrame{border:1px solid var(--glass-border)!important;border-radius:var(--radius-card)!important;overflow:hidden!important;}

/* Scrollbar */
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:var(--text-muted);border-radius:3px;}
::-webkit-scrollbar-thumb:hover{background:var(--accent-cyan);}

/* Hide chrome */
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/backend_processed_clusters.csv")
    df["RAR"] = df["Mean_Return"] / df["Volatility"]
    return df

df = load_data()


# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
MODEL_MAP = {
    "K-Means":      "KMeans_Cluster",
    "Hierarchical": "Hierarchical_Cluster",
    "DBSCAN":       "DBSCAN_Cluster",
    "GMM":          "GMM_Cluster",
}
MODEL_DESC = {
    "K-Means":      "Partitions assets into a fixed number of equal-sized groups. Fast and intuitive — great for finding broad market segments.",
    "Hierarchical": "Builds a tree of nested groups by merging similar assets step by step. Reveals natural sub-structures in the market.",
    "DBSCAN":       "Finds dense pockets of similar assets and flags outliers as 'noise'. Excellent at spotting unusual or uncategorised coins.",
    "GMM":          "Assigns each asset a probability of belonging to each group. More flexible than K-Means — handles overlapping behaviours.",
}
CLUSTER_COLORS = {-1:"#475569", 0:"#4ade80", 1:"#38bdf8", 2:"#a78bfa", 3:"#facc15", 4:"#fb923c"}
TRIBE_BADGES   = {-1:"⚫", 0:"🟢", 1:"🔵", 2:"🟣", 3:"🟡", 4:"🟠"}
TRIBE_LABELS   = {-1:"Outlier / Noise", 0:"Tribe Alpha", 1:"Tribe Beta",
                   2:"Tribe Gamma",      3:"Tribe Delta", 4:"Tribe Epsilon"}
NEON_SEQ = ["#38bdf8","#a78bfa","#f472b6","#4ade80","#facc15","#fb923c"]

def LAYOUT(**kwargs):
    """Safe layout builder — pass any kwargs, no duplicate keyword errors possible."""
    d = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk, sans-serif", color="#94a3b8", size=11),
        hoverlabel=dict(bgcolor="#0d1220", bordercolor="#38bdf8",
                        font=dict(family="JetBrains Mono, monospace", size=11, color="#e2e8f0")),
    )
    d.update(kwargs)
    return d

# Keep alias so any remaining **PLOTLY_LAYOUT_BASE spreads work (no margin/legend in it)
PLOTLY_LAYOUT_BASE = LAYOUT()

def legend_cfg(**kwargs):
    base = dict(bgcolor="rgba(13,18,32,0.85)", bordercolor="rgba(99,179,237,0.18)",
                borderwidth=1, font=dict(size=10, color="#e2e8f0"))
    base.update(kwargs)
    return base


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt_pct(v, d=3):   return f"{v*100:.{d}f}%"
def fmt_f(v, d=4):     return f"{v:.{d}f}"
def ccolor(cid):       return CLUSTER_COLORS.get(cid, "#94a3b8")
def tbadge(cid):       return TRIBE_BADGES.get(cid, "⚪")
def return_cc(v):      return "metric-positive" if v>=0.002 else ("metric-neutral" if v>=0.001 else "metric-warning")
def vol_cc(v):         return "metric-danger" if v>=0.07 else ("metric-warning" if v>=0.055 else "metric-positive")
def mom_cc(v):         return "metric-positive" if v>0.05 else ("metric-danger" if v<-0.05 else "metric-neutral")

def metric_card(label, value, sub="", cc="metric-neutral"):
    sub_h = f'<div class="metric-sub">{sub}</div>' if sub else ""
    return (f'<div class="metric-card"><div class="metric-label">{label}</div>'
            f'<div class="metric-value {cc}">{value}</div>{sub_h}</div>')

def axis_cfg(title_text):
    return dict(title=dict(text=title_text, font=dict(size=10, color="#64748b")),
                gridcolor="rgba(255,255,255,0.05)", zeroline=True,
                zerolinecolor="rgba(56,189,248,0.14)", zerolinewidth=1,
                tickfont=dict(size=9, color="#475569"))


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:1.8rem;'>
        <div style='font-size:1.5rem;font-weight:800;letter-spacing:-.02em;
             background:linear-gradient(135deg,#38bdf8,#a78bfa);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             background-clip:text;'>🔮 CryptoSeg</div>
        <div style='font-size:.65rem;color:#475569;font-family:"JetBrains Mono",monospace;
             letter-spacing:.08em;margin-top:.2rem;'>MARKET INTELLIGENCE PLATFORM</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='font-size:.68rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;"
                "color:#475569;font-family:\"JetBrains Mono\",monospace;margin-bottom:.6rem;'>Clustering Model</div>",
                unsafe_allow_html=True)

    selected_model = st.radio("model_selector", list(MODEL_MAP.keys()), index=0,
                               key="model", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="info-box" style="font-size:.78rem;"><strong>{selected_model}</strong>'
                f'<br>{MODEL_DESC[selected_model]}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:.68rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;"
                "color:#475569;font-family:\"JetBrains Mono\",monospace;margin-bottom:.6rem;'>Universe Stats</div>",
                unsafe_allow_html=True)

    acol      = MODEL_MAP[selected_model]
    n_clusters = df[acol].nunique()
    n_noise    = int((df["DBSCAN_Cluster"] == -1).sum())

    for lbl, val, extra in [
        ("Total Assets",    str(len(df)),                            ""),
        ("Segments Found",  str(n_clusters),                        ""),
        ("Avg Return",      fmt_pct(df["Mean_Return"].mean(), 2),   ""),
        ("Avg Volatility",  fmt_f(df["Volatility"].mean(), 4),      ""),
        ("DBSCAN Outliers", str(n_noise), "border-color:rgba(251,146,60,.3);"),
    ]:
        vc = "color:#fb923c;" if lbl == "DBSCAN Outliers" else ""
        st.markdown(f'<div class="sidebar-stat" style="{extra}"><div class="sidebar-stat-label">{lbl}</div>'
                    f'<div class="sidebar-stat-value" style="{vc}">{val}</div></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-title">Cryptocurrency Market<br>Pattern Intelligence</div>
<div class="page-subtitle">// BEHAVIORAL SEGMENTATION · 100 ASSETS · ML-POWERED CLUSTERING</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🗺️  Market Segments",
    "🧬  Tribe Profiles",
    "🔭  Asset Deep-Dive",
    "🏆  Smart Screeners",
    "🌐  3D Topography",
    "🚨  Anomaly Radar",
    "🔬  Correlation Matrix",
])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — MARKET SEGMENTS
# ═════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("""<div class="info-box"><strong>How to read this map:</strong> Each dot is one
    cryptocurrency. Our ML algorithms grouped 100 assets into <em>Tribes</em> by colour.
    Coins <strong>close together</strong> behave similarly; coins far apart are fundamentally
    different in their market patterns. Switch models in the sidebar for four algorithmic perspectives.
    </div>""", unsafe_allow_html=True)

    acol        = MODEL_MAP[selected_model]
    cluster_ids = sorted(df[acol].unique())
    tcmap       = {("Outlier" if c==-1 else f"Tribe {c}"): ccolor(c) for c in cluster_ids}

    pdf = df.copy()
    pdf["Tribe"]      = pdf[acol].apply(lambda x: "Outlier" if x==-1 else f"Tribe {x}")
    pdf["Return (%)"] = (pdf["Mean_Return"]*100).round(3).astype(str)+"%"
    pdf["Vol."]       = pdf["Volatility"].round(5)
    pdf["Mom."]       = pdf["Momentum"].round(4)

    fig = px.scatter(pdf, x="PCA1", y="PCA2", color="Tribe", color_discrete_map=tcmap,
                     hover_name="symbol",
                     hover_data={"Return (%)":True,"Vol.":True,"Mom.":True,
                                 "PCA1":False,"PCA2":False,"Tribe":False},
                     labels={"PCA1":"Overall Market Trend →","PCA2":"Risk / Volatility Profile →"},
                     template="plotly_dark")
    fig.update_traces(
        marker=dict(size=10, opacity=0.88, line=dict(width=0.8, color="rgba(255,255,255,0.12)")),
        hovertemplate=("<b style='font-size:13px'>%{hovertext}</b><br>"
                       "<span style='color:#475569'>──────────────────</span><br>"
                       "Return:     <b>%{customdata[0]}</b><br>"
                       "Volatility: <b>%{customdata[1]}</b><br>"
                       "Momentum:   <b>%{customdata[2]}</b><extra></extra>"))
    fig.update_layout(**LAYOUT(
                      height=560, margin=dict(l=40,r=30,t=30,b=50),
                      xaxis=axis_cfg("Overall Market Trend →"),
                      yaxis=axis_cfg("Risk / Volatility Profile →"),
                      legend=legend_cfg(title=dict(text="Market Tribes", font=dict(size=10)))))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("<hr>", unsafe_allow_html=True)

    scols = st.columns(min(len(cluster_ids), 5))
    for i, cid in enumerate(cluster_ids):
        sub = df[df[acol]==cid]
        with scols[i % len(scols)]:
            st.markdown(f'<div class="metric-card" style="border-left:3px solid {ccolor(cid)};">'
                        f'<div class="metric-label">{tbadge(cid)} {"Outlier" if cid==-1 else f"Tribe {cid}"}</div>'
                        f'<div class="metric-value" style="font-size:1.4rem;color:{ccolor(cid)};">{len(sub)} assets</div>'
                        f'<div class="metric-sub">avg return {fmt_pct(sub["Mean_Return"].mean())}</div></div>',
                        unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — TRIBE PROFILES
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    acol        = MODEL_MAP[selected_model]
    cluster_ids = sorted(df[acol].unique())

    st.markdown("""<div class="info-box"><strong>Tribe Profiles</strong> reveal the average financial
    personality of each cluster. Think of each tribe as a <em>character archetype</em>: high-return
    &amp; high-volatility tribes contain aggressive growth coins; low-volatility tribes hold steadier,
    defensive assets.</div>""", unsafe_allow_html=True)

    metrics  = ["Mean_Return","Volatility","Momentum"]
    rdf      = df.groupby(acol)[metrics].mean().reset_index()
    for m in metrics:
        mn,mx = rdf[m].min(), rdf[m].max()
        rdf[m+"_n"] = (rdf[m]-mn)/(mx-mn+1e-9)

    bar_fig = go.Figure()
    for _, row in rdf.iterrows():
        cid = int(row[acol])
        lbl = "Outlier" if cid==-1 else f"Tribe {cid}"
        bar_fig.add_trace(go.Bar(name=lbl, x=["Avg Return","Volatility","Momentum"],
                                  y=[row["Mean_Return_n"],row["Volatility_n"],row["Momentum_n"]],
                                  marker_color=ccolor(cid), opacity=0.87))
    bar_fig.update_layout(**LAYOUT(
                           barmode="group", height=310, margin=dict(l=40,r=30,t=30,b=50),
                           xaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(size=10)),
                           yaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(size=9),
                                      title=dict(text="Relative Score (normalised 0→1)",font=dict(size=9,color="#475569")))))
    st.markdown('<div class="section-heading">📊 Side-by-Side Comparison</div>', unsafe_allow_html=True)
    st.plotly_chart(bar_fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-heading">🧬 Individual Tribe Breakdown</div>', unsafe_allow_html=True)
    nc = min(len(cluster_ids),3)
    col_sets = [st.columns(nc) for _ in range((len(cluster_ids)+nc-1)//nc)]
    gm = df["Mean_Return"].mean()

    for idx, cid in enumerate(cluster_ids):
        sub      = df[df[acol]==cid]
        color    = ccolor(cid)
        label    = "Outlier / Noise" if cid==-1 else f"Tribe {cid}"
        avg_ret  = sub["Mean_Return"].mean()
        avg_vol  = sub["Volatility"].mean()
        avg_mom  = sub["Momentum"].mean()
        top_coin = sub.loc[sub["Mean_Return"].idxmax(),"symbol"]
        with col_sets[idx//nc][idx%nc]:
            st.markdown(f"""<div class="tribe-card" style="border-top:3px solid {color};">
                <div class="tribe-header">
                    <span class="tribe-badge">{tbadge(cid)}</span>
                    <div><div class="tribe-title">{label}</div>
                    <div class="tribe-count">{len(sub)} assets</div></div>
                </div>
                <div class="tribe-stat-row"><span class="tribe-stat-key">AVG RETURN</span>
                    <span class="tribe-stat-val" style="color:{color};">{fmt_pct(avg_ret)} {"↑" if avg_ret>=gm else "↓"}</span></div>
                <div class="tribe-stat-row"><span class="tribe-stat-key">AVG VOLATILITY</span>
                    <span class="tribe-stat-val" style="color:#facc15;">{fmt_f(avg_vol)}</span></div>
                <div class="tribe-stat-row"><span class="tribe-stat-key">AVG MOMENTUM</span>
                    <span class="tribe-stat-val" style="color:#a78bfa;">{fmt_f(avg_mom)} {"↑" if avg_mom>0 else "↓"}</span></div>
                <div class="tribe-stat-row"><span class="tribe-stat-key">TOP PERFORMER</span>
                    <span class="tribe-stat-val" style="color:#38bdf8;">{top_coin}</span></div>
            </div>""", unsafe_allow_html=True)

    with st.expander("📋 View Full Data Table", expanded=False):
        ddf = df[["symbol",acol,"Mean_Return","Volatility","Momentum"]].copy()
        ddf.columns = ["Symbol","Tribe","Return","Volatility","Momentum"]
        ddf["Return"]    = ddf["Return"].apply(fmt_pct)
        ddf["Tribe"]     = ddf["Tribe"].apply(lambda x: "Outlier" if x==-1 else f"Tribe {x}")
        ddf["Volatility"]= ddf["Volatility"].round(5)
        ddf["Momentum"]  = ddf["Momentum"].round(4)
        st.dataframe(ddf.sort_values("Tribe"), use_container_width=True, hide_index=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — ASSET DEEP-DIVE
# ═════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""<div class="info-box"><strong>Asset Deep-Dive</strong> lets you inspect any coin
    in detail. Select an asset to see its financial profile and compare how all four algorithms
    classified it. Universal agreement signals a clear behavioural archetype; disagreement means
    the coin bridges multiple market patterns.</div>""", unsafe_allow_html=True)

    sym_list = sorted(df["symbol"].tolist())
    def_idx  = sym_list.index("BTCUSDT") if "BTCUSDT" in sym_list else 0
    sel_sym  = st.selectbox("Select Asset", sym_list, index=def_idx, label_visibility="collapsed")
    row      = df[df["symbol"]==sel_sym].iloc[0]

    st.markdown(f'<div class="section-heading">📈 Financial Snapshot — {sel_sym}</div>', unsafe_allow_html=True)
    mc1,mc2,mc3 = st.columns(3)
    with mc1:
        st.markdown(metric_card("Average Daily Return", fmt_pct(row["Mean_Return"]),
                    "Higher = more growth on average", return_cc(row["Mean_Return"])), unsafe_allow_html=True)
    with mc2:
        st.markdown(metric_card("Price Volatility", fmt_f(row["Volatility"]),
                    "How wildly the price swings day-to-day", vol_cc(row["Volatility"])), unsafe_allow_html=True)
    with mc3:
        dtxt = "Upward trend 🚀" if row["Momentum"]>0.01 else ("Downward trend 📉" if row["Momentum"]<-0.01 else "Neutral / sideways")
        st.markdown(metric_card("Price Momentum", fmt_f(row["Momentum"],4), dtxt, mom_cc(row["Momentum"])), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    p1,p2 = st.columns(2)
    with p1:
        st.markdown(metric_card("Overall Market Trend (PCA1)", fmt_f(row["PCA1"],4),
                    "Position on the broad market axis","metric-neutral"), unsafe_allow_html=True)
    with p2:
        st.markdown(metric_card("Risk / Volatility Profile (PCA2)", fmt_f(row["PCA2"],4),
                    "Position on the risk/volatility axis","metric-warning"), unsafe_allow_html=True)

    st.markdown('<div class="section-heading">🤖 Model Consensus</div>', unsafe_allow_html=True)
    con_cols  = st.columns(4)
    model_cids = {}
    for i,(mname,mcol) in enumerate(MODEL_MAP.items()):
        cid   = int(row[mcol]); label = "Outlier" if cid==-1 else f"Tribe {cid}"
        color = ccolor(cid); model_cids[mname] = cid
        with con_cols[i]:
            st.markdown(f"""<div class="consensus-card" style="border-top:3px solid {color};">
                <div class="consensus-model">{mname}</div>
                <div class="consensus-cluster" style="color:{color};">{"−1" if cid==-1 else str(cid)}</div>
                <div class="consensus-label">{label}</div></div>""", unsafe_allow_html=True)

    cid_vals  = list(model_cids.values())
    non_noise = [v for v in cid_vals if v!=-1]
    if len(set(cid_vals))==1:
        vcls="success"; icon="✅"
        vtxt=f'<strong>Strong Consensus:</strong> All four algorithms agree — <strong>{sel_sym}</strong> is a textbook member of <strong>{"Outlier" if cid_vals[0]==-1 else f"Tribe {cid_vals[0]}"}</strong>.'
    elif len(set(non_noise))==1 and len(non_noise)>=3:
        vcls="warn"; icon="⚠️"
        vtxt=f'<strong>Partial Consensus:</strong> Most models agree on <strong>{sel_sym}</strong>. One model differs — it may sit on the boundary of two tribes.'
    else:
        vcls="warn"; icon="🔀"
        vtxt=f'<strong>Mixed Signals:</strong> The algorithms disagree on <strong>{sel_sym}</strong>. This coin likely exhibits hybrid trading behaviour bridging multiple patterns.'
    st.markdown(f'<div class="info-box {vcls}" style="margin-top:.8rem;">{icon} {vtxt}</div>', unsafe_allow_html=True)

    if "GMM_Max_Prob" in df.columns:
        gp = float(row["GMM_Max_Prob"]); bw = int(gp*100)
        bc = "#4ade80" if gp>0.9 else ("#facc15" if gp>0.7 else "#fb923c")
        ct = ("Very high confidence — textbook tribe member." if gp>0.95
              else "Moderate confidence — some overlap with neighbours." if gp>0.75
              else "Low confidence — straddles multiple behavioural groups.")
        st.markdown('<div class="section-heading">🎲 GMM Cluster Confidence</div>', unsafe_allow_html=True)
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Probability of Belonging to Assigned GMM Tribe</div>
            <div style="display:flex;align-items:center;gap:1.2rem;margin-top:.5rem;">
                <div style="flex:1;background:rgba(255,255,255,.06);border-radius:100px;height:10px;overflow:hidden;">
                    <div style="width:{bw}%;height:100%;background:{bc};border-radius:100px;"></div></div>
                <div style="font-size:1.4rem;font-weight:700;color:{bc};font-family:'JetBrains Mono',monospace;">{gp:.1%}</div>
            </div><div class="metric-sub" style="margin-top:.6rem;">{ct}</div></div>""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — SMART SCREENERS
# ═════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""<div class="info-box"><strong>Smart Screeners</strong> apply three
    institutional-grade filters to surface the most compelling coins in the universe.
    Each leaderboard ranks all 100 assets by a specific investment objective.
    These are <em>data-driven</em> rankings — not financial advice.</div>""", unsafe_allow_html=True)

    safe_df  = df[df["Mean_Return"]>0].sort_values("Volatility").head(10).reset_index(drop=True)
    trend_df = df.sort_values("Momentum",ascending=False).head(10).reset_index(drop=True)
    smart_df = df.sort_values("RAR",ascending=False).head(10).reset_index(drop=True)

    sc1,sc2,sc3 = st.columns(3)
    rank_colors = ["#facc15","#94a3b8","#fb923c"]

    def render_screener(col, title, icon, accent, desc, math_note, data, val_col, val_fn):
        with col:
            st.markdown(f"""<div class="screener-header" style="border-top:3px solid {accent};">
                <div class="screener-header-icon">{icon}</div>
                <div class="screener-header-title">{title}</div>
                <div class="screener-header-sub">{math_note}</div></div>""", unsafe_allow_html=True)
            st.markdown(f'<div class="info-box" style="font-size:.8rem;margin-bottom:.85rem;">{desc}</div>', unsafe_allow_html=True)
            for i,(_,r) in enumerate(data.iterrows()):
                rc  = rank_colors[i] if i<3 else "#475569"
                sym = r["symbol"].replace("USDT","")
                st.markdown(f"""<div class="screener-card">
                    <div class="screener-row">
                        <div class="screener-rank" style="color:{rc};">#{i+1}</div>
                        <div class="screener-symbol">{sym}</div>
                        <div class="screener-value" style="color:{accent};">{val_fn(r[val_col])}</div>
                    </div>
                    <div class="screener-accent-bar" style="background:linear-gradient(90deg,{accent}55,transparent);opacity:{max(0.15,1-i*0.09):.2f};"></div>
                </div>""", unsafe_allow_html=True)

    render_screener(sc1,"Safe Haven Assets","🛡️","#4ade80",
        "<strong>Lowest-risk growth coins.</strong> Filtered to positive-return assets ranked by "
        "<em>smallest price swings</em>. Slow, steady, and resilient.",
        "filter: Return > 0  ·  sort: Volatility ↑",
        safe_df,"Volatility",lambda v: fmt_f(v,5))

    render_screener(sc2,"Trending Breakouts","🚀","#38bdf8",
        "<strong>Strongest price momentum.</strong> Ranked by how powerfully each coin is trending. "
        "High momentum = active buying pressure and accelerating price.",
        "sort: Momentum ↓",
        trend_df,"Momentum",lambda v: fmt_f(v,4))

    render_screener(sc3,"Smart Money Picks","🧠","#a78bfa",
        "<strong>Best return per unit of risk.</strong> Risk-Adjusted Return (Return ÷ Volatility) "
        "rewards coins that grow strongly <em>without</em> wild price swings.",
        "sort: Mean_Return ÷ Volatility ↓",
        smart_df,"RAR",lambda v: f"{v:.5f}")

    # Risk vs Return scatter
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📊 Risk vs Return Landscape</div>', unsafe_allow_html=True)
    st.markdown("""<div class="info-box" style="margin-bottom:.9rem;">
        The ideal coin sits <strong>top-left</strong>: high return, low risk. Bubble size encodes the
        <strong>Risk-Adjusted Return</strong> score. Gold stars = <strong>Top 5 Smart Money Picks</strong>.
    </div>""", unsafe_allow_html=True)

    rv_df          = df.copy()
    rv_df["RAR_n"] = (rv_df["RAR"]-rv_df["RAR"].min())/(rv_df["RAR"].max()-rv_df["RAR"].min()+1e-9)
    rv_df["Bubble"]= 6+rv_df["RAR_n"]*28
    rv_df["Top5"]  = rv_df["symbol"].isin(smart_df.head(5)["symbol"])
    acolrv         = MODEL_MAP[selected_model]
    rv_df["Tribe"] = rv_df[acolrv].apply(lambda x: "Outlier" if x==-1 else f"Tribe {x}")
    tcmaprv        = {("Outlier" if c==-1 else f"Tribe {c}"): ccolor(c) for c in sorted(rv_df[acolrv].unique())}

    rvfig = px.scatter(rv_df, x="Volatility", y="Mean_Return", size="Bubble", color="Tribe",
                       color_discrete_map=tcmaprv, hover_name="symbol",
                       hover_data={"Volatility":":.5f","Mean_Return":":.5f","RAR":":.5f",
                                   "Bubble":False,"Top5":False,"Tribe":False},
                       template="plotly_dark",
                       labels={"Volatility":"Price Volatility (Risk) →","Mean_Return":"Avg Daily Return →"})
    rvfig.update_layout(**LAYOUT(
                        height=420, margin=dict(l=40,r=30,t=30,b=50),
                        xaxis=axis_cfg("Price Volatility (Risk) →"),
                        yaxis=axis_cfg("Avg Daily Return →")))
    t5 = rv_df[rv_df["Top5"]]
    rvfig.add_trace(go.Scatter(x=t5["Volatility"],y=t5["Mean_Return"],mode="markers+text",
                               marker=dict(symbol="star",size=18,color="#facc15",line=dict(width=1.5,color="#fff")),
                               text=t5["symbol"].str.replace("USDT",""),
                               textposition="top center",
                               textfont=dict(size=9,color="#facc15",family="JetBrains Mono"),
                               name="Top 5 Smart Picks",showlegend=True))
    st.plotly_chart(rvfig, use_container_width=True, config={"displayModeBar": False})


# ═════════════════════════════════════════════════════════════════════════════
# TAB 5 — 3D TOPOGRAPHY
# ═════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("""<div class="info-box"><strong>3D Market Topography</strong> adds a third
    dimension — <em>Volatility</em> — to the cluster map. Drag to rotate, scroll to zoom.
    Peaks = high-risk assets; valleys = calmer coins. Colour = tribe under the active model.</div>""",
    unsafe_allow_html=True)

    acol3d      = MODEL_MAP[selected_model]
    cids3d      = sorted(df[acol3d].unique())
    tcmap3d     = {("Outlier" if c==-1 else f"Tribe {c}"): NEON_SEQ[i%len(NEON_SEQ)] for i,c in enumerate(cids3d)}
    df3d        = df.copy()
    df3d["Tribe"]  = df3d[acol3d].apply(lambda x: "Outlier" if x==-1 else f"Tribe {x}")
    df3d["Ret%"]   = (df3d["Mean_Return"]*100).round(3)

    fig3d = px.scatter_3d(df3d, x="PCA1", y="PCA2", z="Volatility", color="Tribe",
                          color_discrete_map=tcmap3d, hover_name="symbol",
                          hover_data={"Ret%":True,"Volatility":":.5f","Momentum":":.4f",
                                      "PCA1":":.3f","PCA2":":.3f","Tribe":False},
                          labels={"PCA1":"Overall Market Trend","PCA2":"Risk / Vol Profile","Volatility":"Volatility (Height)"},
                          template="plotly_dark", opacity=0.88)
    fig3d.update_traces(marker=dict(size=5.5,line=dict(width=0.4,color="rgba(255,255,255,0.15)")))

    ax3d = dict(backgroundcolor="rgba(0,0,0,0)",gridcolor="rgba(255,255,255,0.06)",
                showbackground=True,zerolinecolor="rgba(56,189,248,0.2)",
                tickfont=dict(size=8,color="#475569"))

    fig3d.update_layout(**LAYOUT(
                        height=640, margin=dict(l=0,r=0,t=30,b=0),
                        scene=dict(
                            xaxis=dict(**ax3d,title=dict(text="Overall Market Trend",font=dict(size=10,color="#64748b"))),
                            yaxis=dict(**ax3d,title=dict(text="Risk / Vol Profile",  font=dict(size=10,color="#64748b"))),
                            zaxis=dict(**ax3d,title=dict(text="Volatility (Height)", font=dict(size=10,color="#64748b"))),
                            bgcolor="rgba(0,0,0,0)",
                            camera=dict(eye=dict(x=1.6,y=1.6,z=0.9))),
                        legend=legend_cfg(title=dict(text="Market Tribes",font=dict(size=10)))))
    st.plotly_chart(fig3d, use_container_width=True, config={"displayModeBar": True})
    st.markdown("""<div class="info-box" style="margin-top:.5rem;">
        💡 <strong>Tip:</strong> Click and drag to orbit · Scroll to zoom · Double-click to reset camera.
        Use the legend to isolate individual tribes.</div>""", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📐 Dimensional Breakdown by Tribe</div>', unsafe_allow_html=True)
    dcols = st.columns(min(len(cids3d),5))
    for i,cid in enumerate(cids3d):
        sub   = df[df[acol3d]==cid]
        color = NEON_SEQ[i%len(NEON_SEQ)]
        with dcols[i%len(dcols)]:
            st.markdown(f'<div class="metric-card" style="border-left:3px solid {color};">'
                        f'<div class="metric-label">{"Outlier" if cid==-1 else f"Tribe {cid}"} · {len(sub)} coins</div>'
                        f'<div class="metric-value" style="font-size:1.1rem;color:{color};">Vol {fmt_f(sub["Volatility"].mean(),4)}</div>'
                        f'<div class="metric-sub">PCA1 avg {fmt_f(sub["PCA1"].mean(),3)} · PCA2 avg {fmt_f(sub["PCA2"].mean(),3)}</div></div>',
                        unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 6 — ANOMALY & WHALE RADAR
# ═════════════════════════════════════════════════════════════════════════════
with tab6:
    outlier_df  = df[df["DBSCAN_Cluster"]==-1].copy()
    normal_df   = df[df["DBSCAN_Cluster"]!=-1].copy()
    g_means     = df[["Mean_Return","Volatility","Momentum"]].mean()

    st.markdown(f"""<div class="info-box warn"><strong>Anomaly &amp; Whale Radar</strong> isolates
    coins that DBSCAN could <em>not</em> assign to any tribe — assets whose trading behaviour is
    so extreme that no cluster could contain them. We detected
    <strong>{len(outlier_df)} Black Swan asset{"s" if len(outlier_df)!=1 else ""}</strong>.</div>""",
    unsafe_allow_html=True)

    if len(outlier_df)==0:
        st.markdown("""<div class="info-box success">✅ <strong>No anomalies detected.</strong>
        Every asset was successfully assigned to a DBSCAN cluster. The market is behaving in a
        coherent, structured fashion.</div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="section-heading">🚨 Black Swan Assets</div>', unsafe_allow_html=True)
        for _,orow in outlier_df.iterrows():
            d_ret = orow["Mean_Return"]-g_means["Mean_Return"]
            d_vol = orow["Volatility"] -g_means["Volatility"]
            d_mom = orow["Momentum"]   -g_means["Momentum"]
            sr,sv,sm = ("+" if d_ret>=0 else ""),("+" if d_vol>=0 else ""),("+" if d_mom>=0 else "")
            c1,c2,c3,c4 = st.columns(4)
            with c1:
                st.markdown(f'<div class="anomaly-card"><div class="anomaly-label">🪙 Asset</div>'
                            f'<div class="anomaly-value" style="font-size:1.5rem;">{orow["symbol"]}</div>'
                            f'<div class="anomaly-sub">DBSCAN Cluster = −1 (Outlier)</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="anomaly-card"><div class="anomaly-label">📈 Avg Return</div>'
                            f'<div class="anomaly-value">{fmt_pct(orow["Mean_Return"])}</div>'
                            f'<div class="anomaly-sub">vs market {sr}{fmt_pct(d_ret)} deviation</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="anomaly-card"><div class="anomaly-label">⚡ Volatility</div>'
                            f'<div class="anomaly-value">{fmt_f(orow["Volatility"])}</div>'
                            f'<div class="anomaly-sub">vs market {sv}{fmt_f(d_vol)} deviation</div></div>', unsafe_allow_html=True)
            with c4:
                st.markdown(f'<div class="anomaly-card"><div class="anomaly-label">🏹 Momentum</div>'
                            f'<div class="anomaly-value">{fmt_f(orow["Momentum"],4)}</div>'
                            f'<div class="anomaly-sub">vs market {sm}{fmt_f(d_mom,4)} deviation</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-heading">🕸️ Behaviour Radar vs Market Average</div>', unsafe_allow_html=True)
        st.markdown("""<div class="info-box warn">The radar compares outlier(s) (red) vs the
        <strong>global market average</strong> (cyan). Where red spikes beyond cyan, the anomaly is
        dramatically more extreme. All values normalised 0–1 for fair comparison.</div>""", unsafe_allow_html=True)

        rcols        = ["Mean_Return","Volatility","Momentum","PCA1","PCA2"]
        rnames       = ["Avg Return","Volatility","Momentum","Market Trend","Risk Profile"]
        g_minr       = df[rcols].min()
        g_maxr       = df[rcols].max()
        g_means_full = df[rcols].mean()
        gnorm        = lambda col: float((g_means_full[col]-g_minr[col])/(g_maxr[col]-g_minr[col]+1e-9))
        onorm        = lambda row,col: float((row[col]-g_minr[col])/(g_maxr[col]-g_minr[col]+1e-9))

        gv = [gnorm(c) for c in rcols]
        radar_fig = go.Figure()
        radar_fig.add_trace(go.Scatterpolar(r=gv+[gv[0]],theta=rnames+[rnames[0]],
                                             fill="toself",name="Market Average",
                                             line=dict(color="#38bdf8",width=2),
                                             fillcolor="rgba(56,189,248,0.12)"))
        oclrs = ["#f87171","#fb923c","#f472b6"]
        for oi,(_,orow) in enumerate(outlier_df.iterrows()):
            ov = [onorm(orow,c) for c in rcols]
            oc = oclrs[oi%len(oclrs)]
            radar_fig.add_trace(go.Scatterpolar(r=ov+[ov[0]],theta=rnames+[rnames[0]],
                                                 fill="toself",name=f"{orow['symbol']} (Outlier)",
                                                 line=dict(color=oc,width=2.5),
                                                 fillcolor="rgba(248,113,113,0.13)"))
        radar_fig.update_layout(**LAYOUT(
                                 height=480, margin=dict(l=40,r=30,t=30,b=50),
                                 polar=dict(bgcolor="rgba(0,0,0,0)",
                                            radialaxis=dict(visible=True,range=[0,1],
                                                            tickfont=dict(size=8,color="#475569"),
                                                            gridcolor="rgba(255,255,255,0.07)",
                                                            linecolor="rgba(255,255,255,0.07)",
                                                            tickvals=[0.25,0.5,0.75,1.0]),
                                            angularaxis=dict(tickfont=dict(size=10,color="#94a3b8"),
                                                             gridcolor="rgba(255,255,255,0.07)",
                                                             linecolor="rgba(255,255,255,0.07)")),
                                 legend=legend_cfg(orientation="h",y=-0.1)))
        st.plotly_chart(radar_fig, use_container_width=True, config={"displayModeBar": False})

        # Position on market map
        st.markdown('<div class="section-heading">📍 Position in the Market Map</div>', unsafe_allow_html=True)
        acolanom = MODEL_MAP[selected_model]
        apdf     = df.copy()
        apdf["Tribe"] = apdf[acolanom].apply(lambda x: "Outlier" if x==-1 else f"Tribe {x}")
        atcmap   = {("Outlier" if c==-1 else f"Tribe {c}"): ccolor(c) for c in sorted(apdf[acolanom].unique())}

        ascat = px.scatter(apdf[apdf["DBSCAN_Cluster"]!=-1], x="PCA1", y="PCA2",
                           color="Tribe", color_discrete_map=atcmap, hover_name="symbol",
                           template="plotly_dark", opacity=0.4,
                           labels={"PCA1":"Overall Market Trend →","PCA2":"Risk / Volatility Profile →"})
        ascat.update_traces(marker=dict(size=7))
        for _,orow in outlier_df.iterrows():
            ascat.add_trace(go.Scatter(x=[orow["PCA1"]],y=[orow["PCA2"]],
                                       mode="markers+text",
                                       marker=dict(size=22,color="#f87171",symbol="star",
                                                   line=dict(width=2,color="#fff")),
                                       text=[orow["symbol"]],textposition="top center",
                                       textfont=dict(size=10,color="#f87171",family="JetBrains Mono"),
                                       name=f"⚠ {orow['symbol']}",showlegend=True))
        ascat.update_layout(**LAYOUT(
                            height=380, margin=dict(l=40,r=30,t=30,b=50),
                            xaxis=axis_cfg("Overall Market Trend →"),
                            yaxis=axis_cfg("Risk / Volatility Profile →")))
        st.plotly_chart(ascat, use_container_width=True, config={"displayModeBar": False})


# ═════════════════════════════════════════════════════════════════════════════
# TAB 7 — CORRELATION MATRIX
# ═════════════════════════════════════════════════════════════════════════════
with tab7:
    st.markdown("""<div class="info-box"><strong>Correlation Matrix</strong> measures how strongly
    pairs of financial metrics move together. <strong>+1.0</strong> = perfect lockstep;
    <strong>−1.0</strong> = perfectly opposite; <strong>0</strong> = no relationship.
    Filter by tribe to uncover hidden relationships inside specific market segments.</div>""",
    unsafe_allow_html=True)

    acol_corr   = MODEL_MAP[selected_model]
    cids_corr   = sorted(df[acol_corr].unique())
    scope_opts  = ["🌐 Entire Market"] + [
        f"{'⚫ Outlier' if c==-1 else f'{tbadge(c)} Tribe {c}'} ({len(df[df[acol_corr]==c])} coins)"
        for c in cids_corr
    ]
    scope_map = {"🌐 Entire Market": None}
    for c in cids_corr:
        lbl = f"{'⚫ Outlier' if c==-1 else f'{tbadge(c)} Tribe {c}'} ({len(df[df[acol_corr]==c])} coins)"
        scope_map[lbl] = c

    cc1,cc2 = st.columns([1,2])
    with cc1:
        st.markdown("<div style='font-size:.72rem;color:#64748b;font-family:\"JetBrains Mono\",monospace;"
                    "text-transform:uppercase;letter-spacing:.08em;margin-bottom:.4rem;'>Filter Scope</div>",
                    unsafe_allow_html=True)
        scope_choice = st.selectbox("scope",scope_opts,index=0,label_visibility="collapsed")

    sel_cid = scope_map[scope_choice]
    if sel_cid is None:
        scope_df   = df; scope_name = "Entire Market (100 assets)"
    else:
        scope_df   = df[df[acol_corr]==sel_cid]
        scope_name = f"{'Outlier' if sel_cid==-1 else f'Tribe {sel_cid}'} ({len(scope_df)} assets)"
    with cc2:
        st.markdown(f'<div class="info-box" style="margin-top:.1rem;">Showing correlations for: '
                    f'<strong>{scope_name}</strong> · n = {len(scope_df)} assets · '
                    f'model = <strong>{selected_model}</strong></div>', unsafe_allow_html=True)

    corr_m   = scope_df[["Mean_Return","Volatility","Momentum"]].corr()
    corr_m.index = corr_m.columns = ["Avg Return","Volatility","Momentum"]

    hmap = px.imshow(corr_m, color_continuous_scale="IceFire", zmin=-1, zmax=1,
                     text_auto=".3f", template="plotly_dark", aspect="auto")
    hmap.update_traces(textfont=dict(family="JetBrains Mono, monospace",size=18,color="#e2e8f0"),
                       hovertemplate="<b>%{y}</b> vs <b>%{x}</b><br>Correlation: <b>%{z:.4f}</b><extra></extra>")
    hmap.update_layout(**LAYOUT(
                       height=460, margin=dict(l=80,r=80,t=40,b=80),
                       xaxis=dict(tickfont=dict(size=12,color="#94a3b8",family="Space Grotesk"),side="bottom"),
                       yaxis=dict(tickfont=dict(size=12,color="#94a3b8",family="Space Grotesk")),
                       coloraxis_colorbar=dict(title=dict(text="Correlation",font=dict(size=10,color="#64748b")),
                                               tickfont=dict(size=9,color="#64748b"),thickness=14,len=0.85,
                                               bgcolor="rgba(13,18,32,0.8)",bordercolor="rgba(99,179,237,0.15)")))
    st.plotly_chart(hmap, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-heading">🔍 Plain-English Interpretation</div>', unsafe_allow_html=True)
    ic1,ic2,ic3 = st.columns(3)
    rv_val = float(corr_m.loc["Avg Return","Volatility"])
    rm_val = float(corr_m.loc["Avg Return","Momentum"])
    vm_val = float(corr_m.loc["Volatility","Momentum"])

    def cstrength(v):
        a = abs(v)
        return "very strong" if a>0.7 else ("moderate" if a>0.4 else ("weak" if a>0.15 else "negligible"))
    def cdir(v): return "positive" if v>0 else "negative"

    with ic1:
        sign = "⬆️" if rv_val>0 else "⬇️"
        st.markdown(metric_card("Return ↔ Volatility",f"{rv_val:+.3f} {sign}",
            f"{cstrength(rv_val).title()} {cdir(rv_val)} relationship. "
            f"{'Higher-return coins tend to be riskier.' if rv_val>0.15 else 'Return and volatility are relatively independent here.'}",
            "metric-warning" if abs(rv_val)>0.4 else "metric-neutral"), unsafe_allow_html=True)
    with ic2:
        sign = "⬆️" if rm_val>0 else "⬇️"
        st.markdown(metric_card("Return ↔ Momentum",f"{rm_val:+.3f} {sign}",
            f"{cstrength(rm_val).title()} {cdir(rm_val)} relationship. "
            f"{'Trending coins also deliver stronger returns.' if rm_val>0.15 else 'Momentum does not reliably predict return here.' if abs(rm_val)<0.15 else 'High-momentum coins show lower returns in this group.'}",
            "metric-positive" if rm_val>0 else "metric-neutral"), unsafe_allow_html=True)
    with ic3:
        sign = "⬆️" if vm_val>0 else "⬇️"
        st.markdown(metric_card("Volatility ↔ Momentum",f"{vm_val:+.3f} {sign}",
            f"{cstrength(vm_val).title()} {cdir(vm_val)} relationship. "
            f"{'More volatile coins are also trending harder.' if vm_val>0.15 else 'Risk and momentum are broadly independent here.' if abs(vm_val)<0.15 else 'Lower-risk coins show stronger momentum in this group.'}",
            "metric-positive" if vm_val>0 else "metric-warning"), unsafe_allow_html=True)

    # Cross-tribe comparison
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📊 Compare Correlations Across All Tribes", expanded=False):
        rows = []
        for cid in cids_corr:
            sub = df[df[acol_corr]==cid]
            if len(sub)>=3:
                rows.append({"Tribe": "Outlier" if cid==-1 else f"Tribe {cid}",
                             "Return↔Volatility":  round(float(sub["Mean_Return"].corr(sub["Volatility"])),4),
                             "Return↔Momentum":    round(float(sub["Mean_Return"].corr(sub["Momentum"])),4),
                             "Volatility↔Momentum":round(float(sub["Volatility"].corr(sub["Momentum"])),4),
                             "Assets": len(sub)})
        cdf = pd.DataFrame(rows)
        if not cdf.empty:
            cfig = go.Figure()
            for bi,bcol in enumerate(["Return↔Volatility","Return↔Momentum","Volatility↔Momentum"]):
                cfig.add_trace(go.Bar(name=bcol,x=cdf["Tribe"],y=cdf[bcol],
                                      marker_color=NEON_SEQ[bi%len(NEON_SEQ)],opacity=0.82))
            cfig.add_hline(y=0,line=dict(color="rgba(255,255,255,0.15)",width=1,dash="dot"))
            cfig.update_layout(**LAYOUT(barmode="group",height=320,margin=dict(l=40,r=30,t=30,b=50),
                                xaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(size=10)),
                                yaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(size=9),
                                           title=dict(text="Correlation Coefficient (−1 to +1)",
                                                      font=dict(size=9,color="#475569")),range=[-1.1,1.1])))
            st.plotly_chart(cfig, use_container_width=True, config={"displayModeBar": False})
            st.dataframe(cdf, use_container_width=True, hide_index=True)