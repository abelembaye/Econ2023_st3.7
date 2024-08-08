
# conda activate cenv311
# streamlit run app.py
# if packages updated run "pip freeze > requirements.txt "
# # If not installed, tar.gz file install from GITHUB: pip install https://github.com/abelembaye/drawable_package/raw/master/streamlit-drawable-canvas-0.9.3.10.tar.gz  # just try to see the URL of the .tar.gz file as outsider and add /raw/ before the branch name, tricky
import hmac
import streamlit as st
# from helper_fns import check_password

if "course" not in st.session_state:
    st.session_state.course = None

if "username" not in st.session_state:
    st.session_state.username = None

if "wkd" not in st.session_state:
    st.session_state.wkd = None

COURSES = [None, "Econ2023"]  # , "Econ3333"]


# if not check_password():
#     st.stop()


def login():
    st.header("Log in")
    # course is take from this selection; course can be replaced by password
    course = st.selectbox("Choose your Course", COURSES)
    # lastname = st.text_input("Enter your last name")
    # wkd = st.text_input(
    #     r"Please your enter your working directory so that your work is saved and uploaded when you comeback to the same assessment. mine is for example, C:\\Users\\aembaye\\Documents")
    if st.button("Log in"):
        st.session_state.course = course
        # st.session_state.username = lastname  # added by me
        st.session_state.username = "lastname"
        # st.session_state.wkd = wkd
        st.session_state.wkd = "C:/Users/aembaye/Documents"

        st.rerun()


def logout():
    st.session_state.course = None
    st.session_state.username = None
    st.rerun()


course = st.session_state.course

# logout() function as a page
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# this is just an example of page outside of folder
settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

quiz_01 = st.Page(
    "Econ2023/quiz_01.py",
    title="Quiz 01",
    icon=":material/healing:",
    default=(course == "Econ2023"),
)

quiz_02 = st.Page(
    "Econ2023/quiz_02.py", title="Quiz 02", icon=":material/handyman:"
)


account_pages = [logout_page, settings]
Econ2023_pages = [quiz_01, quiz_02]
# the list here must be unique than the above
# Econ3333_pages = [quiz_01x, quiz_02x]


st.title("Quiz Apps")

st.logo("images/horizontal_blue.png", icon_image="images/icon_blue.png")

page_dict = {}

if st.session_state.course in ["Econ2023"]:  # ["Requester", "Admin"]
    page_dict["Econ2023"] = Econ2023_pages
# if st.session_state.course in ["Econ3333"]:  # ["Econ2023", "Admin"]
#     page_dict["Econ3333"] = Econ3333_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)

else:
    pg = st.navigation([st.Page(login)])

pg.run()
