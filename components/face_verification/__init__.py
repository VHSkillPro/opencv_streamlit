import streamlit as st
from services.face_verification.service import (
    ClassService,
    StudentClassService,
    StudentService,
)

studentService = StudentService()
classService = ClassService()
studentClassService = StudentClassService()


def init_session_state():
    if "filter_student" not in st.session_state:
        st.session_state["filter_student"] = {
            "student_id": "",
            "student_name": "",
            "class_id": "",
        }

    if "filter_class" not in st.session_state:
        st.session_state["filter_class"] = {
            "class_id": "",
            "class_name": "",
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
            "form_add_class": False,
            "form_edit_class": False,
            "form_search_class": False,
        }

    if "selected_students" not in st.session_state:
        st.session_state["selected_students"] = []

    if "selected_classes" not in st.session_state:
        st.session_state["selected_classes"] = []


@st.cache_resource(ttl="1h")
def get_table_data(student_id: str = "", student_name: str = "", class_id: str = ""):
    """
    Get table data of students

    ## Arguments:
        student_id - Student id to filter
        student_name - Student name to filter

    ## Returns:
        Table data of students and students data
    """

    students = None
    if class_id == "":
        students = studentService.find(student_id, student_name)
    else:
        students = studentClassService.find(class_id, student_id, student_name)

    table_data = {"checkbox": [], "id": [], "name": [], "card": [], "selfie": []}
    for id, student in students.items():
        table_data["checkbox"].append(False)
        table_data["id"].append(student["id"])
        table_data["name"].append(student["name"])
        table_data["card"].append(studentService.storage.get_url(student["card"], 3600))
        table_data["selfie"].append(
            studentService.storage.get_url(student["selfie"], 3600)
        )

    return table_data, students


@st.cache_data(ttl="1h")
def get_class_table_data(class_id: str = "", class_name: str = ""):
    """
    Get table data of classes

    ## Arguments:
        class_id - Class id to filter
        class_name - Class name to filter

    ## Returns:
        Table data of classes
    """

    classes = classService.find(class_id, class_name)
    table_data = {"checkbox": [], "id": [], "name": []}

    for id, class_ in classes.items():
        table_data["checkbox"].append(False)
        table_data["id"].append(class_["id"])
        table_data["name"].append(class_["name"])

    return table_data
