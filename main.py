# QR CODE generator and scanner using Python

import pyqrcode
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import streamlit as st
from streamlit_option_menu import option_menu
import random
from urllib import request

# generates random filename for the image to download 
def generate_file_name(extension: str): 
    file_name = random.randrange(10000000, 20000000)
    extension = extension
    return f'{file_name}{extension}'

# creates qrcode by getting data from userto be encoded 
def create_qr():
    widgets = st.multiselect(
        label='Select',
        options=("Name", "Phone", "E-mail", "Address", "URL", "Others")
    )

    if st.checkbox("Select all"):
        widgets = ("Name", "Phone", "E-mail", "Address", "URL", "Others")
    
    content = f""    
    for widget in widgets:
        if widget in ("Name", "Phone", "E-mail"):
            content += f"{widget}" + ": " + st.text_input(label=widget, placeholder=f"Enter {widget.lower()} here") + "\n"
        elif widget == "URL":
            content += f"{widget}" + ": " + st.text_input(label=widget, placeholder=f"Enter {widget.lower()} here").lower() + "\n"
        elif widget == "Address":
            content += f"{widget}" + ": " + st.text_area(label=widget, placeholder=f"Enter {widget.lower()} here") + "\n"
        elif widget == "Others":
            content += st.text_area(label=widget, placeholder=f"Enter {widget.lower()} here") + "\n"
    
    if content:

        st.markdown("""
            <style>
                div.row-widget.stButton, div.css-1kyxreq.etr89bj2, div.row-widget.stDownloadButton{
                    display: flex;
                    justify-content: center;
                }
            </style>
        """, unsafe_allow_html=True)

        if st.button(label="Create"):
            # creates qrcode based on the content
            qr = pyqrcode.create(content=content)

            # saves the qrcode file
            filename = generate_file_name(".png")
            qr.png(file=filename, scale=5)

            # displays qrcode in the screen
            st.image(filename)

            # downloads the qrcode
            with open(filename, "rb") as file:
                st.download_button(label="Download", data=file, file_name=filename)

# scans the picture which is got from the camera and
# displays the content which is encoded in the qrcode
def scan_qr():
    img_file_buffer = st.camera_input("Take a pic of the QR CODE", help="You can also scan BARCODE")
    if img_file_buffer:
        bytes_data = img_file_buffer.getvalue()
        image = cv2.imdecode(np.frombuffer(bytes_data, np.int8), 1)

        qr = decode(image)
        if qr:
            qr = qr[0]  

            rect_pts = np.array(qr.rect, dtype=np.int16)  # bounding points to draw rectangle

            poly_pts = np.array(qr.polygon, dtype=np.int32)  # bounding points to draw polygon(acutally rectangle)

            cropped_img = image[rect_pts[1]:rect_pts[1]+rect_pts[3], rect_pts[0]:rect_pts[0]+rect_pts[2]]

            exact_qr = cv2.imencode(ext='.jpg', img=cropped_img)[1]

            st.markdown("""
                <style>
                div.css-1n76uvr.e1tzin5v0{
                    text-align: justify;
                }
                </style>
            """, unsafe_allow_html=True)

            data = (qr.data).decode()  # getting data encoded in the qrcode
            with st.container():
                # st.image(cropped_img)
                copied_data = data
                if "\n" in copied_data:
                    datas = copied_data.split("\n")
                    for copied_data in datas:
                        st.write(copied_data)
                else:
                    st.write(copied_data)
                    # st.download_button(label='Download scanned QR Code', data=exact_qr.tobytes(), file_name=generate_file_name('.jpg'))
            # downloads the data as text file
            st.download_button(label='Download data', data=data, file_name=generate_file_name('.txt'))

        else:
            st.error("Retake a pic of the QR CODE")

# sets page icon
request.urlretrieve("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcwXAIghq_CM2XrNs9FxwIdruhVwteaBhQJw&usqp=CAU", filename="title_icon")
title_icon = cv2.imread("title_icon")
st.set_page_config(page_title='QR Generator & Scanner',page_icon='title_icon')

# removes default sidebar and footer note
st.markdown("""
    <style>
        #MainMenu{
            display: none;
        }
        footer.css-1lsmgbg.egzxvld0{
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# st.title("QR Code Generator & Scanner")
st.markdown("""
    <h1 align="center">QR Code <br>Generator & Scanner</h1>
""", unsafe_allow_html=True)

# creates navigation bar
options = ('Create', 'Scan')
selected = option_menu(
    menu_title=None, 
    options=options,
    default_index=0,
    orientation="horizontal",
    icons=("qr-code", "qr-code-scan")
)

if selected == options[0]:
    create_qr()
if selected == options[1]:
    scan_qr()