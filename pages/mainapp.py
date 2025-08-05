import pymysql
import streamlit as st
import re
import time
import pandas as pd
from backend import user_input_menu, multi_user_input_menu, process_locid, process_mlocid
from backend import generate_signed_url, svm_charts, tsi_plot
import requests
from backend import img_to_base64
from streamlit.components.v1 import html

# ✅ Cache image fetching and base64 conversion
@st.cache_data(show_spinner=False)
def get_footer_image_base64():
    file_url = generate_signed_url('Logos/mdu.png')
    response = requests.get(file_url)
    return img_to_base64(response.content)

# ✅ Footer rendering function
def base_footer():
    img_base64 = get_footer_image_base64()
    footer_image = f"data:image/png;base64,{img_base64}"

    footer = f"""
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        html, body {{
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Poppins', sans-serif;
            background: #eef8ff;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }}

        main {{
            flex: 1;
        }}

        .footer-container {{
            width: 100%;
            background: #000000;
            color: #fff;
            bottom: 0;
            left: 0;
            padding: 20px 0;
            z-index: 9999;
            border-radius: 15px;
            overflow: hidden;
            display: flex;
            justify-content: space-evenly;
            align-items: flex-start;
            flex-wrap: wrap;
        }}

        .container {{
            width: 100%;
            margin: 0;
            padding: 0 20px;
            display: flex;
            justify-content: space-evenly;
            align-items: flex-start;
            flex-wrap: wrap;
        }}

        .container li a:hover {{
            color: #b9d694;
            transition: all 0.5s ease;
        }}

        .col-1 {{
            flex-basis: 50%;
            padding: 5px;
            margin-bottom: 20px;
        }}

        .col-1 img {{
            width: 55px;
            margin-bottom: 15px;
        }}

        .col-1 p {{
            color: #fff;
            font-size: 16px;
            line-height: 20px;
        }}

        .col-3 {{
            flex-basis: 15%;
            padding: 5px;
            margin-bottom: 2px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }}

        .special {{
            color: #fff;
            font-size: 25px;
            margin-top: 10px;
            margin-bottom: 10px;
        }}

        .col-3 img {{
            width: 125px;
            height: auto;
            min-width: 125px;
        }}

        .container a {{
            color: #fff;
        }}

        .container a:hover {{
            color: #b9d694;
            transition: all 0.5s ease;
        }}

        .footer-2 {{
            width: 100%;
            background: #2d2d2d;
            color: #fff;
            padding-top: 12px;
            padding-bottom: 2px;
            text-align: center;
        }}
    </style>

    <div class="footer-container">
        <div class="container">
            <div class="col-1">
                <p><br><br><br>Stress Physiology & Molecular Biology Lab,<br>
                Centre for Biotechnology,<br>
                Maharshi Dayanand University,<br> Rohtak, HR, INDIA<br>
                E-mail: <a href="mailto:ssgill14@mdurohtak.ac.in" style="text-decoration: none;">ssgill14@mdurohtak.ac.in</a><br>
                E-mail: <a href="mailto:kduiet@mdurohtak.ac.in" style="text-decoration: none;">kduiet@mdurohtak.ac.in</a>
                </p>
            </div>
            <div class="col-3">
                <a href="https://mdu.ac.in/default.aspx" class="special" style="text-decoration: none;" target="_blank">MDU</a>
                <img src="{footer_image}" alt="mdu">
            </div>
        </div>
        <div class="footer-2">
            <p style="font-size: 15px">CicerOmicsExplorer</p>
        </div>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
    return

def citations_page():
    st.title("Citations")
    
    con = st.container(border=True)
    con.write("### Orthologous analysis:")
    con.write("OrthoVenn3 (2022) - https://orthovenn3.bioinfotoolkits.net/") 
    con.write("Contact: yiwang28@swu.edu.cn")

    con = st.container(border=True)
    con.write("### Sequences:")
    con.write("Phytozome v13 - https://phytozome-next.jgi.doe.gov/")
    con.write("David M. Goodstein, Shengqiang Shu, Russell Howson, Rochak Neupane, Richard D. Hayes, Joni Fazo, Therese Mitros, William Dirks, Uffe Hellsten, Nicholas Putnam, and Daniel S. Rokhsar, Phytozome: a comparative platform for green plant genomics, Nucleic Acids Res. 2012 40 (D1): D1178-D1186.")
    
    con = st.container(border=True)
    con.write("### SNP Calling:")
    con.write("https://cegresources.icrisat.org/cicerseq/")
    con.write("""
    <p>Dr. Rajeev Varshney<br>
    Research Program Director – Genetic Gains, Center of Excellence in Genomics & Systems Biology,<br>
    Building # 300, ICRISAT, Patancheru, 502 324, Telangana, India.<br>
    Office: +91 40 3071 3397<br>
    Email: <a href="mailto:r.k.varshney@cgiar.org">r.k.varshney@cgiar.org</a></p>
""", unsafe_allow_html=True)
    #con.write("TY  - JOUR\nAU  - Toronto International Data Release Workshop Authors\nPY  - 2009\nDA  - 2009/09/01\nTI  - Prepublication data sharing\nJO  - Nature\nSP  - 168\nEP  - 170\nVL  - 461\nIS  - 7261\nAB  - Rapid release of prepublication data has served the field of genomics well. Attendees at a workshop in Toronto recommend extending the practice to other biological data sets.\nSN  - 1476-4687\nUR  - https://doi.org/10.1038/461168a\nDO  - 10.1038/461168a\nID  - Toronto International Data Release Workshop Authors2009\nER  - \nPrepublication Data Sharing:\nToronto International Data Release Workshop Authors (2009), Nature 461:168-170, https://doi.org/10.1038/461168a.")
    con.write("""
    <p>TY  - JOUR<br>
    AU  - Toronto International Data Release Workshop Authors<br>
    PY  - 2009<br>
    DA  - 2009/09/01<br>
    TI  - Prepublication data sharing<br>
    JO  - Nature<br>
    SP  - 168<br>
    EP  - 170<br>
    VL  - 461<br>
    IS  - 7261<br>
    AB  - Rapid release of prepublication data has served the field of genomics well. Attendees at a workshop in Toronto recommend extending the practice to other biological data sets.<br>
    SN  - 1476-4687<br>
    UR  - <a href="https://doi.org/10.1038/461168a" target="_blank">https://doi.org/10.1038/461168a</a><br>
    DO  - 10.1038/461168a<br>
    ID  - Toronto International Data Release Workshop Authors2009<br>
    ER  -<br>
    </p>
    <p>Prepublication Data Sharing:<br>
    Toronto International Data Release Workshop Authors (2009), Nature 461:168-170, <a href="https://doi.org/10.1038/461168a" target="_blank">https://doi.org/10.1038/461168a</a></p>
""", unsafe_allow_html=True)

    con = st.container(border=True)
    con.write("### Cellular Localization:")
    con.write("CELLO v.2.5: subCELlular Localization predictor - http://cello.life.nctu.edu.tw/")
    con.write("(1) Yu CS, Lin CJ, Hwang JK: Predicting subcellular localization of proteins for Gram-negative bacteria by support vector machines based on n-peptide compositions. Protein Science 2004, 13:1402-1406.")
    con.write("(2) Yu CS, Chen YC, Lu CH, Hwang JK, Proteins: Structure, Function and Bioinformatics, 2006, 64:643-651.")

    con = st.container(border=True)
    con.write("### Protein-Protein Interactions (PPI):")
    con.write("STRING v12.0 - https://string-db.org/")
    con.write("Szklarczyk D, Kirsch R, Koutrouli M, Nastou K, Mehryary F, Hachilif R, Annika GL, Fang T, Doncheva NT, Pyysalo S, Bork P‡, Jensen LJ‡, von Mering C‡.\
    The STRING database in 2023: protein-protein association networks and functional enrichment analyses for any sequenced genome of interest.\
    Nucleic Acids Res. 2023 Jan 6;51(D1):D638-646.PubMed")
    con.write("Szklarczyk D*, Gable AL*, Nastou KC, Lyon D, Kirsch R, Pyysalo S, Doncheva NT, Legeay M, Fang T, Bork P‡, Jensen LJ‡, von Mering C‡.\
    The STRING database in 2021: customizable protein-protein networks, and functional characterization of user-uploaded gene/measurement sets.\
    Nucleic Acids Res. 2021 Jan 8;49(D1):D605-12.PubMed")
    con.write("Szklarczyk D, Gable AL, Lyon D, Junge A, Wyder S, Huerta-Cepas J, Simonovic M, Doncheva NT, Morris JH, Bork P‡, Jensen LJ‡, von Mering C‡.\
    STRING v11: protein-protein association networks with increased coverage, supporting functional discovery in genome-wide experimental datasets.\
    Nucleic Acids Res. 2019 Jan; 47:D607-613.PubMed")
    con.write("Szklarczyk D, Morris JH, Cook H, Kuhn M, Wyder S, Simonovic M, Santos A, Doncheva NT, Roth A, Bork P‡, Jensen LJ‡, von Mering C‡.\
    The STRING database in 2017: quality-controlled protein-protein association networks, made broadly accessible.\
    Nucleic Acids Res. 2017 Jan; 45:D362-68.PubMed")
    con.write("Szklarczyk D, Franceschini A, Wyder S, Forslund K, Heller D, Huerta-Cepas J, Simonovic M, Roth A, Santos A, Tsafou KP, Kuhn M, Bork P‡, Jensen LJ‡, von Mering C‡.\
    STRING v10: protein-protein interaction networks, integrated over the tree of life.\
    Nucleic Acids Res. 2015 Jan; 43:D447-52.PubMed")
    con.write("Franceschini A, Lin J, von Mering C, Jensen LJ‡.\
    SVD-phy: improved prediction of protein functional associations through singular value decomposition of phylogenetic profiles.\
    Bioinformatics. 2015 Nov; btv696.PubMed")
    con.write("Franceschini A*, Szklarczyk D*, Frankild S*, Kuhn M, Simonovic M, Roth A, Lin J, Minguez P, Bork P‡, von Mering C‡, Jensen LJ‡.\
    STRING v9.1: protein-protein interaction networks, with increased coverage and integration.\
    Nucleic Acids Res. 2013 Jan; 41:D808-15.PubMed")
    con.write("Szklarczyk D*, Franceschini A*, Kuhn M*, Simonovic M, Roth A, Minguez P, Doerks T, Stark M, Muller J, Bork P‡, Jensen LJ‡, von Mering C‡.\
    The STRING database in 2011: functional interaction networks of proteins, globally integrated and scored.\
    Nucleic Acids Res. 2011 Jan; 39:D561-8.PubMed")
    con.write("Jensen LJ*, Kuhn M*, Stark M, Chaffron S, Creevey C, Muller J, Doerks T, Julien P, Roth A, Simonovic M, Bork P‡, von Mering C‡.\
    STRING 8--a global view on proteins and their functional interactions in 630 organisms.\
    Nucleic Acids Res. 2009 Jan; 37:D412-6.PubMed")
    con.write("von Mering C*, Jensen LJ*, Kuhn M, Chaffron S, Doerks T, Krueger B, Snel B, Bork P‡.\
    STRING 7--recent developments in the integration and prediction of protein interactions.\
    Nucleic Acids Res. 2007 Jan; 35:D358-62.PubMed")
    con.write("von Mering C, Jensen LJ, Snel B, Hooper SD, Krupp M, Foglierini M, Jouffre N, Huynen MA, Bork P‡.\
    STRING: known and predicted protein-protein associations, integrated and transferred across organisms.\
    Nucleic Acids Res. 2005 Jan; 33:D433-7.PubMed")
    con.write("von Mering C, Huynen M, Jaeggi D, Schmidt S, Bork P‡, Snel B.\
    STRING: a database of predicted functional associations between proteins.\
    Nucleic Acids Res. 2003 Jan; 31:258-61.PubMed")
    con.write("Snel B‡, Lehmann G, Bork P, Huynen MA.\
    STRING: a web-server to retrieve and display the repeatedly occurring neighbourhood of a gene.\
    Nucleic Acids Res. 2000 Sep 15;28(18):3442-4.PubMed")
    con.write("*contributed equally\
    ‡corresponding author")

    con = st.container(border=True)
    con.write("### PROMOTER Analysis:")
    con.write("PlantCARE, a database of plant cis-acting regulatory elements - http://bioinformatics.psb.ugent.be/webtools/plantcare/html/")
    con.write("Reference to PlantCARE:\
    PlantCARE, a database of plant cis-acting regulatory elements and a portal to tools for in silico analysis of promoter sequences\
    Magali Lescot, Patrice Dhais, Gert Thijs, Kathleen Marchal, Yves Moreau, Yves Van de Peer, Pierre Rouz and Stephane Rombauts\
    Nucleic Acids Res. 2002 Jan 1;30(1):325-327. \
    \
    PlantCARE, a plant cis-acting regulatory element database\
    Stephane Rombauts, Patrice Dhais, Marc Van Montagu and Pierre Rouz\
    Nucleic Acids Res. 1999 Jan 1;27(1):295-6. PMID: 9847207; UI: 99063718.")
    con.write("Gibbs Sampling method to detect over-represented motifs in upstream regions of co-expressed genes. Thijs,G., Marchal,K., Lescot,M., Rombauts,S., De Moor,B., Rouze,P., Moreau,Y. (2002) Journal of Computational Biology, In Press")
    con.write("A Gibbs Sampling Method to Detect Over-represented Motifs in the Upstream Regions of Co-expressed Genes. Thijs,G., Marchal,K., Lescot,M., Rombauts,S., De Moor,B., Rouze,P., Moreau,Y. (2001) Proceedings Recomb'2001, pages 296-302.")
    con.write("A higher order background model improves the detection of regulatory elements by Gibbs Sampling Thijs G., Lescot M., Marchal K., Rombauts S., De Moor B., Rouz P., Moreau Y. (2001) Bioinformatics, in press.")
    con.write("Detection of cis-acting regulatory elements in plants: a Gibbs sampling approach. Thijs,G., Rombauts,S., Lescot,M., Marchal,K., De Moor,B., Moreau,Y. and Rouz,P. Proceedings of the second International conference on bioinformatics of genome regulation and structure (2000), ICG, Novosibirsk, Russia V. 1, pp. 118-126")
    con.write("Recognition of gene regulatory sequences by bagging of neural networks.Thijs, G., Moreau, Y., Rombauts, S., De Moor, B., and Rouz, P. (1999). Proceedings of the Ninth International Conference on Artificial Neural Networks (ICANN '99), European Neural Network Society (Ed.). London, Institution of Electrical Engineers (IEE), pp. 988-993 [ISBN 0-85296-721-7].\n")
    con.write("Adaptive Quality-based clustering of gene expression profiles.Frank De Smet, Kathleen Marchal, Janick Mathijs, Gert Thijs, Bart De Moor and Yves Moreau Bioinformatics, in press.")

    # Footer
    #base_footer()
    return

def glossary_page():
    st.title("Glossary")
    st.write("**Key Terms and Definitions**")
    glossary_entries = {
        'GS - Germinating Seedling': '- The early stage of seedling development where the seed begins to sprout and grow.',
        'S - Shoot': '- The above-ground part of the plant, including stems, leaves, and flowers.',
        'ML - Mature Leaf': '- A fully developed leaf, which has completed its growth.',
        'YL - Young Leaf': '- A developing leaf that has not yet reached full maturity.',
        'Brac - Bracteole': '- A small leaf-like structure at the base of a flower or inflorescence.',
        'R - Root': '- The part of the plant that anchors it in the soil and absorbs water and nutrients.',
        'Rtip - Root Tip': '- The growing tip of the root, where new cells are produced.',
        'RH - Root Hair': '- Tiny hair-like structures on the root that increase surface area for water absorption.',
        'Nod - Nodule': '- A swollen structure on plant roots, often containing nitrogen-fixing bacteria.',
        'SAM - Shoot Apical Meristem': '- The tissue at the tip of the shoot where growth and development occur.',
        'FB1-FB4 - Stages of Flower Bud Development': '- Sequential stages representing the development of flower buds.',
        'FL1-FL5 - Stages of Flower Development': '- Sequential stages representing the development of flowers.',
        'Cal - Calyx': '- The outermost whorl of a flower, usually consisting of sepals.',
        'Cor - Corolla': '- The petals of a flower, collectively forming the corolla.',
        'And - Androecium': '- The male reproductive part of the flower, consisting of stamens.',
        'Gyn - Gynoecium': '- The female reproductive part of the flower, consisting of pistils.',
        'Pedi - Pedicel': '- The stalk that supports a flower or an inflorescence.',
        'Emb - Embryo': '- The early stage of development of a plant from the fertilized egg cell.',
        'Endo - Endosperm': '- The tissue that provides nourishment to the developing embryo in seeds.',
        'SdCt - Seed Coat': '- The outer protective layer of a seed.',
        'PodSh - Podshell': '- The outer casing that surrounds the seeds within a pod.',
        '5DAP - Seed 5 Days After Pollination': '- The developmental stage of seed five days after pollination.',
        '10DAP - Seed 10 Days After Pollination': '- The developmental stage of seed ten days after pollination.',
        '20DAP - Seed 20 Days After Pollination': '- The developmental stage of seed twenty days after pollination.',
        '30DAP - Seed 30 Days After Pollination': '- The developmental stage of seed thirty days after pollination.',
        'GO - Gene Ontology': '- a framework for the model of biology that describes gene functions in a species-independent manner.',
        'KEGG - Kyoto Encyclopedia of Genes and Genomes': '- a database resource for understanding high-level functions and utilities of biological systems.',
        'FPKM - Fragments Per Kilobase of transcript per Million mapped reads': '- a normalized method for counting RNA-seq reads.',
        'miRNA - MicroRNA': '- small non-coding RNA molecules that regulate gene expression by binding to complementary sequences on target mRNA.',
        'lncRNA - Long Non-Coding RNA': '- a type of RNA molecule that is greater than 200 nucleotides in length but does not encode proteins.',
        'ST - Seed Tissue': '- the tissue in seeds that supports the development of the embryo and storage of nutrients.',
        'FDS - Flower Development Stages': '- the various phases of growth and development that a flower undergoes from bud to bloom.',
        'FP - Flower Parts': '- the various components that make up a flower, including petals, sepals, stamens, and carpels.',
        'GT - Green Tissues': ' - plant tissues that are photosynthetic, primarily found in leaves and stems.',
        'RT - Root Tissues': '- the tissues found in the root system of a plant, involved in nutrient absorption and anchorage.',
        'TF - Transcription Factor': '- a protein that controls the rate of transcription of genetic information from DNA to messenger RNA.',
        'Non-TF - Non-Transcription Factors': '- proteins or molecules that do not directly bind to DNA to initiate or regulate transcription, but still influence gene expression through other mechanisms.',
        'WGCNA - Weighted Gene Co-expression Network Analysis': '- a method for finding clusters (modules) of highly correlated genes and studying their relationships to clinical traits.',
        'PPI - Protein-Protein Interaction': '- physical contacts between two or more proteins that occur in a living organism and are essential for various biological functions, including signal transduction and gene regulation.',
        'SNP CALLING - Single Nucleotide Polymorphism': 'The process of identifying single nucleotide polymorphisms (SNPs) in a genome from sequencing data. SNPs are variations at a single position in the DNA sequence, and SNP calling is crucial for genetic studies and disease association analyses.',
        'PEPTIDE SEQUENCE': 'A sequence of amino acids that make up a peptide, which is a short chain of amino acids linked by peptide bonds.',
        'CDS SEQUENCE - Coding Sequence': '- the portion of a gene\'s DNA or RNA that codes for a protein.',
        'TRANSCRIPT SEQUENCE': 'The RNA sequence transcribed from a gene, which may be translated into a protein or may function as non-coding RNA.',
        'GENOMIC SEQUENCE': 'The complete sequence of nucleotides (DNA or RNA) that make up the entire genome of an organism.'
    }

    con=st.container(border=True)
    search_term = con.text_input("Search Glossary", "")
    
    filtered_entries = {term: definition for term, definition in glossary_entries.items() if search_term.lower() in term.lower() or search_term.lower() in definition.lower()}
    con=st.container(border=True)
    with con:
        for term, definition in filtered_entries.items():
            with st.expander(term):
                st.write(definition)
    #base_footer()
    return


#@st.cache_data(show_spinner=False)
def get_image_url(image_path):
    return generate_signed_url(image_path)

def meta_data_page():
    st.title("Statistical Insights")
    st.write("**Key Insights and Analytics from the Application Backend**")

    # Call charts (no caching needed for these)
    svm_charts()
    tsi_plot()

    # Use cached image URLs
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(get_image_url("Images/1.png"), caption="Expression Data Heatmap", use_container_width=True)
        st.write("")
        st.image(get_image_url("Images/2.png"), caption="SVM Kernel Performance", use_container_width=True)
        st.write("")
        st.image(get_image_url("Images/7.png"), caption="Tissue Specific Distribution Plots", use_container_width=True)
        st.write("")

    with col2:
        st.image(get_image_url("Images/4.png"), caption="Functional Annotation [Root Tissues]", use_container_width=True)
        st.write("")

    col3, col4 = st.columns(2)
    with col3:
        st.image(get_image_url("Images/11.png"), caption="Functional Annotation [Seed Tissues]", use_container_width=True)
        st.write("")

    with col4:
        st.image(get_image_url("Images/5.png"), caption="WGCNA Heatmaps", use_container_width=True)
        st.write("")

    st.image(get_image_url("Images/3.png"), caption="Performance Charts for All Files", use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        st.image(get_image_url("Images/8.png"), caption="Functional Annotation [Flower Development Stages]", use_container_width=True)
        st.write("")
        st.image(get_image_url("Images/9.png"), caption="Functional Annotation [Flower Parts]", use_container_width=True)
        st.write("")

    with col6:
        st.image(get_image_url("Images/10.png"), caption="Functional Annotation [Green Tissues]", use_container_width=True)
        st.write("")
        st.image(get_image_url("Images/6.png"), caption="Comparison of lncRNAs, TF, and Non-TF", use_container_width=True)
        st.write("")

    # Footer
    #base_footer()
    return


# ✅ Cache the video URL generation to avoid repeated calls
@st.cache_data(show_spinner=False)
def get_video_url(video_path):
    return generate_signed_url(video_path)

def tutorials_page():
    st.title("Tutorials Page")
    st.write("**Learn how to use this interface**")
    st.write("This page helps you understand how to use the app through video tutorials. Follow the steps below:")

    # ✅ Cache the video URLs for tutorials
    navigation_video_url = get_video_url("Videos/navigation.mp4")
    if navigation_video_url:
        st.video(navigation_video_url, start_time=0)
    else:
        st.warning("Video not found or unable to generate URL.")

    st.subheader("Registration and Login")
    register_video_url = get_video_url("Videos/register.mp4")
    if register_video_url:
        st.video(register_video_url, start_time=0)
    else:
        st.warning("Video not found or unable to generate URL.")
    st.markdown("""
    1. Navigate to the Login page.
    2. Register for new users.
    3. Login using your credentials.
    4. Unlock Search functionality and additional features.""")

    st.subheader("Single Task Tutorial")
    start_task1_video_url = get_video_url("Videos/start_task1.mp4")
    if start_task1_video_url:
        st.video(start_task1_video_url, start_time=0)
    else:
        st.warning("Video not found or unable to generate URL.")
    st.markdown("""
    1. Navigate to the **Start Task** page.
    2. Enter the 8-character code when prompted.
    3. Click the **Start** button to begin the task.
    4. Wait for the task to complete and view the results.""")

    st.subheader("Multi Task Tutorial")
    start_task2_video_url = get_video_url("Videos/start_task2.mp4")
    if start_task2_video_url:
        st.video(start_task2_video_url, start_time=0)
    else:
        st.warning("Video not found or unable to generate URL.")
    st.markdown("""
    1. Navigate to the **Start Task** page.
    2. Enter the 8-character code when prompted.
    3. Click the **Start** button to begin the task.
    4. Wait for the task to complete and view the results.""")

    st.subheader("Glossary Tutorial")
    glossary_video_url = get_video_url("Videos/glossary.mp4")
    if glossary_video_url:
        st.video(glossary_video_url, start_time=0)
    else:
        st.warning("Video not found or unable to generate URL.")

    # Call base_footer function
    #base_footer()
    return


#@st.cache_data(show_spinner=False)
def get_image_url(image_path):
    return generate_signed_url(image_path)

def display_about_content():
    st.title("About Us")
    col1, col2 = st.columns(2)
    
    # Container 1
    st.markdown("""<style>.stVerticalBlock.st-key-au2, .stVerticalBlock.st-key-au1, .stVerticalBlock.st-key-au3, .stVerticalBlock.st-key-au4, .stVerticalBlock.st-key-au5, .stVerticalBlock.st-key-au6 {background-color: rgb(185, 214, 148); color: white; padding: 20px; border-radius: 10px; transition: all 0.3s ease-in-out;} .stVerticalBlock.st-key-au2:hover, .stVerticalBlock.st-key-au1:hover, .stVerticalBlock.st-key-au3:hover, .stVerticalBlock.st-key-au4:hover, .stVerticalBlock.st-key-au5:hover, .stVerticalBlock.st-key-au6:hover {background-color: rgba(242,240,239,0.5); color: black; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); transform: translateY(-2px);}</style>""", unsafe_allow_html=True)
    con = col1.container(border=False, key="au1")
    with con:
        c1, c2 = st.columns([7,13])
        c1.image(get_image_url("About/img.jpg"), use_container_width=True)
        c2.subheader("Dr. Sarvajeet Singh Gill")
        c2.write("Centre for Biotechnology\
                 \nMaharshi Dayanand University, Rohtak, HR, India\
                 \nㅤ")
        d0,d1,d2,d3,d4=c2.columns([1,5,1,5,1])
        d1.link_button("Profile",url="wwww.google.com",use_container_width=True)
        d3.link_button("Email",url="mailto:abc@gmail.com",use_container_width=True)
    
    # Container 2
    con = col2.container(border=False, key="au2")
    with con:
        c1, c2 = st.columns([7,13])
        c1.image(get_image_url("About/img.jpg"), use_container_width=True)
        c2.subheader("Dr. Kamaldeep Joshi")
        c2.write("Department of Computer Science and Technology\
                 \nUniversity Institute of Engineering and Technology,\
                 \nMaharshi Dayanand University, Rohtak, HR, India")
        d0,d1,d2,d3,d4=c2.columns([1,5,1,5,1])
        d1.link_button("Profile",url="wwww.google.com",use_container_width=True)
        d3.link_button("Email",url="mailto:abc@gmail.com",use_container_width=True)

    # Container 3
    con = col1.container(border=False, key="au3")
    with con:
        c1, c2 = st.columns([7,13])
        c1.image(get_image_url("About/img.jpg"), use_container_width=True)
        c2.subheader("Dr. Ritu Gill")
        c2.write("Centre for Biotechnology\
                 \nMaharshi Dayanand University, Rohtak, HR, India\
                 \nㅤ")
        d0,d1,d2,d3,d4=c2.columns([1,5,1,5,1])
        d1.link_button("Profile",url="wwww.google.com",use_container_width=True)
        d3.link_button("Email",url="mailto:abc@gmail.com",use_container_width=True)
    
    # Container 4
    con = col2.container(border=False, key="au4")
    with con:
        c1, c2 = st.columns([7,13])
        c1.image(get_image_url("About/img.jpg"), use_container_width=True)
        c2.subheader("Dr. Gopal Kalwan")
        c2.write("Centre for Biotechnology\
                 \nMaharshi Dayanand University, Rohtak, HR, India\
                 \nㅤ")
        d0,d1,d2,d3,d4=c2.columns([1,5,1,5,1])
        d1.link_button("Profile",url="wwww.google.com",use_container_width=True)
        d3.link_button("Email",url="mailto:abc@gmail.com",use_container_width=True)

    # Container 5
    con = col1.container(border=False, key="au5")
    with con:
        c1, c2 = st.columns([7,13])
        c1.image(get_image_url("About/img.jpg"), use_container_width=True)
        c2.subheader("Ms. Ashima Nehra")
        c2.write("Centre for Biotechnology\
                 \nMaharshi Dayanand University, Rohtak, HR, India\
                 \nㅤ")
        d0,d1,d2,d3,d4=c2.columns([1,5,1,5,1])
        d1.link_button("Profile",url="wwww.google.com",use_container_width=True)
        d3.link_button("Email",url="mailto:abc@gmail.com",use_container_width=True)
    
    # Container 6
    con = col2.container(border=False, key="au6")
    with con:
        c1, c2 = st.columns([7,13])
        c1.image(get_image_url("About/img.jpg"), use_container_width=True)
        c2.subheader("Aakash Kharb")
        c2.write("Department of Computer Science and Technology\
                 \nUniversity Institute of Engineering and Technology,\
                 \nMaharshi Dayanand University, Rohtak, HR, India")
        d0,d1,d2,d3,d4=c2.columns([1,5,1,5,1])
        d1.link_button("Profile",url="wwww.google.com",use_container_width=True)
        d3.link_button("Email",url="mailto:abc@gmail.com",use_container_width=True)
    return

def about_page():
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = 'ABOUT-US'
    
    def set_active_tab(tab_name):
        st.session_state.active_tab = tab_name
    
    # Create columns for buttons
    st.write(" ")
    col1, col2, col3, col4, col5 = st.columns(5)
    if col1.button("ABOUT-US", key="btn_about",use_container_width=True):
        set_active_tab('ABOUT-US')
        st.rerun()
    if col2.button("STATISTICS", key="btn_meta",use_container_width=True):
        set_active_tab('STATISTICS')
        st.rerun()
    if col3.button("CITATIONS", key="btn_citations",use_container_width=True):
        set_active_tab('CITATIONS')
        st.rerun()
    if col4.button("GLOSSARY", key="btn_glossary",use_container_width=True):
        set_active_tab('GLOSSARY')
        st.rerun()
    if col5.button("TUTORIALS", key="btn_tutorials",use_container_width=True):
        set_active_tab('TUTORIALS')
        st.rerun()
        
    # Display content based on active tab
    if st.session_state.active_tab == 'ABOUT-US':
        display_about_content()
    elif st.session_state.active_tab == 'STATISTICS':
        meta_data_page()
    elif st.session_state.active_tab == 'CITATIONS':
        citations_page()
    elif st.session_state.active_tab == 'GLOSSARY':
        glossary_page()
    elif st.session_state.active_tab == 'TUTORIALS':
        tutorials_page()
    
    base_footer()
    return

@st.cache_data
def gallery_html():
    file_url=generate_signed_url('Gallery/1.png')
    response=requests.get(file_url)
    img_base64 = img_to_base64(response.content)
    gallery_image = f"data:image/png;base64,{img_base64}"
    gallery_html=f"""<style>
        /* Importing the Nunito font from Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@200;300;400;600;700&display=swap');
        
        /* Defining a CSS variable for the color orange */
        :root {{
          --orange: #bfd59b;/*#ffa500;*/
        }}
        
        /* Universal reset for all elements */
        * {{
          font-family: 'Nunito', sans-serif; /* Setting the default font to Nunito */
          margin: 0; /* Removing default margin */
          padding: 0; /* Removing default padding */
          box-sizing: border-box; /* Ensuring padding and border are included in element dimensions */
          outline: none; /* Removing default outline */
          border: none; /* Removing default border */
          text-decoration: none; /* Removing default text decoration (e.g., underline on links) */
          transition: all 0.2s linear; /* Adding a smooth transition effect for all properties */
        }}
        
        /* Styling for text selection */
        *::selection {{
          background: var(--orange); /* Setting the background color of selected text to orange */
          color: #fff; /* Setting the text color of selected text to white */
        }}
        
        /* Base styles for the HTML element */
        html {{
          font-size: 62.5%; /* Setting base font size to 10px (62.5% of 16px) */
          overflow-x: hidden; /* Hiding horizontal scrollbar */
          scroll-padding-top: 6rem; /* Adding padding to the top of scrollable areas */
          scroll-behavior: smooth; /* Enabling smooth scrolling */
        }}
        
        /* Styling for all sections */
        section {{
          padding: 4rem 9%; /* Adding padding to all sections */
        }}
        
        /* Styling for buttons */
        .btn {{
          display: inline-block; /* Making buttons inline-block elements */
          margin-top: 1rem; /* Adding margin to the top of buttons */
          background: var(--orange); /* Setting background color to orange */
          color: #fff; /* Setting text color to white */
          padding: 0.8rem 3rem; /* Adding padding */
          border: 0.2rem solid var(--orange); /* Adding a border */
          cursor: pointer; /* Changing cursor to pointer on hover */
          font-size: 1.7rem; /* Setting font size */
        }}
        
        /* Styling for button hover state */
        .btn:hover {{
          background: rgba(238,127,87,1); /* Changing background color on hover of gallery buttons */
          color: var(--orange); /* Changing text color on hover */
        }}
        
        /* Styling for the gallery section */
        .gallery .box-container {{
          display: flex; /* Using flexbox for layout */
          flex-wrap: wrap; /* Allowing items to wrap to the next line */
          gap: 1.5rem; /* Adding space between items */
        }}
        
        /* Styling for individual boxes in the gallery section */
        .gallery .box-container .box{{
          overflow: hidden; /* Hiding overflow content */
          box-shadow: 0 1rem 2rem rgba(0, 0, 0, 0.1); /* Adding a shadow */
          border: 1rem solid #fff; /* Adding a white border */
          border-radius: 0.5rem; /* Adding rounded corners */
          flex: 1 1 30rem; /* Allowing boxes to grow and shrink, with a base width of 30rem */
          height: 25rem; /* Setting a fixed height */
          position: relative; /* Setting position to relative for child elements */
        }}
        
        /* Styling for images inside gallery boxes */
        .gallery .box-container .box img {{
          height: 100%; /* Setting image height to 100% of the box */
          width: 100%; /* Setting image width to 100% of the box */
          object-fit: cover; /* Ensuring the image covers the box without distortion */
        }}
        
        /* Styling for content inside gallery boxes */
        .gallery .box-container .box .content {{
          position: absolute; /* Positioning content absolutely within the box */
          top: -100%; /* Initially hiding content above the box */
          left: 0; /* Aligning content to the left */
          height: 100%; /* Setting height to 100% of the box */
          width: 100%; /* Setting width to 100% of the box */
          text-align: center; /* Centering text */
          background: rgba(0, 0, 0, 0.7); /* Adding a semi-transparent black background */
          padding: 2rem; /* Adding padding */
          padding-top: 5rem; /* Adding extra padding to the top */
        }}
        
        /* Styling for gallery box hover state */
        .gallery .box-container .box:hover .content{{
          top: 0; /* Moving content down to reveal it on hover */
        }}
        
        /* Styling for headings inside gallery content */
        .gallery .box-container .box .content h3 {{
          font-size: 2.5rem; /* Setting font size */
          color: var(--orange); /* Setting text color to orange */
        }}
        
        /* Styling for paragraphs inside gallery content */
        .gallery .box-container .box .content p {{
          font-size: 1.5rem; /* Setting font size */
          color: #eee; /* Setting text color */
          padding: 0.5rem 0; /* Adding padding */
        }}
        </style>
        
        <html lang="en">
        <head>
        
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
            
        </head>
        <body>
        <!-- gallery section starts  -->
        
        <section class="gallery" id="gallery">    
            <div class="box-container">
        
                <div class="box">
                    <img src={gallery_image} alt="">
                    <div class="content">
                        <h3>Person 1</h3>
                        <h3>@gmail.com</h3>
                        <a href="mailto:akharbrtk2@gmail.com?subject=Chickpea%20Omics%20Explorer%20App%20Inquiry&body=I%20am%20writing%20to%20inquire%20about..." class="btn">E-mail</a>
                    </div>
                </div>
                <div class="box">
                    <img src={gallery_image} alt="">
                    <div class="content">
                        <h3>Person 2</h3>
                        <h3>@gmail.com</h3>
                        <a href="mailto:akharbrtk2@gmail.com?subject=Chickpea%20Omics%20Explorer%20App%20Inquiry&body=I%20am%20writing%20to%20inquire%20about..." class="btn">E-mail</a>
                    </div>
                </div>
                <div class="box">
                    <img src={gallery_image} alt="">
                    <div class="content">
                        <h3>Person 3</h3>
                        <h3>@gmail.com</h3>
                        <a href="mailto:akharbrtk2@gmail.com?subject=Chickpea%20Omics%20Explorer%20App%20Inquiry&body=I%20am%20writing%20to%20inquire%20about..." class="btn">E-mail</a>
                    </div>
                </div>
                <div class="box">
                    <img src={gallery_image} alt="">
                    <div class="content">
                        <h3>Person 4</h3>
                        <h3>@gmail.com</h3>
                        <a href="mailto:akharbrtk2@gmail.com?subject=Chickpea%20Omics%20Explorer%20App%20Inquiry&body=I%20am%20writing%20to%20inquire%20about..." class="btn">E-mail</a>
                    </div>
                </div>
                <div class="box">
                    <img src={gallery_image} alt="">
                    <div class="content">
                        <h3>Person 5</h3>
                        <h3>@gmail.com</h3>
                        <a href="mailto:akharbrtk2@gmail.com?subject=Chickpea%20Omics%20Explorer%20App%20Inquiry&body=I%20am%20writing%20to%20inquire%20about..." class="btn">E-mail</a>
                    </div>
                </div>
                <div class="box">
                    <img src={gallery_image} alt="">
                    <div class="content">
                        <h3>Person 6</h3>
                        <h3>@gmail.com</h3>
                        <a href="mailto:akharbrtk2@gmail.com?subject=Chickpea%20Omics%20Explorer%20App%20Inquiry&body=I%20am%20writing%20to%20inquire%20about..." class="btn">E-mail</a>
                    </div>
                </div>
            </div>
        </section>
        
        <!-- gallery section ends -->
        
        </body>
        </html>
    """

    html(gallery_html,height=600,scrolling=True)
    return

def initialize_database():
    try:
        mysql_config = st.secrets["mysql"]
        host = mysql_config["host"]
        user = mysql_config["user"]
        password = mysql_config["password"]
        port = mysql_config["port"]
        db = "Chickpea"

        mydb = pymysql.connect(host=host,user=user,password=password,port=port,ssl={"ssl_disabled": True})
        mycursor = mydb.cursor()

        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        mydb.commit()
        mycursor.execute(f"USE {db}")

        query1 = """
        CREATE TABLE IF NOT EXISTS Authentication (
            SNo INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(20) NOT NULL UNIQUE,
            Password VARCHAR(255) NOT NULL
        )
        """
        mycursor.execute(query1)
        mydb.commit()

        query2 = """
        CREATE TABLE IF NOT EXISTS Identity (
            Username VARCHAR(20) PRIMARY KEY,
            FirstName VARCHAR(30) NOT NULL,
            LastName VARCHAR(30),
            Email VARCHAR(255) NOT NULL UNIQUE,
            FOREIGN KEY (Username) REFERENCES Authentication(Username)
        )
        """
        mycursor.execute(query2)
        mydb.commit()

        query3 = """
        CREATE TABLE IF NOT EXISTS History (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Username VARCHAR(20) NOT NULL,
            tid VARCHAR(20),
            mtid VARCHAR(255),
            locid VARCHAR(20),
            mlocid VARCHAR(255),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Username) REFERENCES Authentication(Username)
        )
        """
        mycursor.execute(query3)
        mydb.commit()

        query4 = """
        CREATE TABLE IF NOT EXISTS Visitor (
            Visitor_number INT AUTO_INCREMENT PRIMARY KEY,
            Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        mycursor.execute(query4)
        mydb.commit()
        st.success(f"Database '{db}' and tables created successfully.")
        return mydb, mycursor

    except pymysql.Error as e:
        st.error(f"Error: {e}")
        return None, None

# Function to check if a user exists in the Authentication table
def check_user(username, password):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Authentication WHERE Username = %s AND Password = %s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to add a new user to the Authentication and Identity tables
def add_user(username, password, first_name, last_name, email):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Authentication (Username, Password) VALUES (%s, %s)", (username, password))
        cursor.execute("INSERT INTO Identity (Username, FirstName, LastName, Email) VALUES (%s, %s, %s, %s)", (username, first_name, last_name, email))
        conn.commit()
        conn.close()
        return True
    except pymysql.Error as e:
        st.error(f"Error: {e}")
        conn.close()
        return False

# Function to validate email
def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def validate_username_length(username):
    return 1 <= len(username) <= 20

# Function to validate username
def validate_username(username):
    pattern = r"^[a-zA-Z0-9!@#$%^&*_+\-\/?]{1,20}$"
    return re.match(pattern, username) is not None

# Function to validate password length
def validate_password(password):
    return len(password) >= 8

def validate_password_max(password):
    return len(password) <= 20

# Function to connect to the database
def connect_to_db():
    mysql_config = st.secrets["mysql"]
    return pymysql.connect(host=mysql_config["host"],user=mysql_config["user"],password=mysql_config["password"],port=mysql_config["port"],database="Chickpea",ssl={"ssl_disabled": True})

def basic_stats():
    conn3 = connect_to_db()
    cursor3 = conn3.cursor()
    cursor3.execute("SELECT COUNT(*) FROM Authentication")
    total_members = cursor3.fetchone()[0]
    #st.sidebar.subheader(f"Total Members : {total_members}")    #change

    cursor3.execute("SELECT COUNT(*) FROM History")
    total_searches = cursor3.fetchone()[0]
    #st.sidebar.subheader(f"Total Searches : {total_searches}")  #change

    conn3.commit()
    conn3.close()
    return total_members, total_searches

def update_visitor_count():
    conn4 = connect_to_db()
    cursor4 = conn4.cursor()
    if st.session_state.get("first_access",False):
        if st.session_state.current_page !="HOME":
            query = "INSERT INTO Visitor (Timestamp) VALUES (NOW())"
            cursor4.execute(query)
            conn4.commit()
            st.session_state.first_access = False

    query = "SELECT COUNT(*) FROM Visitor"
    cursor4.execute(query)
    result = cursor4.fetchone()
    conn4.close()
    return result[0]

# Streamlit app
def security_login():
    st.title("Login and Registration")

    # Initialize database and tables
    if "db_initialized" not in st.session_state:
        st.session_state.mydb, st.session_state.mycursor = initialize_database()
        if st.session_state.mydb and st.session_state.mycursor:
            st.session_state.db_initialized = True

    # Initialize session state for authentication
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        choice = st.radio("Choose an option", ["Login", "Register"])

        if choice == "Login":
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if check_user(username, password):
                    st.session_state['authenticated'] = True
                    st.success("Logged in successfully!")
                    st.title(f"Welcome user")
                    conn = connect_to_db()
                    cursor = conn.cursor()
                    #main part to confirm
                    query5 = "SELECT FirstName FROM Identity WHERE Username = %s"
                    cursor.execute(query5, (username,))
                    user_info = cursor.fetchone()
                    if user_info:
                        st.title(f"Hello {user_info[0]}!")
                    else:
                        st.title("User information not found.")
                    query6 = "SELECT LastName FROM Identity WHERE Username = %s"
                    cursor.execute(query6, (username,))
                    user_info = cursor.fetchone()
                    if user_info:
                        st.title(f"Hello {user_info[0]}!")
                    else:
                        st.title("User information not found.")
                    query7 = "SELECT Email FROM Identity WHERE Username = %s"
                    cursor.execute(query7, (username,))
                    user_info = cursor.fetchone()
                    if user_info:
                        st.title(f"Hello {user_info[0]}!")
                    else:
                        st.title("User information not found.")
                else:
                    st.error("Invalid username or password")

        elif choice == "Register":
            st.subheader("Register")
            username = st.text_input("Username (max 20 chars, allowed: a-z, A-Z, 0-9, !@#$%^&*_+-/?)")
            password = st.text_input("Password (min 8 chars)", type="password")
            first_name = st.text_input("First Name (max 30 chars)")
            last_name = st.text_input("Last Name (max 30 chars, optional)", "")
            email = st.text_input("Email")

            if st.button("Register"):
                if not validate_username_length(username):
                    st.error("Username must be between 1 and 20 characters long.")
                elif not validate_password_max(password):
                    st.error("Password must be less than 20 characters long.")
                elif not validate_username(username):
                    st.error("Invalid username. Only a-z, A-Z, 0-9, and !@#$%^&*_+-/? are allowed.")
                elif not validate_email(email):
                    st.error("Invalid email. Must contain @ and .com.")
                elif not validate_password(password):
                    st.error("Password must be at least 8 characters long.")
                else:
                    if add_user(username, password, first_name, last_name, email):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Username or email already exists.")

    else:
        st.subheader("Search Page")
        st.write("Welcome to the Search Page!")
    return

def login_interface():
    #with st.container(border=True):
    with st.expander("⠀", expanded=st.session_state.get('expander_state', True)):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.title("Login")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Enter Username")
        with col3:
            username = st.text_input("Username", key="login_username", label_visibility="collapsed")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Enter Password")
        with col3:
            password = st.text_input("Password", key="login_password", type="password", label_visibility="collapsed")
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 2, 1, 1, 1])
        with col4:
            if st.button("Continue", use_container_width=True):
                st.success("Checking credentials")
                if check_user(username, password):
                    st.success("Logged in successfully!")
                    st.write("By clicking Confirm you agree to the Code of Conduct. utilize the true potential of this amazing Explorer")
                    st.session_state["logged_in"] = True
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    #st.session_state['expander_state'] = False
                    if st.session_state.get("redirect_to_login", False):
                        st.session_state["redirect_to_login"] = False
                        #st.switch_page("pages/Search.py")
                        #time.sleep(2)
                        #st.rerun()
                else:
                    st.error("Invalid username or password")

def register_interface():
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.title("Register")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("First Name")
            fname = st.text_input("FirstName", label_visibility="collapsed")
        with col3:
            st.subheader("Last Name")
            lname = st.text_input("LastName", label_visibility="collapsed")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Create Username")
        with col3:
            username1 = st.text_input("Username", label_visibility="collapsed")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Enter Email")
        with col3:
            email1 = st.text_input("Email", label_visibility="collapsed")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Create Password")
        with col3:
            password1 = st.text_input("Password1", type="password", label_visibility="collapsed")
        
        col1, col2, col3, col4 = st.columns(4)
        with col2:
            st.subheader("Confirm Password")
        with col3:
            password2 = st.text_input("Password2", type="password", label_visibility="collapsed")
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 2, 1, 1, 1])
        with col4:
            if st.button("Register", use_container_width=True):
                if password1 == password2:
                    st.success("Password checked")
                    if not validate_username_length(username1):
                        st.error("Username must be between 1 and 20 characters long.")
                    elif not validate_password_max(password1):
                        st.error("Password must be less than 20 characters long.")
                    elif not validate_username(username1):
                        st.error("Invalid username. Only a-z, A-Z, 0-9, and !@#$%^&*_+-/? are allowed.")
                    elif not validate_email(email1):
                        st.error("Invalid email. Must contain @ .com .ac .in ")
                    elif not validate_password(password1):
                        st.error("Password must be at least 8 characters long.")
                    else:
                        if add_user(username1, password1, fname, lname, email1):
                            st.success("Registration successful! Please login.")
                            st.session_state.current_interface='login'
                            st.rerun()
                        else:
                            st.error("Username or email already exists.")
                else:
                    st.warning("Passwords do not match. Please try again.")

def login_page():
    if 'current_interface' not in st.session_state:
        st.session_state.current_interface = None
    st.title("Security")

    if st.session_state.get("logged_in", False) and st.session_state.get("authenticated", False):
        username = st.session_state.get('username')
        details_button = st.expander("⠀", expanded=True)
        col1, col2, col4, col6, col7 = st.columns([1, 2, 1, 2, 1])
        history_button = col2.button("History", key="history_login")
        logout_button = col6.button("Logout", key="logout_login")
        conn2 = connect_to_db()
        cursor2 = conn2.cursor()
        query = "SELECT Username,FirstName, LastName, Email FROM Identity WHERE Username = %s"
        cursor2.execute(query, (username,))
        result = cursor2.fetchone()
        with details_button:
                col1,col2=st.columns(2)
                with col1:
                    st.subheader(f"**Name**: {result[1]} {result[2]}")
                    st.subheader(f"**Username**: {result[0]}")
                with col2:
                    st.subheader(f"**Email**: {result[3]}")
        cursor2.execute("SELECT COUNT(*) FROM History WHERE Username = %s", (username,))
        user_searches = cursor2.fetchone()[0]
        st.subheader(f"**Total Searches** for **{username}**: **{user_searches}**")
        conn2.commit()
        conn2.close()

        if history_button:
            conn2 = connect_to_db()
            cursor2 = conn2.cursor()
            con = st.container(border=True)
            con.write(f"**History** for **{username}** :-")
            cursor2.execute("SELECT * FROM History WHERE Username = %s", (username,))
            rows = cursor2.fetchall()
            column_names = [desc[0] for desc in cursor2.description]
            df = pd.DataFrame(rows, columns=column_names)
            con.dataframe(df, use_container_width=True)
            conn2.close()

        # Handle logout
        if logout_button:
            st.session_state["logged_in"] = False
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.success("You have been logged out successfully!")
            time.sleep(2)
            st.rerun()

    else:
        # User is not logged in, show login and register options
        col1, col2, col4, col6, col7 = st.columns([1, 2, 1, 2, 1])
        login_button = col2.button("Login")
        register_button = col6.button("Register")

        if login_button:
            st.session_state.current_interface = 'login'

        if register_button:
            st.session_state.current_interface = 'register'

        # Show the appropriate interface based on the current state
        if st.session_state.current_interface == 'login':
            login_interface()
            if st.session_state.get("authenticated", False):
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 2, 1, 1, 1])
                col4.button("Confirm")
        elif st.session_state.current_interface == 'register':
            register_interface()
    return

def home_page():
    st.markdown("""<style>.stVerticalBlock.st-key-con2hp, .stVerticalBlock.st-key-con31hp, .stVerticalBlock.st-key-con32hp, .stVerticalBlock.st-key-con11hp, .stVerticalBlock.st-key-con12hp {background-color: rgba(255,119,75,1); padding: 20px; border-radius: 10px; transition: all 0.3s ease-in-out;} .stVerticalBlock.st-key-con2hp:hover, .stVerticalBlock.st-key-con31hp:hover, .stVerticalBlock.st-key-con32hp:hover, .stVerticalBlock.st-key-con11hp:hover, .stVerticalBlock.st-key-con12hp:hover {background-color: rgba(255,119,75,0.5); box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); transform: translateY(-2px);} .stVerticalBlock.st-key-rest1container, .stVerticalBlock.st-key-rest3container {background-color: #f4f4f9; padding: 30px; border-radius: 15px;}</style>""", unsafe_allow_html=True)
    #st.markdown("""<style>.block-container {padding-top: 6rem;padding-bottom: 2rem;padding-left: 1rem;padding-right: 1rem;}</style>""", unsafe_allow_html=True)
    col1,col2,col3=st.columns([1,2,1])
    with col1:
        con=st.container(border=True,height=260)
        con=st.container(border=True,height=260)
    col2.markdown(''
        '<style>'
        '    /* General Styles */'
        '    .hp-body {'
        '        font-family: Arial, sans-serif;'
        '        margin: 0;'
        '        padding: 0;'
        '        color: #333;'
        '    }'
        '    .hp-container {'
        '        max-width: 1000px;'
        '        background-color: #f4f4f9;'
        '        margin: 0 auto;'
        '        padding: 20px;'
        '        border-radius: 2rem;'
        '        border: 10px solid #ff774b;'
        '        box-shadow: 0 4px 8px rgba(0,0,0,0.1);'
        '    }'
        '    /* Paragraph Styles */'
        '    .hp-paragraph {'
        '        font-size: 1rem;'
        '        line-height: 1.6;'
        '        margin-bottom: 20px;'
        '        text-align: justify; /* Text is now justified */'
        '    }'
        '    .hp-paragraph b {'
        '        color: #e74c3c;'
        '        font-weight: bold;'
        '    }'
        '    .hp-paragraph em {'
        '        font-style: italic;'
        '        text-decoration: underline;'
        '    }'
        '    .hp-list {'
        '        list-style-type: square;'
        '        margin-left: 20px;'
        '    }'
        '    /* Additional Paragraphs */'
        '    .hp-additional-paragraph {'
        '        font-size: 1rem;'
        '        line-height: 1.6;'
        '        margin-bottom: 30px;'
        '    }'
        '</style>'
        '<div class="hp-body">'
        '  <div class="hp-container">'
        '    <!-- Heading and Subheading -->'
        '    <p style="text-align: center; font-size: 3rem; margin-bottom: 5px; color: #2c3e50; font-weight: bold;">ChickpeaOmicsExplorer</p>'
        '    <p style="text-align: center; font-size: 1.2rem; color: #7f8c8d; margin-bottom: 10px; font-weight: bold;">CHICKPEA (<i>Cicer arietinum L.</i>) DATABASE</p>'
        '    <!-- Paragraph with List and Special Effects -->'
        '    <br><p class="hp-paragraph">'
        '      Chickpea (<i>Cicer arietinum L.</i>), a major legume valued for its high protein content and predominantly cultivated in arid and semi-arid regions. With the advent of high throughput sequencing technologies vast amount of genomic and transcriptomic data have been generated. To effectively utilize this wealth of information, we developed AI-driven platform, the “CHICKPEA OMICS EXPLORER”. This interactive database integrates multiple genomic resources including Phytozome, NCBI, CicerSeq and the chickpea transcriptome database. It offers comprehensive tools for spatial-temporal gene expression profiling, motif discovery, RNA coding potential analysis, protein interaction networks, pathway enrichment analysis, SNP detection, and ortholog identification. By consolidating diverse datasets and analysis, the Chickpea Omics Explorer serves as a powerful resourse for trait dissection, molecular breeding and functional genomics research in chickpea.'
        '    </p>'
        '    <ul class="hp-list">'
        '    </ul>'
        '    <!-- Additional Paragraphs -->'
        '    <p class="hp-additional-paragraph">'
        '    </p>'
        '    <p class="hp-additional-paragraph">'
        '    </p>'
        '    <!-- More Text -->'
        '    <p class="hp-additional-paragraph">'
        '    </p>'
        '  </div>'
        '</div>'
        '', unsafe_allow_html=True)
    with col3:
        con=st.container(border=True,height=260)
        con=st.container(border=True,height=260)
    #sub1
    con=st.container(border=False, key="rest1container")
    with con:
        col1,col2=st.columns(2)
        con=col1.container(border=True,key="con11hp")
        with con:
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
        con=col2.container(border=True,key="con12hp")
        with con:
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")

        con=st.container(border=True)
        with con:
            gallery_html()

    #sub3
    con=st.container(border=False, key="rest3container")
    with con:
        con=st.container(border=True,key="con2hp")
        with con:
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")

        col1,col2=st.columns(2)
        con=col1.container(border=True,key="con31hp")
        with con:
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
        con=col2.container(border=True,key="con32hp")
        with con:
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")
            st.write(".")

    base_footer()
    return

def search_page():
    if st.session_state.get('authenticated', False):
        username = st.session_state.get('username')
    st.title("Search")
    st.write("**Begin the search by interacting with the backend process.**")
    col1, col2 = st.columns(2)

    with col1:
        con1 = st.container(border=True)
        tid = con1.text_input("Enter the Gene ID: ", placeholder="e.g., Ca_00001", key="Tid_input1").strip()
        mtid = con1.text_input("Enter multiple Gene IDs: ", placeholder="e.g., Ca_00001, Ca_00002", key="mTid_input2").strip()
        if mtid:
            mtid_list = [item.strip() for item in mtid.replace(",", " ").split()]
            mtid_list = list(set(mtid_list))
            mtid = ",".join(mtid_list)

    with col2:
        con2 = st.container(border=True)
        locid = con2.text_input("Enter the NCBI ID: ", placeholder="e.g., LOC101511858", key="Locid_input1").strip()
        mlocid = con2.text_input("Enter multiple NCBI IDs: ", placeholder="e.g., LOC101511858, LOC101496413", key="mLocid_input2").strip()
        if mlocid:
            mlocid_list = [item.strip() for item in mlocid.replace(",", " ").split()]
            mlocid_list = list(set(mlocid_list))
            mlocid = ",".join(mlocid_list)

    con1, con2, con3 = st.columns([2, 2, 2])
    with con2:
        start_button = st.button("Search", use_container_width=True, key="Searchbutton1")

    if start_button:
        if not st.session_state.get("logged_in", False):
            if tid or mtid or locid or mlocid:
                st.warning("You need to login to perform this action. Redirecting to login page in 5 seconds...")
                time.sleep(5)
                st.session_state["redirect_to_login"] = True
                st.rerun()
        else:
            conn = connect_to_db()
            cursor = conn.cursor()
            if tid:
                if 1 <= len(tid) <= 20:
                    result = user_input_menu(tid)
                    st.write(result)
                    st.toast("Task completed successfully.")
                    query_tid = """
                    INSERT INTO History (Username, tid)
                    VALUES (%s, %s)
                    """
                    cursor.execute(query_tid, (username, tid))
                else:
                    st.warning("Gene ID must be at most 20 characters.")
            elif mtid:
                result = multi_user_input_menu(mtid)
                st.write(result)
                chunk_size = 255
                st.toast("Task completed successfully.")
                query_mtid = """
                INSERT INTO History (Username, mtid)
                VALUES (%s, %s)
                """
                for i in range(0, len(mtid), chunk_size):
                    chunk = mtid[i:i + chunk_size]
                    cursor.execute(query_mtid, (username, chunk))
                
                #cursor.execute(query_mtid, (username, mtid))
            elif locid:
                if 1 <= len(locid) <= 20:
                    tid = process_locid(locid)
                    result = user_input_menu(tid)
                    st.write(result)
                    st.toast("Task completed successfully.")
                    query_locid = """
                    INSERT INTO History (Username, locid)
                    VALUES (%s, %s)
                    """
                    cursor.execute(query_locid, (username, locid))
                else:
                    st.warning("NCBI ID must be at most 20 characters.")
            elif mlocid:
                mtid = process_mlocid(mlocid)
                result = multi_user_input_menu(mtid)
                st.write(result)
                chunk_size = 255
                st.toast("Task completed successfully.")
                query_mlocid = """
                INSERT INTO History (Username, mlocid)
                VALUES (%s, %s)
                """
                for i in range(0, len(mlocid), chunk_size):
                    chunk = mlocid[i:i + chunk_size]
                    cursor.execute(query_mlocid, (username, chunk))
                #cursor.execute(query_mlocid, (username, mlocid))
            else:
                st.warning("Need either a Gene ID or NCBI ID to proceed.")
            conn.commit()
            conn.close()
    elif tid == "":
        st.warning("Need Gene ID to proceed.")
    else:
        st.write("Press the 'Search' button to begin ...")
        st.write("Follow the instructions or check out tutorials")
    c1,c2,c3,c4=st.columns([2,3,3,2])
    if st.session_state.get('authenticated', False):
        if c2.button("History", key="History_search",use_container_width=True):
            conn2= connect_to_db()
            cursor2= conn2.cursor()
            st.write(f"History for {username} :-")
            cursor2.execute("SELECT * FROM History WHERE Username = %s", (username,))
            rows = cursor2.fetchall()
            column_names = [desc[0] for desc in cursor2.description]
            df = pd.DataFrame(rows, columns=column_names)
            st.dataframe(df)
            conn2.close()
    if st.session_state.get('authenticated', False):
        if c3.button("Logout", key="logout_search",use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.success("You have been logged out successfully!")
            time.sleep(2)
            st.rerun()
    base_footer()
    return

