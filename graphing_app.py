import streamlit as st
# import hmac
import streamlit as st
import pandas as pd
import numpy as np
import json
import sys
import os
import random
# import mysqlclient  # pip install mysqlclient (hard to work with this pacakge)
# import PIL
from PIL import Image, UnidentifiedImageError
# import pymysql  # pip install pymysql
import io
from io import BytesIO
import base64
from datetime import date
import pdfkit  # pip install pdfkit
# pip install Jinja2
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader  # pip install
import time
from time import sleep
# import streamlit_authenticator as stauth  # pip install streamlit-authenticator
# import mysql.connector  # pip install mysql-connector-python
# from mysql.connector import FieldType  # pip install mysql-connector-python
from sqlalchemy.sql import text  # pip install SQLAlchemy
import sqlite3  # pip install db-sqlite3

# import toml
# from streamlit_drawable_canvas import st_canvas
import sqlalchemy.exc
from collections import OrderedDict
from helper_fns import start_assessment, next_question, previous_question, finish_assessment, serialize_data, make_ss_user_inputs, make_html_template


if "course" not in st.session_state:
    st.session_state.course = None
st.session_state.course = "Econ2023"

if "username" not in st.session_state:
    st.session_state.username = None
st.session_state.username = "aembaye"
if "incloud" not in st.session_state:
    # change this to True to enable cloud deployment
    st.session_state.incloud = True  # False  #
if "wkd" not in st.session_state:
    st.session_state.wkd = None
st.session_state.wkd = "C:/Users/aembaye/OneDrive - University of Arkansas/C2-embaye/Rh/Learn/_Python/myProjects"

# define things that are unique to the assignment/activity
pagetitle = pageheader = "Quiz 1"
act_name = "quiz_01"
questions_jsonfile = 'questions_' + act_name + '.json'
dbtable_file = "db_" + act_name + ".json"
# r"C:\Users\aembaye\Documents"
workingdir = st.session_state.wkd

# Ensure the working directory exists
if not os.path.exists(workingdir):
    os.makedirs(workingdir)

# Construct the full path to the database file
full_path_db = os.path.join(workingdir, dbtable_file)
st.write(full_path_db)

# Load the questions from the JSON file
try:
    with open(questions_jsonfile, 'r') as file:
        questions = json.load(file)
except FileNotFoundError:
    st.error(f"Questions file {questions_jsonfile} not found.")
    questions = []
except Exception as e:
    st.error(f"An error occurred while loading questions: {e}")
    questions = []

# Load the default values from the database file
try:
    with open(full_path_db, "r") as json_file:
        default_vals = json.load(json_file)
except FileNotFoundError:
    st.warning(
        f"Database file {full_path_db} not found. Setting default values to an empty dictionary.")
    default_vals = {}
except Exception as e:
    st.error(f"An error occurred while loading default values: {e}")
    default_vals = {}

if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {}
# inputs4template = {}  # for the html template; all the user inputs can be used from user_inputs dict; but, for image upload, we cannot do that and we have to create for it
if 'inputs4template' not in st.session_state:
    st.session_state.inputs4template = {}

# Initialize session state variables
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = -1
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if not st.session_state.quiz_started:
    st.button("Start", on_click=start_assessment)

else:
    make_ss_user_inputs(questions, default_vals)

    col1, col2, col3 = st.columns([2, 8, 2])  # Adjust the ratio as needed

    if st.session_state.current_question_index > 0:
        with col1:
            st.button("Previous", on_click=previous_question)

    if st.session_state.current_question_index < len(questions) - 1:
        with col3:
            st.button("Next", on_click=next_question)
    else:
        with col3:
            st.button("Finish", on_click=finish_assessment)

# Display the character counts
# st.write(f"Character counts: {char_counts}")
# sys.exit()
# if True:
# Serialize user_inputs excluding or converting non-serializable data
serializable_user_inputs = serialize_data(st.session_state.user_inputs)

# save user entry in .json file
save_button = st.button(label="save your work", key="save_button")
if save_button:
    # Serialize and save user_inputs to act01_db.json
    with open(full_path_db, "w") as json_file:
        json.dump(serializable_user_inputs, json_file)
        st.write(
            f"User input saved as .json file in the file full path: {full_path_db} or {json_file}")

submit = st.button(
    "Generate PDF", key="generate_button")

# generate template.html with rendered user_inputs
template = make_html_template(questions)  # returns template

# sys.exit()
# if True:
# st.write(f'uploads: {uploads}')
# to convert the template.html file to pdf
if submit:
    # Render the template with the user_inputs dictionary
    # html = template.render(**user_inputs)
    html = template

    if st.session_state.incloud == True:
        pdf = pdfkit.from_string(html, False)  # when in cloud deployment

    # if local development:
    else:
        # must be comments in deployment in cloud
        path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

        # must be commented in deployment in cloud
        config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        pdf = pdfkit.from_string(html,  configuration=config)
        # pdf = pdfkit.from_string(
        #     html, f"{st.session_state.username}_Pset03_completed.pdf", configuration=config)

    st.success(
        "🎉 Your PDF file has been generated! Download it below and submit it in gradescope!")

    st.download_button(
        # "⬇️ Download HTML",
        "⬇️ Download pdf",
        # data=html,
        data=pdf,
        # file_name=f"{st.session_state.username}_Pset03_completed.html",
        file_name=f"{st.session_state.username}_{act_name}.pdf",
        # mime="text/html",
        mime="application/octet-stream",
    )
