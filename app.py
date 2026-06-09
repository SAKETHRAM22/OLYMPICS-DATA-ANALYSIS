import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


st.set_page_config(
    page_title="Olympic Intelligence Platform",
    page_icon="◎",
    layout="wide",
    initial_sidebar_state="expanded",
)

GOLD = "#F5C542"
BLUE = "#0085FF"
SILVER = "#C0C0C0"
BRONZE = "#CD7F32"
BLACK = "#0B0B0B"
SURFACE = "#141414"
MUTED = "#A3A3A3"
GRID = "rgba(255,255,255,0.08)"
PLOT_COLORS = [GOLD, BLUE, SILVER, BRONZE, "#10B981", "#F97316", "#A855F7"]
IOC_TO_ISO = {
    "AFG": "AF", "ALB": "AL", "ALG": "DZ", "AND": "AD", "ANG": "AO", "ARG": "AR",
    "ARM": "AM", "AUS": "AU", "AUT": "AT", "AZE": "AZ", "BAH": "BS", "BAN": "BD",
    "BAR": "BB", "BEL": "BE", "BER": "BM", "BIH": "BA", "BLR": "BY", "BOL": "BO",
    "BOT": "BW", "BRA": "BR", "BRN": "BH", "BUL": "BG", "CAN": "CA", "CHI": "CL",
    "CHN": "CN", "COL": "CO", "CRC": "CR", "CRO": "HR", "CUB": "CU", "CYP": "CY",
    "CZE": "CZ", "DEN": "DK", "DOM": "DO", "ECU": "EC", "EGY": "EG", "ERI": "ER",
    "ESP": "ES", "EST": "EE", "ETH": "ET", "FIN": "FI", "FRA": "FR", "GBR": "GB",
    "GEO": "GE", "GER": "DE", "GHA": "GH", "GRE": "GR", "GUA": "GT", "HKG": "HK",
    "HUN": "HU", "INA": "ID", "IND": "IN", "IRI": "IR", "IRL": "IE", "IRQ": "IQ",
    "ISL": "IS", "ISR": "IL", "ITA": "IT", "JAM": "JM", "JOR": "JO", "JPN": "JP",
    "KAZ": "KZ", "KEN": "KE", "KOR": "KR", "KSA": "SA", "KUW": "KW", "LAT": "LV",
    "LBN": "LB", "LTU": "LT", "LUX": "LU", "MAR": "MA", "MAS": "MY", "MDA": "MD",
    "MEX": "MX", "MGL": "MN", "MKD": "MK", "MNE": "ME", "NED": "NL", "NGR": "NG",
    "NOR": "NO", "NZL": "NZ", "PAK": "PK", "PAN": "PA", "PER": "PE", "PHI": "PH",
    "POL": "PL", "POR": "PT", "PRK": "KP", "PUR": "PR", "QAT": "QA", "ROU": "RO",
    "RSA": "ZA", "RUS": "RU", "SEN": "SN", "SGP": "SG", "SLO": "SI", "SRB": "RS",
    "SRI": "LK", "SUI": "CH", "SVK": "SK", "SWE": "SE", "SYR": "SY", "THA": "TH",
    "TPE": "TW", "TTO": "TT", "TUN": "TN", "TUR": "TR", "UAE": "AE", "UGA": "UG",
    "UKR": "UA", "URU": "UY", "USA": "US", "UZB": "UZ", "VEN": "VE", "VIE": "VN",
    "YUG": "RS", "ZIM": "ZW",
}


@st.cache_data(show_spinner="Loading Olympic intelligence data...")
def load_data():
    df = pd.read_csv("athlete_events.csv")
    region_df = pd.read_csv("noc_regions.csv")
    return preprocessor.preprocess(df, region_df)


df = load_data()


def apply_design_system():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {{
            --black: {BLACK};
            --surface: {SURFACE};
            --gold: {GOLD};
            --blue: {BLUE};
            --silver: {SILVER};
            --bronze: {BRONZE};
            --muted: {MUTED};
        }}

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 10% 0%, rgba(0,133,255,0.16), transparent 28%),
                radial-gradient(circle at 88% 12%, rgba(245,197,66,0.12), transparent 30%),
                linear-gradient(135deg, #050505 0%, #0B0B0B 48%, #101010 100%);
            color: #F7F7F7;
        }}

        .main .block-container {{
            max-width: 1680px;
            padding: 2rem 2.4rem 4rem;
        }}

        [data-testid="stSidebar"] {{
            background: rgba(12,12,12,0.94);
            border-right: 1px solid rgba(255,255,255,0.08);
            backdrop-filter: blur(16px);
        }}

        [data-testid="stSidebar"] * {{
            color: #F5F5F5;
        }}

        [data-testid="stSidebar"] .stRadio label,
        [data-testid="stSidebar"] .stSelectbox label {{
            color: #D7D7D7 !important;
            font-weight: 700;
            letter-spacing: 0.02em;
            text-transform: uppercase;
            font-size: 0.72rem;
        }}

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {{
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 14px;
        }}

        .stDataFrame, .stTable {{
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 22px 70px rgba(0,0,0,0.32);
        }}

        .platform-header {{
            position: relative;
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 24px;
            padding: 28px 30px;
            background:
                linear-gradient(135deg, rgba(20,20,20,0.96), rgba(20,20,20,0.74)),
                linear-gradient(90deg, rgba(0,133,255,0.18), rgba(245,197,66,0.10));
            box-shadow: 0 30px 90px rgba(0,0,0,0.38);
            overflow: hidden;
            margin-bottom: 24px;
        }}

        .platform-header:after {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, transparent 0%, rgba(255,255,255,0.06) 45%, transparent 68%);
            transform: translateX(-70%);
            animation: sheen 8s ease-in-out infinite;
        }}

        @keyframes sheen {{
            0%, 60% {{ transform: translateX(-70%); }}
            100% {{ transform: translateX(80%); }}
        }}

        .rings {{
            display: flex;
            gap: 7px;
            align-items: center;
            margin-bottom: 16px;
        }}

        .ring {{
            width: 22px;
            height: 22px;
            border: 3px solid;
            border-radius: 50%;
            box-shadow: 0 0 18px currentColor;
        }}

        .platform-title {{
            font-size: clamp(2.2rem, 4vw, 4.4rem);
            line-height: 1.02;
            margin: 0;
            font-weight: 800;
            letter-spacing: 0;
        }}

        .platform-subtitle {{
            color: #CFCFCF;
            font-size: 1.05rem;
            margin: 12px 0 0;
            max-width: 820px;
        }}

        .section-shell {{
            background: rgba(20,20,20,0.76);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 22px;
            padding: 24px;
            box-shadow: 0 24px 80px rgba(0,0,0,0.28);
            margin: 18px 0 24px;
            backdrop-filter: blur(12px);
            animation: reveal 0.55s ease both;
        }}

        @keyframes reveal {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .section-kicker {{
            color: {GOLD};
            text-transform: uppercase;
            font-weight: 800;
            letter-spacing: 0.11em;
            font-size: 0.72rem;
            margin-bottom: 8px;
        }}

        .section-title {{
            margin: 0;
            color: #FFFFFF;
            font-size: 1.65rem;
            font-weight: 800;
            letter-spacing: 0;
        }}

        .section-copy {{
            color: #BEBEBE;
            margin: 8px 0 18px;
            max-width: 900px;
            line-height: 1.6;
        }}

        .kpi-card {{
            min-height: 164px;
            padding: 20px;
            border-radius: 22px;
            background: linear-gradient(145deg, rgba(20,20,20,0.96), rgba(255,255,255,0.035));
            border: 1px solid rgba(255,255,255,0.08);
            box-shadow: 0 22px 70px rgba(0,0,0,0.26);
            transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-6px);
            border-color: rgba(245,197,66,0.55);
            box-shadow: 0 30px 90px rgba(245,197,66,0.10);
        }}

        .kpi-icon {{
            width: 42px;
            height: 42px;
            display: grid;
            place-items: center;
            border-radius: 15px;
            background: rgba(245,197,66,0.12);
            color: {GOLD};
            font-size: 1.35rem;
            margin-bottom: 18px;
        }}

        .kpi-label {{
            color: #B9B9B9;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 800;
        }}

        .kpi-value {{
            font-size: 2.05rem;
            line-height: 1;
            font-weight: 800;
            color: #FFFFFF;
            margin: 8px 0;
        }}

        .kpi-trend {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            color: #7DE2B8;
            background: rgba(16,185,129,0.10);
            border: 1px solid rgba(16,185,129,0.20);
            padding: 5px 9px;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 800;
        }}

        .metric-strip {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin: 10px 0 18px;
        }}

        .pill {{
            padding: 9px 12px;
            border-radius: 999px;
            border: 1px solid rgba(255,255,255,0.10);
            background: rgba(255,255,255,0.05);
            color: #EAEAEA;
            font-weight: 700;
        }}

        .athlete-card {{
            padding: 17px;
            border-radius: 18px;
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.08);
            transition: transform 0.25s ease, background 0.25s ease;
            min-height: 142px;
        }}

        .athlete-card:hover {{
            transform: translateY(-4px);
            background: rgba(255,255,255,0.07);
        }}

        .athlete-rank {{
            color: {GOLD};
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08em;
        }}

        .athlete-name {{
            color: #FFFFFF;
            font-weight: 800;
            margin-top: 8px;
            font-size: 1rem;
        }}

        .athlete-meta {{
            color: #BDBDBD;
            font-size: 0.85rem;
            margin-top: 8px;
            line-height: 1.35;
        }}

        .sidebar-brand {{
            padding: 10px 2px 18px;
            border-bottom: 1px solid rgba(255,255,255,0.10);
            margin-bottom: 18px;
        }}

        .sidebar-brand-title {{
            font-size: 1rem;
            font-weight: 800;
            color: #FFFFFF;
        }}

        .sidebar-brand-copy {{
            color: #A8A8A8;
            font-size: 0.78rem;
            margin-top: 5px;
        }}

        .separator {{
            height: 1px;
            background: rgba(255,255,255,0.10);
            margin: 18px 0;
        }}

        .stPlotlyChart {{
            border-radius: 20px;
            overflow: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def configure_plotly(fig, height=430, showlegend=True):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(family="Inter, sans-serif", color="#F4F4F5"),
        hovermode="x unified",
        showlegend=showlegend,
        margin=dict(l=24, r=24, t=42, b=36),
        colorway=PLOT_COLORS,
        legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, showline=False)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, showline=False)
    return fig


def section(kicker, title, copy):
    st.markdown(
        f"""
        <div class="section-shell">
            <div class="section-kicker">{kicker}</div>
            <h2 class="section-title">{title}</h2>
            <p class="section-copy">{copy}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def header():
    st.markdown(
        """
        <div class="platform-header">
            <div class="rings">
                <span class="ring" style="color:#0085FF"></span>
                <span class="ring" style="color:#F5C542"></span>
                <span class="ring" style="color:#111;border-color:#EAEAEA;box-shadow:0 0 18px rgba(255,255,255,0.32)"></span>
                <span class="ring" style="color:#10B981"></span>
                <span class="ring" style="color:#CD7F32"></span>
            </div>
            <h1 class="platform-title">Olympic Intelligence Platform</h1>
            <p class="platform-subtitle">125 Years of Olympic Performance Analytics</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(icon, label, value, description, trend):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value:,}</div>
            <div style="color:#BDBDBD;font-size:0.86rem;min-height:40px;">{description}</div>
            <span class="kpi-trend">▲ {trend}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpis():
    editions = df["Year"].nunique() - 1
    cities = df["City"].nunique()
    sports = df["Sport"].nunique()
    events = df["Event"].nunique()
    athletes = df["Name"].nunique()
    nations = df["region"].nunique()

    cols = st.columns(6)
    cards = [
        ("◎", "Editions", editions, "Modern Olympic cycles analyzed", "Historic coverage"),
        ("◈", "Countries", nations, "National delegations represented", "Global reach"),
        ("◌", "Athletes", athletes, "Competitors across all records", "Deep roster"),
        ("◆", "Sports", sports, "Disciplines in the Olympic program", "Program breadth"),
        ("◇", "Events", events, "Medal and participation events", "Event density"),
        ("●", "Host Cities", cities, "Cities that staged the Games", "Host network"),
    ]

    for col, card in zip(cols, cards):
        with col:
            kpi_card(*card)


def sidebar():
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">Olympic Command Center</div>
            <div class="sidebar-brand-copy">Performance, medals, nations, athletes</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pages = {
        "🏅 Global Medal Intelligence": "Medal Tally",
        "📈 Olympic Intelligence Overview": "Overall Analysis",
        "🌍 National Performance Intelligence": "Country wise Analysis",
        "🧬 Athlete Performance Laboratory": "Athlete wise analysis",
    }

    choice = st.sidebar.radio("Navigation", list(pages.keys()), label_visibility="collapsed")
    st.sidebar.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.sidebar.caption("Filters update the active intelligence view.")
    return pages[choice]


def medal_color_table(table):
    numeric_cols = [col for col in ["🥇 Gold", "🥈 Silver", "🥉 Bronze", "Total"] if col in table.columns]
    gold_col = "🥇 Gold" if "🥇 Gold" in table.columns else None
    silver_col = "🥈 Silver" if "🥈 Silver" in table.columns else None
    bronze_col = "🥉 Bronze" if "🥉 Bronze" in table.columns else None
    styled = table.style.format({col: "{:,.0f}" for col in numeric_cols}).set_properties(
        **{"background-color": SURFACE, "color": "#F4F4F5", "border-color": "#2A2A2A"}
    )
    if gold_col:
        styled = styled.background_gradient(subset=[gold_col], cmap="YlOrBr")
    if silver_col:
        styled = styled.background_gradient(subset=[silver_col], cmap="Greys")
    if bronze_col:
        styled = styled.background_gradient(subset=[bronze_col], cmap="Oranges")
    return (
        styled
    )


def flag_from_iso(code):
    if not code or len(code) != 2:
        return "🏳"
    return "".join(chr(127397 + ord(char)) for char in code.upper())


def medal_display_table(tally, selected_country):
    display = tally.copy()
    if "NOC" in display.columns:
        display.insert(0, "Flag", display["NOC"].map(lambda noc: flag_from_iso(IOC_TO_ISO.get(str(noc).upper()))))
    elif "Year" in display.columns:
        display.insert(0, "Flag", "🏳" if selected_country == "Overall" else "🏅")
    for col, icon in {"Gold": "🥇", "Silver": "🥈", "Bronze": "🥉"}.items():
        if col in display.columns:
            display.rename(columns={col: f"{icon} {col}"}, inplace=True)
    return display


def medal_tally_page():
    st.sidebar.header("Medal Intelligence")
    years, countries = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Edition", years)
    selected_country = st.sidebar.selectbox("Country Search", countries)

    with st.spinner("Compiling medal intelligence..."):
        tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    context_title = "Global Medal Intelligence"
    if selected_year != "Overall" and selected_country == "Overall":
        context_title = f"{selected_year} Olympic Medal Intelligence"
    elif selected_year == "Overall" and selected_country != "Overall":
        context_title = f"{selected_country} Medal Intelligence"
    elif selected_year != "Overall" and selected_country != "Overall":
        context_title = f"{selected_country} at the {selected_year} Olympics"

    section(
        "Medal Tally",
        context_title,
        "A command-center view of podium conversion, medal concentration, and the leading national programs behind Olympic dominance.",
    )

    if tally.empty:
        st.warning("No medal data available for the selected filters.")
        return

    medal_cols = [col for col in ["Gold", "Silver", "Bronze", "Total"] if col in tally.columns]
    totals = tally[medal_cols].sum(numeric_only=True)
    st.markdown(
        f"""
        <div class="metric-strip">
            <span class="pill">🥇 Gold {int(totals.get("Gold", 0)):,}</span>
            <span class="pill">🥈 Silver {int(totals.get("Silver", 0)):,}</span>
            <span class="pill">🥉 Bronze {int(totals.get("Bronze", 0)):,}</span>
            <span class="pill">Total {int(totals.get("Total", 0)):,}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    chart_col, pie_col = st.columns([1.45, 1])
    top_col = "NOC" if "NOC" in tally.columns else "Year"
    top_10 = tally.sort_values("Total", ascending=False).head(10)

    with chart_col:
        bar = px.bar(
            top_10,
            x="Total",
            y=top_col,
            orientation="h",
            color="Gold",
            color_continuous_scale=[BRONZE, GOLD],
            text="Total",
            title="Top 10 Medal Producers",
        )
        bar.update_traces(textposition="outside", marker_line_width=0, hovertemplate="<b>%{y}</b><br>Total medals: %{x}<extra></extra>")
        bar.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(configure_plotly(bar, height=470, showlegend=False), use_container_width=True)

    with pie_col:
        pie_values = [totals.get("Gold", 0), totals.get("Silver", 0), totals.get("Bronze", 0)]
        pie = px.pie(
            names=["Gold", "Silver", "Bronze"],
            values=pie_values,
            hole=0.56,
            color=["Gold", "Silver", "Bronze"],
            color_discrete_map={"Gold": GOLD, "Silver": SILVER, "Bronze": BRONZE},
            title="Medal Share by Type",
        )
        pie.update_traces(textinfo="percent+label", hovertemplate="<b>%{label}</b><br>%{value:,} medals<br>%{percent}<extra></extra>")
        st.plotly_chart(configure_plotly(pie, height=470), use_container_width=True)

    st.subheader("Sortable Medal Table")
    display_tally = medal_display_table(tally, selected_country)
    st.dataframe(medal_color_table(display_tally), use_container_width=True, height=520)


def line_chart(data, x, y, title, color):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data[x],
        y=data[y],
        mode="lines",
        line=dict(width=0),
        fill="tozeroy",
        fillcolor=f"rgba({int(color[1:3], 16)},{int(color[3:5], 16)},{int(color[5:7], 16)},0.18)",
        hoverinfo="skip",
        showlegend=False,
    ))
    fig.add_trace(go.Scatter(
        x=data[x],
        y=data[y],
        mode="lines+markers",
        line=dict(color=color, width=4, shape="spline"),
        marker=dict(size=8, color=color),
        name=y,
        hovertemplate=f"<b>%{{x}}</b><br>{y}: %{{y:,}}<extra></extra>",
    ))
    fig.update_layout(title=title)
    return configure_plotly(fig, height=380, showlegend=False)


def athlete_cards(table, max_cards=6):
    cards = table.head(max_cards).reset_index(drop=True)
    cols = st.columns(3)
    for idx, row in cards.iterrows():
        with cols[idx % 3]:
            region = row.get("region", "")
            sport = row.get("Sport", "")
            medals = row.get("Medals", row.get("count", ""))
            st.markdown(
                f"""
                <div class="athlete-card">
                    <div class="athlete-rank">RANK {idx + 1:02d}</div>
                    <div class="athlete-name">{row.get("Name", "Unknown")}</div>
                    <div class="athlete-meta">{sport}<br>{region}<br><b style="color:{GOLD};">{medals} medals</b></div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def overall_page():
    section(
        "Executive Overview",
        "Olympic Intelligence Overview",
        "The Olympic movement expands like a living global system: more nations, more athletes, richer event calendars, and increasingly specialized elite performers.",
    )

    st.markdown('<div class="section-kicker">Olympic Growth Story</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    nations_over_time = helper.participating_nations_over_time(df, "region")
    events_over_time = helper.events_over_time(df, "Event")
    athletes_over_time = helper.athletes_over_time(df, "Name")

    with col1:
        st.plotly_chart(line_chart(nations_over_time, "Edition", "No of Countries", "Nations Over Time", BLUE), use_container_width=True)
    with col2:
        st.plotly_chart(line_chart(events_over_time, "Edition", "No of Events", "Events Over Time", GOLD), use_container_width=True)
    with col3:
        st.plotly_chart(line_chart(athletes_over_time, "Edition", "No of Athletes", "Athletes Over Time", "#10B981"), use_container_width=True)

    section(
        "Evolution of Olympic Sports",
        "Event Density by Sport and Edition",
        "This heatmap shows where the Olympic program has deepened over time, revealing the sports that became high-volume medal environments.",
    )

    heatmap_source = df.drop_duplicates(["Year", "Sport", "Event"])
    heatmap_df = heatmap_source.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count").fillna(0).astype(int)
    heatmap = px.imshow(
        heatmap_df,
        aspect="auto",
        color_continuous_scale=["#101010", BLUE, GOLD],
        labels=dict(x="Edition", y="Sport", color="Events"),
        title="Olympic Sports Program Heatmap",
    )
    st.plotly_chart(configure_plotly(heatmap, height=760), use_container_width=True)

    section(
        "Greatest Athletes",
        "Medal Leaders and Dominant Performers",
        "The leading athletes sit at the intersection of repeat qualification, event opportunity, team context, and extraordinary competitive durability.",
    )

    sports_list = df["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, "Overall")
    selected_sport = st.selectbox("Sport Search", sports_list, key="overall_sport")
    most_successful = helper.most_successful_athlete(df, selected_sport)
    athlete_cards(most_successful)
    st.dataframe(most_successful, use_container_width=True, height=360)


def country_profile_values(selected_country):
    medal_base = helper.fetch_medal_tally(df, "Overall", selected_country)
    total_medals = int(medal_base["Total"].sum()) if "Total" in medal_base else 0
    debut = df[df["region"] == selected_country]["Year"].min() if selected_country != "Overall" else df["Year"].min()
    global_tally = helper.fetch_medal_tally(df, "Overall", "Overall").sort_values("Total", ascending=False).reset_index(drop=True)
    rank = "N/A"
    if selected_country != "Overall":
        nocs = df[df["region"] == selected_country]["NOC"].dropna().unique()
        matched = global_tally[global_tally["NOC"].isin(nocs)]
        if not matched.empty:
            rank = int(matched.index.min() + 1)
    return total_medals, debut, rank, medal_base


def country_page():
    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()
    country_list.insert(0, "Overall")
    selected_country = st.sidebar.selectbox("Country Search", country_list)

    total_medals, debut, rank, medal_base = country_profile_values(selected_country)
    title_country = "Global Olympic Field" if selected_country == "Overall" else selected_country
    section(
        "Scouting Dashboard",
        "National Performance Intelligence",
        "A premium country profile covering medal trajectory, sport strengths, podium mix, and athlete-level sources of competitive advantage.",
    )

    st.markdown(
        f"""
        <div class="metric-strip">
            <span class="pill">{title_country}</span>
            <span class="pill">Ranking {rank}</span>
            <span class="pill">Total Medals {total_medals:,}</span>
            <span class="pill">Olympic Debut {int(debut) if pd.notna(debut) else "N/A"}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    medals_over_time = helper.year_wise_medal_tally2(df, selected_country)
    col1, col2 = st.columns([1.4, 1])
    with col1:
        fig = px.line(medals_over_time, x="Year", y="Medal", markers=True, title="Medal Timeline")
        fig.update_traces(line=dict(color=GOLD, width=4, shape="spline"), marker=dict(size=9, color=GOLD))
        st.plotly_chart(configure_plotly(fig, height=460, showlegend=False), use_container_width=True)

    with col2:
        breakdown = medal_base[["Gold", "Silver", "Bronze"]].sum().reset_index()
        breakdown.columns = ["Medal", "Count"]
        fig = px.bar(
            breakdown,
            x="Medal",
            y="Count",
            color="Medal",
            color_discrete_map={"Gold": GOLD, "Silver": SILVER, "Bronze": BRONZE},
            title="Podium Mix",
            text="Count",
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(configure_plotly(fig, height=460), use_container_width=True)

    section(
        "Sport Distribution",
        "Where Medal Power Concentrates",
        "Sport-wise medal distribution reveals whether performance is broadly diversified or concentrated in a smaller set of specialist programs.",
    )
    medal_events = df.dropna(subset=["Medal"]).drop_duplicates(["Team", "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    if selected_country != "Overall":
        medal_events = medal_events[medal_events["region"] == selected_country]
    sport_dist = medal_events.groupby("Sport")["Medal"].count().sort_values(ascending=False).head(15).reset_index()
    fig = px.bar(sport_dist, x="Medal", y="Sport", orientation="h", color="Medal", color_continuous_scale=[BLUE, GOLD], title="Top Medal Sports")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(configure_plotly(fig, height=560, showlegend=False), use_container_width=True)

    heatmap_df = helper.country_event_heatmap(df, selected_country)
    heatmap = px.imshow(
        heatmap_df,
        aspect="auto",
        color_continuous_scale=["#101010", BLUE, GOLD],
        labels=dict(x="Edition", y="Sport", color="Medals"),
        title="Sport Medal Heatmap",
    )
    st.plotly_chart(configure_plotly(heatmap, height=680), use_container_width=True)

    section(
        "Most Successful Athletes",
        "Athlete-Level Medal Sources",
        "These profiles identify the athletes most associated with the selected national performance footprint.",
    )
    most_successful_country = helper.most_successful_athlete_countrywise(df, selected_country)
    athlete_cards(most_successful_country)
    st.dataframe(most_successful_country, use_container_width=True, height=360)


def safe_weight_height(sport):
    data = helper.weightvsheight(df, sport)
    if data is not None:
        return data
    temp_df = df.drop_duplicates(subset=["Name", "region"]).copy()
    temp_df["Medal"] = temp_df["Medal"].fillna("NO MEDAL")
    return temp_df[temp_df["Sport"] == sport]


def athlete_page():
    section(
        "Sports Science",
        "Athlete Performance Laboratory",
        "A physiology and participation lens on Olympic competition, connecting age, body profile, medal outcomes, sport specialization, and gender participation trends.",
    )

    unique_athletes = df.drop_duplicates(subset=["Name", "region"])
    y1 = unique_athletes["Age"].dropna()
    y2 = unique_athletes[unique_athletes["Medal"] == "Gold"]["Age"].dropna()
    y3 = unique_athletes[unique_athletes["Medal"] == "Silver"]["Age"].dropna()
    y4 = unique_athletes[unique_athletes["Medal"] == "Bronze"]["Age"].dropna()

    fig = ff.create_distplot(
        [y1, y2, y3, y4],
        ["Overall Age", "Gold Medalist", "Silver Medalist", "Bronze Medalist"],
        show_hist=False,
        show_rug=False,
        colors=[BLUE, GOLD, SILVER, BRONZE],
    )
    fig.update_traces(line=dict(width=3))
    st.plotly_chart(configure_plotly(fig, height=520), use_container_width=True)

    section(
        "Gold Medalist Age by Sport",
        "Age Curves for Elite Outcomes",
        "Different sports reward different competitive windows, from early-career explosive disciplines to endurance and precision events with longer peaks.",
    )

    famous_sports = [
        "Basketball", "Judo", "Football", "Tug-Of-War", "Athletics",
        "Swimming", "Badminton", "Sailing", "Gymnastics",
        "Art Competitions", "Handball", "Weightlifting", "Wrestling",
        "Water Polo", "Hockey", "Rowing", "Fencing",
        "Shooting", "Boxing", "Taekwondo", "Cycling", "Diving", "Canoeing",
        "Tennis", "Golf", "Softball", "Archery",
        "Volleyball", "Synchronized Swimming", "Table Tennis", "Baseball",
        "Rhythmic Gymnastics", "Rugby Sevens",
        "Beach Volleyball", "Triathlon", "Rugby", "Polo", "Ice Hockey",
    ]
    x = []
    names = []
    for sport in famous_sports:
        temp_df = unique_athletes[unique_athletes["Sport"] == sport]
        ages = temp_df[temp_df["Medal"] == "Gold"]["Age"].dropna()
        if len(ages) > 1:
            x.append(ages)
            names.append(sport)

    sport_age = ff.create_distplot(x, names, show_hist=False, show_rug=False, colors=PLOT_COLORS * 6)
    sport_age.update_traces(line=dict(width=2))
    st.plotly_chart(configure_plotly(sport_age, height=620), use_container_width=True)

    section(
        "Height vs Weight Analysis",
        "Body Profile and Medal Outcomes",
        "The scatter view compares athlete morphology across sports, medal categories, and gender with transparent markers for dense elite cohorts.",
    )

    sports_list = df["Sport"].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, "Overall")
    selected_sport = st.selectbox("Sport Search", sports_list, key="athlete_sport")
    weight_height = safe_weight_height(selected_sport).dropna(subset=["Weight", "Height"])

    scatter = px.scatter(
        weight_height,
        x="Weight",
        y="Height",
        color="Medal",
        symbol="Sex",
        hover_data=["Name", "region", "Sport", "Age"],
        opacity=0.62,
        color_discrete_map={"Gold": GOLD, "Silver": SILVER, "Bronze": BRONZE, "NO MEDAL": "#6B7280"},
        title="Athlete Height vs Weight",
    )
    scatter.update_traces(marker=dict(size=8, line=dict(width=0)))
    st.plotly_chart(configure_plotly(scatter, height=620), use_container_width=True)

    section(
        "Gender Participation Trend",
        "Participation Balance Across Editions",
        "The gender participation trend shows how Olympic roster composition has evolved as the Games expanded and women’s event access increased.",
    )
    final = helper.men_vs_women(df)
    gender_fig = px.line(final, x="Year", y=["Male", "Female"], markers=True, title="Men vs Women Participation")
    gender_fig.update_traces(line=dict(width=4, shape="spline"), marker=dict(size=8))
    st.plotly_chart(configure_plotly(gender_fig, height=520), use_container_width=True)

    st.markdown(
        f"""
        <div class="metric-strip">
            <span class="pill">Median Age {unique_athletes["Age"].median():.1f}</span>
            <span class="pill">Median Height {unique_athletes["Height"].median():.1f} cm</span>
            <span class="pill">Median Weight {unique_athletes["Weight"].median():.1f} kg</span>
            <span class="pill">Athlete Records {unique_athletes["Name"].nunique():,}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


apply_design_system()
header()
render_kpis()

user_menu = sidebar()

if user_menu == "Medal Tally":
    medal_tally_page()
elif user_menu == "Overall Analysis":
    overall_page()
elif user_menu == "Country wise Analysis":
    country_page()
elif user_menu == "Athlete wise analysis":
    athlete_page()

