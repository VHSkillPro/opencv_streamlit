import streamlit as st


def init_session_state():
    if "filter_id" not in st.session_state:
        st.session_state["filter_id"] = ""
    if "filter_name" not in st.session_state:
        st.session_state["filter_name"] = ""

    if "face_names" not in st.session_state:
        st.session_state["face_names"] = []
    if "face_labels" not in st.session_state:
        st.session_state["face_labels"] = []
    if "card_face_features" not in st.session_state:
        st.session_state["card_face_features"] = []
    if "selected_students" not in st.session_state:
        st.session_state["selected_students"] = []
    if "toasts" not in st.session_state:
        st.session_state["toasts"] = []

    forms_id = ["form_add_student", "form_edit_student", "form_search_student"]
    for id in forms_id:
        if id not in st.session_state:
            st.session_state[id] = False
