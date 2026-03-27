from datetime import date
import io
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="SDG 15 - Life on Land",
    page_icon="🌿",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(180deg, #fff7f8 0%, #fff1f3 100%);
            color: #1f1f1f;
        }
        .hero {
            background: linear-gradient(120deg, #b00020 0%, #7a0018 100%);
            color: white;
            padding: 2rem;
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.15);
            box-shadow: 0 10px 28px rgba(0,0,0,0.15);
            margin-bottom: 1rem;
        }
        .card {
            background: white;
            border: 1px solid #ffd1d9;
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 6px 18px rgba(176, 0, 32, 0.09);
            color: #1f1f1f;
        }
        .tm-badge {
            background: #e60028;
            color: white;
            border-radius: 999px;
            padding: 0.25rem 0.75rem;
            font-size: 0.85rem;
            font-weight: 700;
            display: inline-block;
            margin-bottom: 0.5rem;
        }
        .kpi {
            background: linear-gradient(120deg, #e60028 0%, #b00020 100%);
            color: white;
            border-radius: 14px;
            padding: 1rem;
            text-align: center;
            min-height: 110px;
        }
        .kpi h3 {
            margin: 0;
            font-size: 1.8rem;
            color: white;
        }
        .kpi p {
            margin: 0.25rem 0 0;
            color: #ffe5ea;
            font-size: 0.92rem;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #121212 !important;
        }
        .hero h1, .hero h2, .hero h3, .hero p {
            color: white !important;
        }
        p, li, label, span, div {
            color: #1f1f1f;
        }
        [data-testid="stSidebar"] {
            background: #fff0f3;
            border-right: 1px solid #ffc3cf;
        }
        [data-testid="stSidebar"] * {
            color: #1f1f1f !important;
        }
        .stButton > button {
            background: #e60028;
            color: white;
            border: 1px solid #b00020;
            border-radius: 10px;
            font-weight: 600;
        }
        .stButton > button:hover {
            background: #b00020;
            border-color: #7a0018;
            color: white;
        }
        .stTabs [data-baseweb="tab"] {
            color: #7a0018;
            font-weight: 700;
        }
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        .stTextInput input,
        .stNumberInput input,
        .stDateInput input {
            background: #fffafb !important;
            color: #1f1f1f !important;
            border: 1px solid #ffb8c6 !important;
        }
        div[data-baseweb="input"] input::placeholder,
        .stTextInput input::placeholder {
            color: #7a0018 !important;
            opacity: 0.7;
        }
        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div,
        .stSelectbox label,
        .stTextInput label,
        .stNumberInput label,
        .stDateInput label {
            color: #1f1f1f !important;
        }
        [data-baseweb="select"] svg {
            color: #7a0018 !important;
            fill: #7a0018 !important;
        }
        /* Fix dropdown menu readability (opened options list) */
        [role="listbox"] {
            background: #fffafb !important;
            border: 1px solid #ffb8c6 !important;
        }
        [role="option"] {
            background: #fffafb !important;
            color: #1f1f1f !important;
        }
        [role="option"][aria-selected="true"] {
            background: #ffe5ea !important;
            color: #7a0018 !important;
            font-weight: 600;
        }
        [role="option"]:hover {
            background: #ffd6df !important;
            color: #1f1f1f !important;
        }
        [data-testid="stMarkdownContainer"] code {
            color: #7a0018;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "pledges" not in st.session_state:
    st.session_state.pledges = []
if "action_log" not in st.session_state:
    st.session_state.action_log = []
if "obs_log" not in st.session_state:
    st.session_state.obs_log = []

st.sidebar.markdown("## Thomas More x SDG")
st.sidebar.markdown("### Project: SDG 15")
st.sidebar.success("Thema actief: Life on Land")
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Doel van de app**
    - Bewustwording rond biodiversiteit
    - Lokale acties zichtbaar maken
    - Jongeren motiveren om mee te doen
    """
)

st.markdown(
    """
    <div class="hero">
        <span class="tm-badge">THOMAS MORE THEME</span>
        <h1 style="margin:0 0 0.35rem 0;">SDG 15: Life on Land</h1>
        <p style="margin:0; font-size:1.05rem; color:#ffe5ea;">
            Bescherm, herstel en bevorder het duurzaam gebruik van ecosystemen op land.
            Deze interactieve website laat zien hoe studenten en burgers lokaal impact kunnen maken.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

top_left, top_mid, top_right = st.columns(3)
with top_left:
    st.markdown(
        """
        <div class="kpi">
            <h3>31%</h3>
            <p>landoppervlak wereldwijd is bosgebied</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with top_mid:
    st.markdown(
        """
        <div class="kpi">
            <h3>1M+</h3>
            <p>soorten riskeren uitsterven op lange termijn</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with top_right:
    st.markdown(
        """
        <div class="kpi">
            <h3>2030</h3>
            <p>deadline om SDG-doelen te versnellen</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

tab1, tab2, tab3 = st.tabs(
    ["Biodiversiteitsscan", "Actieplanner", "Natuurdagboek"]
)

with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Scan jouw tuin, straat of schoolomgeving")
    c1, c2 = st.columns(2)
    with c1:
        groen_pct = st.slider("Hoeveel % van de zone is groen?", 0, 100, 35)
        inheemse_planten = st.slider("Hoeveel verschillende lokale planten zie je?", 0, 40, 8)
        bomen = st.slider("Aantal bomen", 0, 30, 3)
    with c2:
        pesticide = st.selectbox(
            "Gebruik je pesticiden?",
            ["Nooit", "Soms", "Vaak"],
        )
        wateropvang = st.checkbox("Er is regenwateropvang", value=False)
        nestplek = st.checkbox("Er zijn nest- of schuilplekken voor dieren", value=True)

    pesticide_penalty = {"Nooit": 0, "Soms": 10, "Vaak": 25}[pesticide]
    score = (
        (groen_pct * 0.35)
        + (inheemse_planten * 1.4)
        + (bomen * 1.8)
        + (12 if wateropvang else 0)
        + (10 if nestplek else 0)
        - pesticide_penalty
    )
    score = max(0, min(100, round(score)))

    if score >= 70:
        label = "Sterk ecosysteem"
        kleur = "success"
    elif score >= 40:
        label = "Gemiddeld ecosysteem"
        kleur = "warning"
    else:
        label = "Kwetsbaar ecosysteem"
        kleur = "error"

    st.metric("Biodiversiteitsscore", f"{score}/100")
    getattr(st, kleur)(f"Resultaat: {label}")

    tips = []
    if groen_pct < 45:
        tips.append("Verhoog groene oppervlakte met gevelgroen of plantvakken.")
    if inheemse_planten < 12:
        tips.append("Voeg meer inheemse plantensoorten toe voor bestuivers.")
    if bomen < 5:
        tips.append("Plant extra bomen voor schaduw en betere bodemkwaliteit.")
    if pesticide != "Nooit":
        tips.append("Verminder pesticiden en kies ecologische alternatieven.")
    if not wateropvang:
        tips.append("Installeer regenwateropvang voor droogtebestendigheid.")
    if not nestplek:
        tips.append("Voorzie nestkastjes of natuurlijke schuilplekken.")

    st.markdown("**Jouw gepersonaliseerde verbeteracties:**")
    if tips:
        for tip in tips:
            st.write(f"- {tip}")
    else:
        st.write("- Je doet het al heel goed. Hou dit niveau aan.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Praktische weekplanner")
    actie = st.selectbox(
        "Kies een actie",
        [
            "Boom planten",
            "Zwerfvuil opruimen",
            "Bloemenstrook aanleggen",
            "Nestkast plaatsen",
            "Workshop geven op school",
        ],
    )
    uren = st.slider("Aantal uren dat je eraan werkt", 1, 10, 2)
    deelnemers = st.number_input("Aantal deelnemers", min_value=1, max_value=200, value=3)
    actiedatum = st.date_input("Datum", value=date.today())

    impact_map = {
        "Boom planten": 18,
        "Zwerfvuil opruimen": 10,
        "Bloemenstrook aanleggen": 14,
        "Nestkast plaatsen": 12,
        "Workshop geven op school": 9,
    }
    impactscore = impact_map[actie] * deelnemers + (uren * 2)

    if st.button("Actie opslaan", use_container_width=True):
        st.session_state.action_log.append(
            {
                "Datum": str(actiedatum),
                "Actie": actie,
                "Uren": uren,
                "Deelnemers": deelnemers,
                "Impactscore": impactscore,
            }
        )
        st.success("Actie toegevoegd aan je planner.")

    if st.session_state.action_log:
        df_actions = pd.DataFrame(st.session_state.action_log)
        st.dataframe(df_actions, use_container_width=True)
        st.bar_chart(df_actions.set_index("Datum")["Impactscore"], color="#e60028")
        st.metric("Totale impactscore", int(df_actions["Impactscore"].sum()))
    else:
        st.info("Nog geen acties toegevoegd.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Natuurdagboek en observaties")
    soort = st.text_input("Waargenomen soort (plant of dier)")
    locatie = st.text_input("Locatie")
    aantal = st.number_input("Aantal waarnemingen", min_value=1, max_value=500, value=1)
    status = st.selectbox("Status", ["Gezien", "Veel gezien", "Zeldzaam"])

    if st.button("Observatie toevoegen", use_container_width=True):
        if soort.strip() and locatie.strip():
            st.session_state.obs_log.append(
                {
                    "Datum": str(date.today()),
                    "Soort": soort.strip(),
                    "Locatie": locatie.strip(),
                    "Aantal": int(aantal),
                    "Status": status,
                }
            )
            st.success("Observatie toegevoegd.")
        else:
            st.warning("Vul soort en locatie in.")

    if st.session_state.obs_log:
        df_obs = pd.DataFrame(st.session_state.obs_log)
        st.dataframe(df_obs, use_container_width=True)

        csv_bytes = df_obs.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download observaties als CSV",
            data=io.BytesIO(csv_bytes),
            file_name="natuurdagboek.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.info("Nog geen observaties.")
    st.markdown("</div>", unsafe_allow_html=True)

left_col, right_col = st.columns([1.1, 0.9])
with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Waarom SDG 15 belangrijk is")
    st.write(
        """
        SDG 15 gaat over bossen, biodiversiteit, bodemkwaliteit en ecosystemen.
        Zonder gezonde natuur zijn er grotere risico's op voedselproblemen, hitte-eilanden,
        overstromingen en verlies van leefruimte voor dieren.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Jouw SDG 15 pledge")
    naam = st.text_input("Naam")
    keuze = st.selectbox(
        "Welke actie ga jij doen?",
        [
            "Ik plant dit semester minstens 1 boom",
            "Ik help 1 keer per maand met natuurherstel",
            "Ik promoot biodiversiteit op school",
            "Ik start een lokale SDG-campagne",
        ],
    )
    if st.button("Voeg pledge toe", use_container_width=True):
        if naam.strip():
            st.session_state.pledges.append(f"{naam.strip()} - {keuze}")
            st.success("Top! Jouw pledge is toegevoegd.")
        else:
            st.warning("Vul eerst je naam in.")

    if st.session_state.pledges:
        st.markdown("**Community pledges**")
        for item in st.session_state.pledges[-8:]:
            st.write(f"- {item}")
    else:
        st.info("Nog geen pledges. Word de eerste!")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### Thomas More Design Notes")
c1, c2, c3 = st.columns(3)
c1.info("Kleuren: roodtinten in Thomas More stijl")
c2.info("Heldere kaarten en afgeronde UI")
c3.info("Interactieve elementen voor showcase")

st.caption(
    "Gemaakt voor de projectfase 'Van Ontwerp naar App' met Streamlit en een Thomas More look & feel."
)