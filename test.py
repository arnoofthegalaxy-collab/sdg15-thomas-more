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

# ── Session state init ──────────────────────────────────────────────────────
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


# ── Lokale plant coach (offline fallback) ───────────────────────────────────
def ai_plant_coach(question: str) -> str:
    q = question.lower().strip()

    if not q:
        return "Hoi! 🌿 Stel gerust een vraag, bijvoorbeeld: 'Hoe kan ik mijn munt verzorgen?'"
    if len(q) < 3:
        return "Hoi! Typ iets specifieker, bv. 'Mijn basilicum heeft gele blaadjes, wat doe ik?'"
    if len(q) > 600:
        return "Je vraag is erg lang. Maak ze korter voor een beter antwoord."

    blocked_terms = ["gif", "vergif", "bleekmiddel", "benzine", "zuur", "explosief", "bom", "self-harm", "zelfmoord"]
    abusive_terms = ["kanker", "kkr", "tering", "mongool", "idioot", "debiel", "hoer", "slet", "nigger"]
    if any(term in q for term in blocked_terms):
        return "Daar kan ik niet mee helpen. Ik geef alleen veilig en natuurvriendelijk tuinadvies 🌿"
    if any(term in q for term in abusive_terms):
        return "Laten we respectvol blijven! Stel je vraag opnieuw in nette taal 😊"

    # ── Begroeting ────────────────────────────────────────────────────────
    begroeting_words = ["hallo", "hoi", "hey", "goedemorgen", "goedemiddag", "goedenavond", "dag", "hi ", "hello"]
    if any(word in q for word in begroeting_words):
        return (
            "Hoi! Ik ben Arno, jouw persoonlijke plant coach 🌿\n\n"
            "Ik kan je helpen met alles over planten: verzorging, ziektes, plagen, water geven, "
            "bodem, snoei, stekken, kamerplanten, moestuin en nog veel meer.\n\n"
            "Stel gerust je vraag — ik help je graag! 😊"
        )

    tips = []

    # ══════════════════════════════════════════════════════════════════════
    # SPECIFIEKE PLANTEN — uitgebreide kennisbank
    # ══════════════════════════════════════════════════════════════════════
    plant_db = {
        # Kruiden
        "munt": (
            "Munt houdt van vochtige grond en gedeeltelijke schaduw. "
            "Hij verspreidt zich snel — plant hem liefst in een pot. "
            "Bij kleine zwarte of bruine beestjes (bladluizen/trips): "
            "spoel de plant af met een straaltje water, spuit daarna met verdunde groene zeep "
            "(1 theelepel op 1 liter water) om de 3 dagen. Knip zwaar aangetaste takjes weg."
        ),
        "basilicum": (
            "Basilicum houdt van warmte (min. 18°C) en volle zon. "
            "Geef water aan de basis, nooit op de bladeren. "
            "Knip bloeiende toppen weg zodat het blad blijft groeien. "
            "Gele bladeren = te veel water of te koud."
        ),
        "rozemarijn": (
            "Rozemarijn wil volle zon en droge, goed drainerende grond. "
            "Weinig water nodig — liever te droog dan te nat. "
            "Snoei na de bloei voor een compacte vorm."
        ),
        "tijm": (
            "Tijm is droogtebestendig en houdt van zon en magere grond. "
            "Geef weinig water en snoei regelmatig om hem compact te houden."
        ),
        "peterselie": (
            "Peterselie wil vochtige, voedingsrijke grond en gedeeltelijke zon. "
            "Geef regelmatig water maar vermijd wateroverlast. "
            "Oogst van buiten naar binnen zodat het hart blijft groeien."
        ),
        "koriander": (
            "Koriander schiet snel in zaad bij warmte. Plant op een koele, lichte plek. "
            "Zaai om de 3 weken opnieuw voor een continue oogst."
        ),
        "bieslook": (
            "Bieslook is heel gemakkelijk: geeft regelmatig water, staat goed in zon of halfschaduw. "
            "Knip nooit te diep — laat altijd 3-4 cm staan."
        ),
        "lavendel": (
            "Lavendel houdt van volle zon, droge grond en weinig mest. "
            "Snoei licht na de bloei maar ga nooit in het oude hout. "
            "Ideaal voor bestuivers en een natuurlijke muggenwering."
        ),
        "salie": (
            "Salie wil volle zon en droge grond. Weinig water nodig. "
            "Snoei in het voorjaar voor een frisser uiterlijk."
        ),
        "oregano": (
            "Oregano gedijt in volle zon op droge, arme grond. "
            "Weinig water, niet te bemesten. Droog de blaadjes voor intensere smaak."
        ),

        # Kamerplanten
        "monstera": (
            "Monstera houdt van indirect licht en water eens per week. "
            "Geef plantenvoeding van april tot september. "
            "Gele bladeren = te veel water. Bruine randen = te droge lucht of te weinig water."
        ),
        "pothos": (
            "Pothos is de makkelijkste kamerplant: verdraagt schaduw en droogte. "
            "Geef water als de grond droog aanvoelt. "
            "Perfect voor beginners en hangpotten."
        ),
        "cactus": (
            "Cactus heeft weinig water nodig (1x per 2-3 weken in zomer, maandelijks in winter). "
            "Veel zon en goed drainerende cactusgrond. "
            "Nooit in een pot zonder afwateringsgat."
        ),
        "vetplant": (
            "Vetplanten houden van veel zon en weinig water. "
            "Oppassen voor overgieten: wortelrot ligt op de loer. "
            "Gebruik speciale cactus/vetplantgrond."
        ),
        "orchidee": (
            "Orchideeën giet je 1x per week door onderdompeling (10 min in water). "
            "Geen directe zon, wel helder indirect licht. "
            "Na de bloei: snoei de steel net boven een knoop voor herbloeien."
        ),
        "ficus": (
            "Ficus houdt niet van verplaatsen (bladval!). "
            "Geef water als de bovenste grond droog is. Vermijd tocht en radiatorwarmte. "
            "Veeg de bladeren af voor betere fotosynthese."
        ),
        "spathiphyllum": (
            "Lepelplant wil vochtige grond en geen direct zonlicht. "
            "Hangt hij slap? Geef direct water — hij herstelt snel. "
            "Bloeit beter met meer licht."
        ),
        "sansevieria": (
            "Vrouwentong is bijna onverwoestbaar: weinig water, weinig licht, weinig aandacht. "
            "Ideaal voor beginners. Geef max. 1x per 2-3 weken water."
        ),
        "aloe vera": (
            "Aloë vera wil veel zon en weinig water. "
            "Laat de grond volledig drogen tussen twee beurten. "
            "Het gel in de bladeren werkt kalmerend op brandwonden."
        ),
        "aloe": (
            "Aloë vera wil veel zon en weinig water. "
            "Laat de grond volledig drogen tussen twee waterbeurten. "
            "Het gel in de bladeren werkt kalmerend op brandwonden."
        ),
        "calathea": (
            "Calathea is kieskeurig: wil hoge luchtvochtigheid, indirect licht en zacht (regen)water. "
            "Sproei regelmatig of zet op een schoteltje met water en kiezel."
        ),
        "fern": (
            "Varens willen constant vochtige grond en hoge luchtvochtigheid. "
            "Geen direct zonlicht. Sproei de bladeren dagelijks."
        ),
        "varen": (
            "Varens willen constant vochtige grond en hoge luchtvochtigheid. "
            "Geen direct zonlicht. Sproei de bladeren dagelijks."
        ),
        "palmlelie": (
            "Yucca (palmlelie) wil veel zon en droge grond. "
            "Weinig water nodig — verdraagt droogte uitstekend."
        ),
        "yucca": (
            "Yucca wil veel zon en droge grond. "
            "Weinig water nodig — verdraagt droogte uitstekend."
        ),
        "dracaena": (
            "Dracaena verdraagt weinig licht en weinig water. "
            "Gele bladeren = te veel water of fluoride in leidingwater — gebruik regenwater."
        ),
        "anthurium": (
            "Anthurium wil indirect licht en vochtige maar niet natte grond. "
            "Geef voeding van maart tot september. Bloeit langer bij meer licht."
        ),
        "begonia": (
            "Begonia wil licht maar geen felle zon. Geef water als de grond half droog is. "
            "Verwijder verwelkte bloemen voor langere bloeitijd."
        ),
        "strelitzia": (
            "Paradijsvogelbloem wil volle zon en matige watergift. "
            "Bloeit na 3-5 jaar. Niet te vaak verpotten — bloeit beter in kleine pot."
        ),

        # Moestuin
        "tomaat": (
            "Tomaten willen veel zon (min. 6u/dag), regelmatig water aan de basis (niet op bladeren) "
            "en een steunstok. Verwijder zijscheuten voor meer energie naar de vruchten. "
            "Geef kaliumrijke mest vanaf de bloei."
        ),
        "komkommer": (
            "Komkommer wil warmte, veel water en voedingsrijke grond. "
            "Geef dagelijks water in warme periodes. Steun de ranken aan een rek."
        ),
        "courgette": (
            "Courgette is productief maar neemt veel ruimte in. "
            "Geef regelmatig water aan de wortel, niet op het blad (schimmelgevoelig). "
            "Oogst jong voor de beste smaak."
        ),
        "sla": (
            "Sla wil koelte, vocht en halfschaduw in de zomer. "
            "Zaai om de 2 weken voor een continue oogst. Schieten door warmte = oogsten."
        ),
        "spinazie": (
            "Spinazie is een koudekruiper: zaai in voor- en najaar. "
            "Vochtige grond en geen felle zon. Schiet in zaad bij warmte."
        ),
        "wortel": (
            "Wortelen willen diepe, losse, steenvrije grond. "
            "Dunner zaaien geeft dikkere wortels. Watergift consistent houden voor rechte groei."
        ),
        "paprika": (
            "Paprika wil warmte, zon en regelmatig water. "
            "Geef voeding om de 2 weken. Binnenshuis of in serre in ons klimaat."
        ),
        "aubergine": (
            "Aubergine heeft veel warmte nodig (20-30°C). "
            "Geef regelmatig water en voeding. Bescherm tegen koude nachten."
        ),
        "prei": (
            "Prei wil vochtige, voedingsrijke grond. Plant diep voor een lang wit gedeelte. "
            "Aanaarden verhoogt de oogst."
        ),
        "ui": (
            "Uien willen volle zon en goed drainerende grond. "
            "Stop met water geven als het loof omvalt — dan zijn ze rijp."
        ),
        "knoflook": (
            "Knoflook plant je in de herfst, oogst je in de zomer. "
            "Volle zon, droge grond. Verwijder bloemstelen voor grotere bollen."
        ),
        "aardappel": (
            "Aardappelen willen losse, vruchtbare grond. "
            "Aanaarden voorkomt groene knollen. Ziek loof verwijderen bij Phytophthora."
        ),
        "aardbei": (
            "Aardbeien willen zon, vochtige grond en voeding in het groeiseizoen. "
            "Verwijder uitlopers voor grotere vruchten. Bescherm tegen slakken."
        ),
        "boon": (
            "Bonen (stamboon/stokboon) willen zon en regelmatig water. "
            "Niet te vroeg planten — geen vorst verdragen. Stokbonen hebben steun nodig."
        ),
        "erwt": (
            "Erwten zijn koudeliefhebbers: zaai vroeg in het voorjaar. "
            "Hebben steun nodig. Oogst regelmatig voor meer productie."
        ),
        "radijs": (
            "Radijs groeit snel (3-4 weken). Volle zon, vochtige grond. "
            "Oogst op tijd — te lang wachten maakt ze hol en scherp."
        ),
        "pompoen": (
            "Pompoenen willen veel ruimte, zon en voedingsrijke grond. "
            "Geef rijkelijk water en mest. Eén plant per m² is genoeg."
        ),

        # Bloemen & tuin
        "roos": (
            "Rozen bloeien beter met regelmatige snoei, organische mest en min. 6u zon per dag. "
            "Snoeien in februari/maart. Verwijder verwelkte bloemen. "
            "Bladluizen aanpakken met groene zeep of neemolie."
        ),
        "geranium": (
            "Geraniums willen veel zon en matige watergift. "
            "Laat de grond drogen tussen twee beurten. Verwijder verwelkte bloemen. "
            "Overwinteren op een koele, vorstvrije plek."
        ),
        "petunia": (
            "Petunias willen volle zon en regelmatige watergift. "
            "Geef wekelijks vloeibare mest voor langdurige bloei. Knip terug bij uitgebloeide planten."
        ),
        "zonnebloem": (
            "Zonnebloemen willen veel zon en matig water. "
            "Zaai direct in de volle grond na de laatste vorst. "
            "Diep wortelsysteem — verplaatsen na zaai is moeilijk."
        ),
        "dahlia": (
            "Dahlias willen volle zon, voedingsrijke grond en regelmatig water. "
            "Knollen bewaren vorstvrij in de winter. Uitplanten na de laatste vorst."
        ),
        "tulp": (
            "Tulpen plant je in de herfst (oktober-november). "
            "Na de bloei: laat het blad uitsterven voor sterke bollen het jaar erop. "
            "Rooien in warme, vochtige regio's."
        ),
        "narcis": (
            "Narcissen zijn makkelijk en giftig voor ongedierte. "
            "Plant in de herfst, 3x zo diep als de bol breed is. "
            "Laat het blad na de bloei uitsterven."
        ),
        "hyacint": (
            "Hyacinten willen goed drainerende grond en volle zon. "
            "Plant in de herfst. Sterk geurend en aantrekkelijk voor bestuivers."
        ),
        "hortensia": (
            "Hortensia wil halfschaduw en vochtige grond. "
            "Niet in volle middagzon. Snoeien na de bloei of in het vroege voorjaar. "
            "Blauwe bloem = zure grond; roze = basische grond."
        ),
        "viooltje": (
            "Viooltjes willen koele temperaturen en regelmatig water. "
            "Ideaal voor vroege lente en herfst. Verwijder verwelkte bloemen."
        ),
        "begonia": (
            "Begonia wil licht maar geen felle zon. "
            "Geef water als de grond half droog is. Verwijder verwelkte bloemen."
        ),
        "fuchsia": (
            "Fuchsia wil halfschaduw en regelmatige watergift. "
            "Voeden om de 2 weken voor lange bloei. Overwinteren vorstvrij."
        ),
        "heide": (
            "Heide wil zure grond, volle zon en weinig bemesting. "
            "Gebruik regenwater of bronwater — geen kalkrijk leidingwater. "
            "Snoei licht na de bloei."
        ),
        "bamboe": (
            "Bamboe groeit snel en invasief. Plant in een container of met een wortelscherm. "
            "Wil vocht en voedingsrijke grond. Gele bladeren = te weinig stikstof."
        ),
        "buxus": (
            "Buxus wil halfschaduw en vochtige grond. "
            "Snoei 2x per jaar (mei en augustus). "
            "Gevoelig voor buxusmot — controleer regelmatig en behandel met Bacillus thuringiensis."
        ),
        "klimroos": (
            "Klimrozen willen volle zon, een stevige constructie en regelmatige snoei. "
            "Snoei na de eerste bloei de zijscheuten kort in."
        ),
        "clematis": (
            "Clematis wil haar 'hoofd in de zon, voeten in de schaduw'. "
            "Plant diep (10 cm onder de grond). Snoeigroep bepaalt wanneer je snoeit."
        ),

        # Bomen & struiken
        "appelboom": (
            "Appelbomen willen volle zon en een vochtige maar goed drainerende grond. "
            "Snoei in de winter voor een goede vruchtvorming. "
            "Bescherm tegen appelschurft met goede luchtcirculatie."
        ),
        "perenboom": (
            "Perenbomen zijn gevoeliger voor vorst dan appels. "
            "Snoei in de winter, behalve bij vorst. Goed drainerende, vruchtbare grond."
        ),
        "pruimenboom": (
            "Pruimenbomen willen zon en beschutting tegen de wind. "
            "Snoei zo weinig mogelijk (gevoelig voor kanker). "
            "Rijpe vruchten snel oogsten om wespen te vermijden."
        ),
        "vijgenboom": (
            "Vijgen willen veel zon en weinig water. Ideaal in een pot op een zonnige plek. "
            "Bescherm de wortels bij strenge vorst."
        ),
        "magnolia": (
            "Magnolia wil zure, vochtige grond en beschutting tegen vroege voorjaarsnachtvorst. "
            "Niet snoein tenzij noodzakelijk."
        ),
        "hulst": (
            "Hulst is wintergroen en besdragend — goed voor vogels. "
            "Wil halfschaduw en vochtige grond. Snoei in april."
        ),
        "vlierbes": (
            "Vlier groeit snel en trekt insecten en vogels aan. "
            "Wil vochtige grond. Snoei sterk terug voor meer productie."
        ),
    }

    for plant_naam, plant_tip in plant_db.items():
        if plant_naam in q:
            tips.append(plant_tip)

    # ══════════════════════════════════════════════════════════════════════
    # PLAGEN & ZIEKTES — uitgebreid
    # ══════════════════════════════════════════════════════════════════════
    if any(word in q for word in ["zwarte beestjes", "zwart beestje", "zwarte vlieg", "zwarte luis", "zwarte insect"]):
        tips.append(
            "Zwarte beestjes zijn vaak zwarte bladluizen of trips. Aanpak:\n"
            "1) Spoel de plant krachtig af met water\n"
            "2) Spuit met verdunde groene zeep (1 tl op 1L water) om de 3 dagen\n"
            "3) Je kunt ook neemolie gebruiken (1 tl op 1L water + paar druppels afwasmiddel)\n"
            "4) Knip zwaar aangetaste takken weg en gooi ze in de vuilnisbak (niet composteren)\n"
            "5) Herhaal 2-3 weken voor volledig resultaat"
        )
    if any(word in q for word in ["bladluis", "luis", "luizen", "groene beestjes", "beestjes"]):
        tips.append(
            "Bladluizen bestrijden: spoel af met water, gebruik verdunde groene zeep of neemolie. "
            "Lieveheersbeestjes en gaasvliegen zijn natuurlijke vijanden — lok ze aan met inheemse bloemen."
        )
    if any(word in q for word in ["witte vlieg", "witte beestjes", "wittevlieg"]):
        tips.append(
            "Witte vlieg aanpakken: gebruik gele vangplaten en spuit met neemolie. "
            "Verwijder aangetaste bladeren. Vermijd overbemesting (trekt witte vlieg aan)."
        )
    if any(word in q for word in ["spintmijt", "spint", "mijt", "spinnetje", "webje"]):
        tips.append(
            "Spintmijt herkend aan fijn webje onder de bladeren. Wil droge lucht. "
            "Verhoog de luchtvochtigheid, sproei de onderkant van de bladeren. "
            "Gebruik acaricide of roofmijten als biologische bestrijding."
        )
    if any(word in q for word in ["schimmel", "meeldauw", "witziekte", "grijs schimmel", "botrytis"]):
        tips.append(
            "Schimmel bestrijden: verwijder aangetaste delen, verbeter luchtcirculatie, "
            "water aan de basis (niet op blad). Bij meeldauw: spuit met baking soda oplossing "
            "(1 tl op 1L water). Bij ernstige infectie: gebruik een koperpreparaat."
        )
    if any(word in q for word in ["slak", "slakken", "naaktslak"]):
        tips.append(
            "Slakken bestrijden zonder gif: koffiedik rondom planten strooien, "
            "eierschalen als barrière, 's avonds handmatig verwijderen. "
            "Of gebruik ijzerfosfaat-korrels (veilig voor huisdieren en egels)."
        )
    if any(word in q for word in ["rups", "rupsen", "vlinder larve", "eet mijn blad"]):
        tips.append(
            "Rupsen handmatig verwijderen 's avonds. "
            "Spuit met Bacillus thuringiensis (Bt) — biologisch en veilig. "
            "Stimuleer vogels in de tuin als natuurlijke vijanden."
        )
    if any(word in q for word in ["aaltje", "nematode", "wortelrot", "wortel rot"]):
        tips.append(
            "Wortelrot door aaltjes of schimmel: verbeter de drainage, "
            "gebruik nematoden als biologische bestrijding bij aaltjesproblemen. "
            "Verwijder en vernietig aangetaste planten."
        )
    if any(word in q for word in ["mier", "mieren"]):
        tips.append(
            "Mieren zelf zijn vaak geen probleem, maar wijzen op bladluizen (ze 'hoeden' de luizen). "
            "Bestrijdt de bladluizen en de mieren verdwijnen vanzelf. "
            "Barrière: koffiedik of krijt rondom de pot."
        )
    if any(word in q for word in ["trips", "tripsen"]):
        tips.append(
            "Trips veroorzaken zilverachtige vlekjes op bladeren. "
            "Gebruik blauwe of gele vangplaten. Spuit met neemolie. "
            "Hoge luchtvochtigheid helpt trips afschrikken."
        )
    if any(word in q for word in ["buxusmot", "buxus mot", "rupsen buxus"]):
        tips.append(
            "Buxusmot bestrijden met Bacillus thuringiensis (Bt-spray). "
            "Controleer regelmatig — vroegtijdig ingrijpen is cruciaal. "
            "Behandel 2-3x met 1-2 weken tussentijd."
        )

    # ══════════════════════════════════════════════════════════════════════
    # SYMPTOMEN
    # ══════════════════════════════════════════════════════════════════════
    if any(word in q for word in ["geel", "gele bladeren", "vergeelt", "blad wordt geel"]):
        tips.append(
            "Gele bladeren kunnen betekenen:\n"
            "- Te veel water (meest voorkomend): voel de grond, laat drogen\n"
            "- Te weinig licht: verplaats naar lichtere plek\n"
            "- Tekort aan voeding: geef plantenvoeding\n"
            "- Natuurlijk: onderste oude bladeren worden soms geel — dat is normaal"
        )
    if any(word in q for word in ["bruin", "bruine punten", "bruine randen", "droge punt"]):
        tips.append(
            "Bruine bladpunten of randen: "
            "vaak te droge lucht, te weinig water, of overmatige bemesting. "
            "Sproei de bladeren, geef meer water of spoel de grond door om zoutophoping weg te spoelen."
        )
    if any(word in q for word in ["slap", "hangt", "laat los", "valt om", "verwelkt"]):
        tips.append(
            "Slappe plant: check eerst de grond. "
            "Droog → geef direct water. "
            "Nat → wortelrot mogelijk — laat drogen en controleer de wortels (gezond = wit, rot = bruin/zacht)."
        )
    if any(word in q for word in ["vlekken", "bruine vlekken", "zwarte vlekken", "gele vlekken"]):
        tips.append(
            "Vlekken op bladeren: "
            "gele vlekken = schimmel of bacterie; bruine vlekken = zonnebrand of schimmel; "
            "zwarte vlekken = bacteriële infectie. "
            "Verwijder aangetaste bladeren, verbeter luchtcirculatie en vermijd water op de bladeren."
        )
    if any(word in q for word in ["bloeit niet", "geen bloemen", "niet bloeiend"]):
        tips.append(
            "Plant bloeit niet: "
            "vaak te weinig licht, te veel stikstofmest (geef meer kalium/fosfaat), "
            "te jonge plant, of verkeerde rust-periode. "
            "Zet op een zonnigere plek en gebruik bloeibevorderende mest."
        )
    if any(word in q for word in ["blad valt", "bladval", "verliest bladeren"]):
        tips.append(
            "Bladval: tocht, temperatuurwisselingen, te weinig licht of verplaatsing zijn veelvoorkomende oorzaken. "
            "Zet de plant op een stabiele, lichte plek zonder tocht."
        )

    # ══════════════════════════════════════════════════════════════════════
    # VERZORGING ALGEMEEN
    # ══════════════════════════════════════════════════════════════════════
    if any(word in q for word in ["water", "gieten", "hoeveel water", "wanneer water", "droog", "te nat"]):
        tips.append(
            "Watergift-regel: steek je vinger 2-3 cm in de grond. "
            "Droog → water geven. Vochtig → wachten. "
            "Geef liever minder vaak maar grondig dan elke dag een beetje."
        )
    if any(word in q for word in ["mest", "voeding", "plantenvoeding", "bemesten", "voedingsstoffen"]):
        tips.append(
            "Bemesting: gebruik in het groeiseizoen (maart-september) organische of vloeibare mest om de 2-4 weken. "
            "In de winter niet of nauwelijks mesten. Overbemesting geeft verbrande wortels."
        )
    if any(word in q for word in ["snoei", "snoeien", "snijden", "terugknippen"]):
        tips.append(
            "Snoeien: gebruik altijd schoon, scherp gereedschap. "
            "Snoei bloeiende struiken na de bloei. "
            "Fruit- en sierbomen in de winter (januari-februari) als ze in rust zijn."
        )
    if any(word in q for word in ["stek", "stekken", "vermeerderen", "nieuwe plant"]):
        tips.append(
            "Stekken: knip een gezond stuk van 10-15 cm, verwijder onderste bladeren, "
            "en zet in water of vochtige stekgrond. "
            "Dek af met een plastic zak voor hoge luchtvochtigheid. "
            "Wortels verschijnen na 2-6 weken."
        )
    if any(word in q for word in ["verpot", "verpotten", "pot te klein", "nieuwe pot"]):
        tips.append(
            "Verpotten: doe dit in het voorjaar. "
            "Kies een pot die 2-3 cm groter is. "
            "Gebruik verse potgrond. Water geven na het verpotten."
        )
    if any(word in q for word in ["bodem", "grond", "aarde", "potgrond", "substraat"]):
        tips.append(
            "Goede bodem: voeg compost toe voor vruchtbaarheid en waterretentie. "
            "Gebruik luchtige potgrond voor kamerplanten. "
            "Voor cactussen/vetplanten: cactusgrond met extra perlite."
        )
    if any(word in q for word in ["licht", "zon", "schaduw", "donker", "vensterbank"]):
        tips.append(
            "Licht: de meeste planten willen helder indirect licht. "
            "Volle zon = min. 6u directe zon. Halfschaduw = 2-4u. "
            "Draai kamerplanten regelmatig voor gelijkmatige groei."
        )
    if any(word in q for word in ["winter", "overwinteren", "vorst", "koude"]):
        tips.append(
            "Overwinteren: haal vorstgevoelige planten binnen bij <5°C. "
            "Minder water geven in de winter. "
            "Koud maar vorstvrij overwinteren (5-10°C) is ideaal voor veel mediterrane planten."
        )
    if any(word in q for word in ["zaad", "zaaien", "kiemen", "zaaigoed"]):
        tips.append(
            "Zaaien: gebruik verse, lichte zaaigrond. "
            "Houd vochtig en warm (18-22°C) tot ontkieming. "
            "Dun uit zodra zaailingen 2 echte blaadjes hebben."
        )
    if any(word in q for word in ["bij", "vlinder", "bestuiver", "biodiversiteit", "insect vriend"]):
        tips.append(
            "Bestuivers aantrekken: plant inheemse soorten, varieer in bloeitijd (van maart tot oktober), "
            "vermijd pesticiden en laat een wilde hoek in de tuin."
        )
    if any(word in q for word in ["composteren", "compost", "afval", "organisch"]):
        tips.append(
            "Compost: vermeng 'bruine' materialen (droog blad, karton) met 'groene' (keukenresten, gras). "
            "Houd vochtig en keer regelmatig om. Na 3-6 maanden heb je rijke compost."
        )
    if any(word in q for word in ["luchtvochtigheid", "te droge lucht", "sproei"]):
        tips.append(
            "Luchtvochtigheid verhogen: sproei de bladeren 's ochtends, "
            "zet de pot op een schoteltje met water en kiezel, "
            "of gebruik een luchtbevochtiger in de buurt van de plant."
        )

    if not tips:
        return (
            "Hoi! Ik ben Arno, jouw plant coach 🌿\n\n"
            "Ik kon je vraag niet direct koppelen aan een specifiek onderwerp. "
            "Voor het beste antwoord, vertel me:\n"
            "- **Welke plant** heb je?\n"
            "- **Wat zie je** precies (gele bladeren, beestjes, slappe stengel, vlekken...)?\n"
            "- **Waar staat** de plant (binnen/buiten, zon/schaduw)?\n"
            "- **Hoe vaak** geef je water en mest?\n\n"
            "Dan geef ik je een concreet en persoonlijk advies! 💚"
        )

    antwoord = "Hier is mijn advies voor jou 🌿\n\n"
    for tip in tips:
        if "\n" in tip:
            antwoord += tip + "\n\n"
        else:
            antwoord += f"- {tip}\n"
    antwoord += "\nKleine moeite, groot verschil voor je plant! Succes 💚"
    return antwoord


# ── Live AI via API ──────────────────────────────────────────────────────────
def resolve_ai_settings(api_key: str, endpoint: str, model: str) -> tuple[str, str]:
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
                    "Je bent Arno, een warme, enthousiaste en deskundige AI plant coach voor SDG 15. "
                    "Je hebt uitgebreide kennis over ALLE aspecten van plantenteelt en -verzorging:\n"
                    "- Kamerplanten (monstera, pothos, orchidee, cactus, vetplanten, varens, etc.)\n"
                    "- Moestuinplanten (tomaat, courgette, sla, kruiden, aardappelen, etc.)\n"
                    "- Tuinplanten (rozen, vaste planten, struiken, bomen, klimplanten)\n"
                    "- Kruiden (basilicum, munt, rozemarijn, tijm, koriander, lavendel, etc.)\n"
                    "- Plagen en ziektes (bladluizen, spintmijt, schimmel, meeldauw, slakken, rupsen)\n"
                    "- Verzorging (water, mest, snoei, verpotten, stekken, zaaien)\n"
                    "- Bodem en compost\n"
                    "- Biodiversiteit en inheemse planten\n"
                    "- Seizoenszorg en overwinteren\n\n"
                    "Gedragsregels:\n"
                    "1. Begin het EERSTE bericht van een gesprek altijd met: 'Hoi! Ik ben Arno, jouw plant coach 🌿'\n"
                    "2. Gebruik een warme, vriendelijke en aanmoedigende toon\n"
                    "3. Geef ALTIJD een concreet antwoord, ook als de vraag vaag is — vraag dan 1-2 verduidelijkingen NA je antwoord\n"
                    "4. Structureer antwoorden met duidelijke stappen (gebruik cijfers of bullets)\n"
                    "5. Geef bij een plaagprobleem altijd: identificatie + directe aanpak + preventie\n"
                    "6. Eindig met een korte bemoediging of tip\n"
                    "7. Maximum 8 bullets of stappen per antwoord\n"
                    "8. Geef NOOIT gevaarlijke, toxische of schadelijke adviezen\n"
                    "9. Weiger respectloos taalgebruik vriendelijk maar duidelijk\n"
                    "10. Antwoord altijd in eenvoudig Nederlands"
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


# ── Sidebar ──────────────────────────────────────────────────────────────────
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

# ── Hero ─────────────────────────────────────────────────────────────────────
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

# ── KPI's ────────────────────────────────────────────────────────────────────
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

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(
    ["Biodiversiteitsscan", "Actieplanner", "Natuurdagboek", "AI Plant Coach"]
)

# ── Tab 1: Biodiversiteitsscan ────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Scan jouw tuin, straat of schoolomgeving")
    c1, c2 = st.columns(2)
    with c1:
        groen_pct = st.slider("Hoeveel % van de zone is groen?", 0, 100, 35)
        inheemse_planten = st.slider("Hoeveel verschillende lokale planten zie je?", 0, 40, 8)
        bomen = st.slider("Aantal bomen", 0, 30, 3)
    with c2:
        pesticide = st.selectbox("Gebruik je pesticiden?", ["Nooit", "Soms", "Vaak"])
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
        label, kleur = "Sterk ecosysteem", "success"
    elif score >= 40:
        label, kleur = "Gemiddeld ecosysteem", "warning"
    else:
        label, kleur = "Kwetsbaar ecosysteem", "error"

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

# ── Tab 2: Actieplanner ───────────────────────────────────────────────────────
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

# ── Tab 3: Natuurdagboek ──────────────────────────────────────────────────────
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

# ── Tab 4: AI Plant Coach (Arno) ──────────────────────────────────────────────
with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🌿 Arno — AI Plant Coach")
    st.info(
        "Hoe werkt Arno? 1) Typ je plantenvraag. 2) Druk op Enter. "
        "3) Arno geeft direct praktisch advies over jouw plant, plaag of probleem."
    )
    st.write(
        "Stel Arno een vraag over planten, plagen, ziektes, water geven, bodem of biodiversiteit. "
        "Hij kent kruiden, kamerplanten, moestuinplanten, bomen en struiken."
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
                0 if st.session_state.ai_mode == "Automatisch (gebruik live AI als key gevonden is)"
                else (1 if st.session_state.ai_mode == "Live AI via API key" else 2)
            ),
        )
        st.session_state.ai_endpoint = st.text_input(
            "API endpoint",
            value=st.session_state.ai_endpoint,
            help="OpenRouter: https://openrouter.ai/api/v1/chat/completions | Groq: https://api.groq.com/openai/v1/chat/completions",
        )
        st.session_state.ai_model = st.text_input(
            "Model",
            value=st.session_state.ai_model,
            help="Voorbeeld: openai/gpt-4o-mini of llama-3.1-8b-instant (Groq)",
        )
        api_key_input = st.text_input(
            "API key",
            type="password",
            help="Je key wordt enkel in deze sessie gebruikt.",
        )
        st.caption("Met key gebruikt de app live AI. Zonder key valt hij terug op de lokale Arno-coach.")

    if st.button("Wis chatgeschiedenis", use_container_width=True):
        st.session_state.ai_history = []
        st.success("Chatgeschiedenis gewist.")

    # Backward-compatible conversie van oude structuur
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
                    "Hoi! Ik ben Arno, jouw plant coach 🌿\n\n"
                    "Stel me een vraag zoals:\n"
                    "- Mijn munt is geïnfecteerd met kleine zwarte beestjes, wat doe ik?\n"
                    "- Waarom worden de bladeren van mijn monstera geel?\n"
                    "- Hoe verzorg ik een orchidee?\n"
                    "- Wanneer moet ik mijn tomaten snoeien?\n\n"
                    "Ik help je graag! 💚"
                )
        else:
            for msg in st.session_state.ai_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

    vraag = st.chat_input("Stel Arno een plantenvraag...")
    if vraag:
        q_lower = vraag.lower().strip()
        abusive_terms_input = ["kanker", "kkr", "tering", "mongool", "idioot", "debiel", "hoer", "slet"]
        if any(term in q_lower for term in abusive_terms_input):
            antwoord = (
                "Ik help je graag met planten, maar hou het respectvol 😊 "
                "Stel je vraag opnieuw in nette taal."
            )
            st.session_state.ai_history.append({"role": "assistant", "content": antwoord})
            st.rerun()

        st.session_state.ai_history.append({"role": "user", "content": vraag})
        with st.chat_message("user"):
            st.markdown(vraag)

        key_from_env = os.getenv("PLANT_AI_API_KEY", "")
        key_from_secrets = get_secret_key()
        live_key = api_key_input.strip() if "api_key_input" in dir() else ""
        live_key = live_key or key_from_env or key_from_secrets
        mode = st.session_state.ai_mode
        auto_mode = mode == "Automatisch (gebruik live AI als key gevonden is)"
        force_live = mode == "Live AI via API key"
        use_live = (auto_mode and bool(live_key)) or (force_live and bool(live_key))

        with st.spinner("Arno denkt na... 🌿"):
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

        st.session_state.ai_history.append({"role": "assistant", "content": antwoord})
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ── Bottom cards ──────────────────────────────────────────────────────────────
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

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Thomas More Design Notes")
c1, c2, c3 = st.columns(3)
c1.info("Kleuren: roodtinten in Thomas More stijl")
c2.info("Heldere kaarten en afgeronde UI")
c3.info("Interactieve elementen voor showcase")

st.caption(
    "Gemaakt voor de projectfase 'Van Ontwerp naar App' met Streamlit en een Thomas More look & feel."
)