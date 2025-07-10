import streamlit as st
from pages.footer_all import base_footer 
from pages.gallery import gallery_html

def home_page():
    st.markdown("""<style>.stVerticalBlock.st-key-con2hp, .stVerticalBlock.st-key-con31hp, .stVerticalBlock.st-key-con32hp, .stVerticalBlock.st-key-con11hp, .stVerticalBlock.st-key-con12hp {background-color: rgba(255,119,75,1); padding: 20px; border-radius: 10px; transition: all 0.3s ease-in-out;} .stVerticalBlock.st-key-con2hp:hover, .stVerticalBlock.st-key-con31hp:hover, .stVerticalBlock.st-key-con32hp:hover, .stVerticalBlock.st-key-con11hp:hover, .stVerticalBlock.st-key-con12hp:hover {background-color: rgba(255,119,75,0.5); box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); transform: translateY(-2px);} .stVerticalBlock.st-key-rest1container, .stVerticalBlock.st-key-rest3container {background-color: #f4f4f9; padding: 30px; border-radius: 15px;}</style>""", unsafe_allow_html=True)
    #st.markdown("""<style>.block-container {padding-top: 6rem;padding-bottom: 2rem;padding-left: 1rem;padding-right: 1rem;}</style>""", unsafe_allow_html=True)
    st.markdown(''
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
    '    <p style="text-align: center; font-size: 3.5rem; margin-bottom: 5px; color: #2c3e50; font-weight: bold;">CicerOmicsExplorer</p>'
    '    <p style="text-align: center; font-size: 1.2rem; color: #7f8c8d; margin-bottom: 10px; font-weight: bold;">CHICKPEA DATABASE</p>'
    '    <!-- Paragraph with List and Special Effects -->'
    '    <br><p class="hp-paragraph">'
    '      This is a <b>creative</b> paragraph showcasing some <em>special effects</em>. Here\'s an unordered list of ideas:'
    '    </p>'
    '    <ul class="hp-list">'
    '      <li>Dynamic Images</li>'
    '      <li>Bold Text</li>'
    '      <li>Images</li>'
    '    </ul>'
    '    <!-- Additional Paragraphs -->'
    '    <p class="hp-additional-paragraph">'
    '    Hello ...'
    '    </p>'
    '    <p class="hp-additional-paragraph">'
    '      Hello ... <b>bold text</b> and <em>italicized text</em>...'
    '    </p>'
    '    <!-- More Text -->'
    '    <p class="hp-additional-paragraph">'
    '      hello ...'
    '    </p>'
    '  </div>'
    '</div>'
    '', unsafe_allow_html=True)

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

if __name__ == "__main__":
    home_page()
