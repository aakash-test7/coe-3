import streamlit as st
st.set_page_config(page_title="CicerOmicsExplorer", layout="wide",initial_sidebar_state="expanded")
from streamlit_navigation_bar import st_navbar
import pages as pg
import time
from pages.security_login import basic_stats, update_visitor_count

pages = ["HOME", "SEARCH", "GENE-INFO", "SPATIAL EXPRESSION", "RNA", "miRNA", "PPI", "LOCALIZATION", "GO-KEGG", "SNP", "ORTHOLOGS", "ABOUT US", "LOGIN"]
logo_path = ("logo.svg")
#urls = {"MDU": "https://mdu.ac.in/default.aspx"}
options={"use_padding": True, "show_menu":False}

styles = {
    "nav": {
        "background-color": "rgb(185, 214, 148)",  # Background color of the navigation bar
        "height": "4rem",  # Set the total height of the navigation bar
        "display": "flex",  # Use flexbox for layout
        "align-items": "center",  # Vertically center the items
        "justify-content": "space-between",
        "padding": "0 1rem",  # Add padding to the left and right of the navigation bar
        "overflow-x": "auto",  # Enable horizontal scrolling if the content overflows
        "white-space": "nowrap",  # Prevent items from wrapping to a new line
    },
    "div": {
        "width": "100%",
    },
    "span": {
        "border-radius": "0.5rem",  # Rounded corners for the headings
        "color": "rgb(49, 51, 63)",  # Text color of the headings
        "margin": "0 0.125rem",  # Margin around each heading
        "padding": "0.4375rem 0.625rem",  # Padding inside each heading
        "font-size": "1.1rem",  # Increase the font size of the headings
        "font-weight": "bold",  # Make the headings bold
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",  # Background color for the active heading
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",  # Background color on hover
    },
}

#st.markdown("""<style>.stApp {padding-top: 6rem !important;}</style>""", unsafe_allow_html=True)
if "current_page" not in st.session_state:
    st.session_state.current_page = "HOME"  # Default to Home page on first load
page = st_navbar(pages, logo_path=logo_path, styles=styles, options=options,logo_page="HOME")

# Logic for redirecting to login or setting pages
if st.session_state.get("redirect_to_login", False):
    st.session_state.current_page = "LOGIN"  # Redirect to Login page
elif st.session_state.get("redirected_to_login", True) is False:
    if "first_time" not in st.session_state or st.session_state.first_time:  # Check if it's the first time
        st.session_state.current_page = "SEARCH"  # First-time visit after redirect should go to Search page
        st.session_state.first_time = False  # Set first_time to False after first visit
else:
    # Set the current page to the selected page from the navbar
    if page != st.session_state.current_page:
        st.session_state.current_page = page

external_links = {
    "NCBI": "https://www.ncbi.nlm.nih.gov/",
    "Phytozome": "https://phytozome-next.jgi.doe.gov/",
    "Ensemble Plants": "https://plants.ensembl.org/index.html",
    "Gramene": "https://www.gramene.org/",
    "Legume Information System": "https://www.legumeinfo.org/",
    "Pulse Crop Database": "https://www.pulsedb.org/main",
    "GrainGenes": "https://wheat.pw.usda.gov/",
    "TAIR": "https://www.arabidopsis.org",
    "Rice Database": "https://shigen.nig.ac.jp/rice/oryzabase/locale/change?lang=en",
    "MaizeGDB": "https://www.maizegdb.org/",
    "SoyBase": "https://www.soybase.org/",
    "Cassavabase": "https://www.cassavabase.org"}

st.sidebar.title("Important Resources")
for name, link in external_links.items():
    st.sidebar.markdown(
f'<a href="{link}" target="_blank" class="sidebar-button" style="text-decoration: none; background-color: rgb(255, 119, 75); color: black;" onmouseover="this.style.textDecoration=\'none\'; this.style.color=\'black\';" onmouseout="this.style.textDecoration=\'none\'; this.style.color=\'black\';">{name}</a>',
        unsafe_allow_html=True)
    

#visitor
if 'first_access' not in st.session_state:
    st.session_state.first_access = True
if 'visitor_count' not in st.session_state:
    st.session_state.visitor_count = 0
if 'display_count' not in st.session_state:
    st.session_state.display_count = True

if st.session_state.first_access:
    st.session_state.visitor_count = update_visitor_count()
    st.session_state.member, st.session_state.search=basic_stats() #change

if st.session_state.display_count:
    st.toast(f"Visitor Count : {st.session_state.visitor_count}")
    st.session_state.display_count = False

#metric=st.sidebar.metric(value=st.session_state.visitor_count,label="Total Visitors",border=True,)
visitor_placeholder = st.sidebar.empty()

if st.session_state.get("authenticated",False): #logout
    visitor_placeholder.metric(value=st.session_state.visitor_count, label="Total Visitors", border=True)
    col1,col2=st.sidebar.columns(2)
    member_placeholder = col1.empty()
    search_placeholder = col2.empty()
    if st.sidebar.button("Site Sync"):
        st.session_state.member, st.session_state.search=basic_stats()
        st.session_state.visitor_count = update_visitor_count()
        #st.sidebar.subheader(f"Total Visitors : {visitor_count}")  #change
        visitor_placeholder.metric(value=st.session_state.visitor_count, label="Total Visitors", border=True)
    #col1,col2=st.sidebar.columns(2)
    #col1.metric(value=st.session_state.member,label="Total Members",delta=None,border=True,)    #change
    #col2.metric(value=st.session_state.search,label="Total Searches",delta=None,border=True,)    #change
    member_placeholder.metric(value=st.session_state.member, label="Total Members", delta=None, border=True)
    search_placeholder.metric(value=st.session_state.search, label="Total Searches", delta=None, border=True)
    if st.sidebar.button("Logout",key="logout_sidebar"):
        st.session_state["logged_in"] = False
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
        st.success("You have been logged out successfully!")
        time.sleep(2)
        st.rerun()

else:
    visitor_placeholder.metric(value=st.session_state.visitor_count, label="Total Visitors", border=True)

    if st.sidebar.button("Site Sync", key="non-member"):
        st.session_state.visitor_count = update_visitor_count()
        #st.sidebar.subheader(f"Total Visitors : {visitor_count}")  #change
        visitor_placeholder.metric(value=st.session_state.visitor_count, label="Total Visitors", border=True)
        st.toast(f"Total visitors: {st.session_state.visitor_count}")

#st.sidebar.markdown("---")  # Adds a separator
st.markdown(
    """
    <style>
        @media (max-width: 900px) {
            .stNavBar-nav {
                overflow-x: scroll;  /* Enable scrolling on smaller screens */
                flex-wrap: nowrap;    /* Prevent wrapping of items */
                padding: 0.5rem;      /* Adjust padding for mobile */
            }
            .stNavBar-span {
                font-size: 0.9rem;      /* Slightly reduce font size for mobile */
            }
        }
        .sidebar-button, .stButton>button {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            color: black;
            background-color: #C3D8A1; /* Green */
            border: 2px solid #9CAD81;
            border-radius: 15px;
            cursor: pointer;
            margin-bottom: 5px;
            text-align: center;
            display: block;
            text-decoration: none;
            transition: all 0.3 ease;
        }

        .sidebar-button:hover, .stButton>button:hover {
            background-color: rgb(255, 119, 75);
            border-color: #2d2d2d;
        }

        .stButton>button:hover p {
            color: black !important; /* Keep text visible */
        }
    </style>
    """,
    unsafe_allow_html=True,
)
functions = {
    "HOME": pg.home_page,
    "SEARCH": pg.search_page,
    "GENE-INFO": pg.gene_info_page,
    "SPATIAL EXPRESSION": pg.spatial_info_page,
    "RNA": pg.rna_type_page,
    "miRNA": pg.mirna_info_page,
    "PPI": pg.ppi_info_page,
    "LOCALIZATION": pg.local_info_page,
    "GO-KEGG": pg.go_info_page,
    "SNP": pg.snp_info_page,
    "ORTHOLOGS": pg.orthologs_info_page,
    "ABOUT US": pg.about_page,
    "LOGIN": pg.login_page
}

go_to = functions.get(st.session_state.current_page)
if go_to:
    go_to()
