from datetime import date
import io
import os
import pandas as pd
import requests
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
        .stDownloadButton > button {
            background: #e60028 !important;
            color: #ffffff !important;
            border: 1px solid #b00020 !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }
        .stDownloadButton > button:hover {
            background: #b00020 !important;
            color: #ffffff !important;
            border-color: #7a0018 !important;
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
        /* Fix date picker popup readability */
        [data-baseweb="calendar"] {
            background: #fffafb !important;
            color: #1f1f1f !important;
        }
        [data-baseweb="calendar"] * {
            color: #1f1f1f !important;
        }
        [data-baseweb="calendar"] [aria-selected="true"] {
            background: #ff4d68 !important;
            color: #ffffff !important;
            border-radius: 999px !important;
        }
        [data-baseweb="calendar"] [role="button"]:hover {
            background: #ffe5ea !important;
            color: #7a0018 !important;
            border-radius: 8px !important;
        }
        [data-baseweb="calendar"] svg {
            fill: #7a0018 !important;
            color: #7a0018 !important;
        }
        [data-testid="stMarkdownContainer"] code {
            color: #7a0018;
        }

        /* Chat-only styling (AI Plant Coach) */
        /* Gebruik robuuste selectors (geen :has) voor consistente weergave. */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 12px !important;
        }
        div[data-testid="stChatMessage"] {
            background: #2f2f2f !important;
            border: 1px solid #4f4f4f !important;
            border-radius: 12px !important;
            padding: 10px 12px !important;
        }
        div[data-testid="stChatMessage"] * {
            color: #ffffff !important;
        }
        div[data-testid="stChatMessage"] a {
            color: #ffd6df !important;
        }
        div[data-testid="stChatMessage"] code {
            color: #ffd6df !important;
            background: transparent !important;
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
if "ai_history" not in st.session_state:
    st.session_state.ai_history = []
if "ai_mode" not in st.session_state:
    st.session_state.ai_mode = "Automatisch (gebruik live AI als key gevonden is)"
if "ai_endpoint" not in st.session_state:
    st.session_state.ai_endpoint = "https://openrouter.ai/api/v1/chat/completions"
if "ai_model" not in st.session_state:
    st.session_state.ai_model = "openai/gpt-4o-mini"


def get_secret_key() -> str:
    try:
        return st.secrets.get("PLANT_AI_API_KEY", "")
    except Exception:
        return ""


def ai_plant_coach(question: str) -> str:
    q = question.lower().strip()
    if not q:
        return "Stel een vraag, bijvoorbeeld: 'Hoe kan ik mijn lavendel gezonder maken?'"
    if len(q) < 5:
        return "Je vraag is te kort. Typ iets specifieker, bv. 'Mijn basilicum heeft gele blaadjes, wat doe ik?'"
    if len(q) > 400:
        return "Je vraag is erg lang. Maak ze korter (max. 400 tekens) voor een beter antwoord."

    blocked_terms = [
        "gif",
        "vergif",
        "bleekmiddel",
        "benzine",
        "zuur",
        "explosief",
        "bom",
        "self-harm",
        "zelfmoord",
    ]
    abusive_terms = [
        "kanker",
        "kkr",
        "tering",
        "mongool",
        "idioot",
        "debiel",
        "hoer",
        "slet",
        "nigger",
        "racist",
        "homohaat",
    ]
    if any(term in q for term in blocked_terms):
        return (
            "Daar kan ik niet mee helpen. Ik geef alleen veilig en natuurvriendelijk tuinadvies "
            "(water, bodem, compost, biodiversiteit, ecologische aanpak)."
        )
    if any(term in q for term in abusive_terms):
        return (
            "Laten we respectvol blijven. Ik help je graag met plantenvragen in nette taal. "
            "Stel je vraag opnieuw, dan geef ik direct bruikbaar advies."
        )

    tips = []
    if any(word in q for word in ["water", "gieten", "droog", "nat"]):
        tips.append(
            "Geef liever minder vaak maar dieper water. Controleer eerst de bovenste 2-3 cm aarde."
        )
    if any(word in q for word in ["mest", "voeding", "geven", "plantenvoeding"]):
        tips.append(
            "Gebruik in het groeiseizoen om de 2-4 weken organische mest. Vermijd overbemesting."
        )
    if any(word in q for word in ["lavendel", "kruid", "kruiden"]):
        tips.append(
            "Lavendel houdt van volle zon, droge grond en weinig mest. Snoei licht na de bloei."
        )
    if any(word in q for word in ["blad", "geel", "bruin", "ziek", "schimmel"]):
        tips.append(
            "Gele of bruine bladeren wijzen vaak op te veel water of slechte drainage. Verwijder zieke bladeren."
        )
    if any(word in q for word in ["insect", "bij", "vlinder", "biodiversiteit", "sdg"]):
        tips.append(
            "Plant inheemse soorten, voorzie bloemvariatie doorheen het jaar en gebruik geen pesticiden."
        )
    if any(word in q for word in ["bodem", "grond", "aarde"]):
        tips.append(
            "Voeg compost toe voor een gezonde bodemstructuur en beter waterbeheer."
        )
    if any(word in q for word in ["slak", "ongedierte", "plaag"]):
        tips.append(
            "Gebruik ecologische aanpak: handmatig verwijderen, barrières, en natuurlijke vijanden aantrekken."
        )

    if not tips:
        return (
            "Ik kan je helpen met bijna alle plantenvragen: water, voeding, bodem, snoei, ziektes, plagen, stekken, "
            "kamerplanten, moestuin en seizoenszorg.\n\n"
            "Voor een sterk antwoord, geef dit mee:\n"
            "- plantnaam\n"
            "- waar de plant staat (binnen/buiten, zon/schaduw)\n"
            "- welk probleem je ziet (gele bladeren, slappe stengel, vlekken, etc.)\n"
            "- hoe vaak je water/voeding geeft"
        )

    return (
        "Hier is mijn advies:\n- "
        + "\n- ".join(tips)
        + "\n\nLet op: dit is algemene hulp en vervangt geen professioneel advies bij ernstige plantenziekte."
    )


def resolve_ai_settings(api_key: str, endpoint: str, model: str) -> tuple[str, str]:
    # Auto-detect Groq keys and set matching OpenAI-compatible endpoint/model.
    if api_key.startswith("gsk_"):
        if "openrouter.ai" in endpoint or endpoint.strip() == "":
            endpoint = "https://api.groq.com/openai/v1/chat/completions"
        if model.strip() in ("", "openai/gpt-4o-mini"):
            model = "llama-3.1-8b-instant"
    return endpoint, model


def ai_api_answer(question: str, api_key: str, endpoint: str, model: str) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Je bent een veilige, praktische AI plantcoach voor SDG 15. "
                    "Beantwoord ALLE plant-gerelateerde vragen (verzorging, voeding, water, bodem, snoei, "
                    "ziektes, plagen, stekken, moestuin, kamerplanten, seizoenszorg, plantkeuze). "
                    "Geef korte, bruikbare tips in eenvoudig Nederlands. "
                    "Als informatie ontbreekt, geef eerst het best mogelijke antwoord en vraag daarna 1-3 korte "
                    "verduidelijkingen. "
                    "GEEN gevaarlijke, toxische, illegale of zelfbeschadigende instructies. "
                    "Gebruik altijd respectvolle taal en weiger scheldwoorden, haatdragende of kwetsende inhoud. "
                    "Nooit adviseren om schadelijke chemicalien te mengen of gevaarlijk te gebruiken. "
                    "Antwoord met concrete stappen, max 8 bullets."
                ),
            },
            {"role": "user", "content": question},
        ],
        "temperature": 0.7,
    }

    final_endpoint, final_model = resolve_ai_settings(api_key, endpoint, model)
    payload["model"] = final_model
    response = requests.post(final_endpoint, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    return content.strip()

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

tab1, tab2, tab3, tab4 = st.tabs(
    ["Biodiversiteitsscan", "Actieplanner", "Natuurdagboek", "AI Plant Coach"]
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

with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("AI Plant Coach")
    st.info(
        "Hoe werkt de AI coach? 1) Typ je plantenvraag. 2) Klik op de knop. "
        "3) Je krijgt direct eenvoudige, veilige en praktische tips."
    )
    st.write(
        "Stel je vraag over planten, bodem, water geven of biodiversiteit. "
        "Je krijgt direct praktische tips in eenvoudige taal."
    )
    with st.expander("AI instellingen (voor echte live AI antwoorden)"):
        st.session_state.ai_mode = st.selectbox(
            "Modus",
            [
                "Automatisch (gebruik live AI als key gevonden is)",
                "Live AI via API key",
                "Lokale coach (offline)",
            ],
            index=(
                0
                if st.session_state.ai_mode == "Automatisch (gebruik live AI als key gevonden is)"
                else (1 if st.session_state.ai_mode == "Live AI via API key" else 2)
            ),
        )
        st.session_state.ai_endpoint = st.text_input(
            "API endpoint",
            value=st.session_state.ai_endpoint,
            help="OpenRouter: https://openrouter.ai/api/v1/chat/completions, Groq: https://api.groq.com/openai/v1/chat/completions",
        )
        st.session_state.ai_model = st.text_input(
            "Model",
            value=st.session_state.ai_model,
            help="Voorbeeld: openai/gpt-4o-mini of een model dat je provider ondersteunt",
        )
        api_key_input = st.text_input(
            "API key",
            type="password",
            help="Je key wordt enkel in deze sessie gebruikt.",
        )
        st.caption(
            "Met key gebruikt de app live AI. Zonder key valt hij terug op de lokale coach."
        )
    if st.button("Wis chatgeschiedenis", use_container_width=True):
        st.session_state.ai_history = []
        st.success("Chatgeschiedenis gewist.")

    # Backward-compatible conversie van oude structuur {"vraag","antwoord"} naar chatberichten.
    if st.session_state.ai_history and "vraag" in st.session_state.ai_history[0]:
        converted = []
        for item in st.session_state.ai_history:
            converted.append({"role": "user", "content": item["vraag"]})
            converted.append({"role": "assistant", "content": item["antwoord"]})
        st.session_state.ai_history = converted

    chat_history_box = st.container(height=420, border=True)
    with chat_history_box:
        if not st.session_state.ai_history:
            with st.chat_message("assistant"):
                st.markdown(
                    "Hoi! Ik ben je AI Plant Coach. Stel een vraag zoals:\n"
                    "- Hoe verzorg ik lavendel?\n"
                    "- Waarom worden mijn bladeren geel?\n"
                    "- Wat kan ik aan mijn planten geven om beter te groeien?"
                )
        else:
            for msg in st.session_state.ai_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

    vraag = st.chat_input("Typ je vraag voor de AI Plant Coach...")
    if vraag:
        q_lower = vraag.lower().strip()
        abusive_terms_input = [
            "kanker",
            "kkr",
            "tering",
            "mongool",
            "idioot",
            "debiel",
            "hoer",
            "slet",
            "nigger",
            "racist",
            "homohaat",
        ]
        if any(term in q_lower for term in abusive_terms_input):
            antwoord = (
                "Ik help je graag met planten, maar hou het respectvol. "
                "Stel je vraag opnieuw in nette taal."
            )
            st.session_state.ai_history.append(
                {"role": "assistant", "content": antwoord}
            )
            st.rerun()

        st.session_state.ai_history.append({"role": "user", "content": vraag})
        with st.chat_message("user"):
            st.markdown(vraag)

        if any(ch.isdigit() for ch in vraag) and "ml" in vraag.lower():
            st.warning(
                "Tip: vermeld liever plantnaam + probleem dan exacte chemische dosissen. "
                "De coach geeft enkel veilige, algemene richtlijnen."
            )

        key_from_env = os.getenv("PLANT_AI_API_KEY", "")
        key_from_secrets = get_secret_key()
        live_key = api_key_input.strip() or key_from_env or key_from_secrets
        mode = st.session_state.ai_mode
        auto_mode = mode == "Automatisch (gebruik live AI als key gevonden is)"
        force_live = mode == "Live AI via API key"
        use_live = (auto_mode and bool(live_key)) or (force_live and bool(live_key))

        with st.spinner("AI denkt na..."):
            if use_live:
                try:
                    antwoord = ai_api_answer(
                        vraag,
                        live_key,
                        st.session_state.ai_endpoint.strip(),
                        st.session_state.ai_model.strip(),
                    )
                except Exception:
                    st.error(
                        "Live AI kon niet antwoorden. Controleer endpoint/model/key in 'AI instellingen'. "
                        "Tip: voor een gsk-key werkt Groq endpoint + model 'llama-3.1-8b-instant'."
                    )
                    antwoord = ai_plant_coach(vraag)
            else:
                antwoord = ai_plant_coach(vraag)

        st.session_state.ai_history.append(
            {"role": "assistant", "content": antwoord}
        )
        st.rerun()
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