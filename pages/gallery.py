import streamlit as st
from streamlit.components.v1 import html
import base64
from backend import generate_signed_url,img_to_base64
import requests

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

gallery_html()