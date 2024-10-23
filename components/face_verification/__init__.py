import streamlit as st
from services.face_verification.service import StudentService

studentService = StudentService()


def init_session_state():
    if "filter_student" not in st.session_state:
        st.session_state["filter_student"] = {
            "student_id": "",
            "student_name": "",
        }

    if "students_data" not in st.session_state:
        st.session_state["students_data"] = {
            "face_labels": [],
            "face_names": [],
            "card_face_features": [],
            "selfie_face_features": [],
        }

    if "toasts" not in st.session_state:
        st.session_state["toasts"] = []

    if "forms_state" not in st.session_state:
        st.session_state["forms_state"] = {
            "form_add_student": False,
            "form_edit_student": False,
            "form_search_student": False,
        }

    if "selected_students" not in st.session_state:
        st.session_state["selected_students"] = []


@st.cache_data(ttl="1h")
def get_table_data(student_id: str = "", student_name: str = ""):
    """
    Get table data of students

    ## Arguments:
        student_id - Student id to filter
        student_name - Student name to filter

    ## Returns:
        Table data of students
    """

    st.session_state["students_data"] = {
        "face_labels": [],
        "face_names": [],
        "card_face_features": [],
        "selfie_face_features": [],
    }

    students = studentService.find(student_id, student_name)
    table_data = {"checkbox": [], "id": [], "name": [], "card": [], "selfie": []}

    for id, student in students.items():
        table_data["checkbox"].append(False)
        table_data["id"].append(student["id"])
        table_data["name"].append(student["name"])
        table_data["card"].append(studentService.storage.get_url(student["card"], 3600))
        table_data["selfie"].append(
            studentService.storage.get_url(student["selfie"], 3600)
        )

        st.session_state["students_data"]["face_labels"].append(student["id"])
        st.session_state["students_data"]["face_names"].append(student["name"])
        st.session_state["students_data"]["card_face_features"].append(
            student["card_face_feature"]
        )
        st.session_state["students_data"]["selfie_face_features"].append(
            student["selfie_face_feature"]
        )

    return table_data
