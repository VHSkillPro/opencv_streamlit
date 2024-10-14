import pandas as pd
import streamlit as st
from services.face_verification.service import StudentService

studentService = StudentService()


def show_form(id: str):
    st.session_state[id] = True


def hidden_all_forms():
    forms_id = ["form_add_student", "form_edit_student", "form_search_student"]
    for id in forms_id:
        st.session_state[id] = False


@st.cache_data(ttl="1h")
def get_table_data(filter: object):
    st.session_state["face_labels"] = []
    st.session_state["card_face_features"] = []
    st.session_state["selfie_face_features"] = []

    students = studentService.find(filter)
    table_data = {"checkbox": [], "id": [], "name": [], "card": [], "selfie": []}
    for id, student in students.items():
        table_data["checkbox"].append(False)
        table_data["id"].append(student["id"])
        table_data["name"].append(student["name"])
        table_data["card"].append(studentService.storage.get_url(student["card"], 3600))
        table_data["selfie"].append(
            studentService.storage.get_url(student["selfie"], 3600)
        )

        st.session_state["face_labels"].append(student["id"])
        st.session_state["card_face_features"].append(student["card_face_feature"])
        st.session_state["selfie_face_features"].append(student["selfie_face_feature"])

    return table_data


def display_form_add_student():
    with st.form(key="form_add"):
        st.markdown("#### Thêm sinh viên")

        first_cols = st.columns(2)
        id = first_cols[0].text_input("Mã sinh viên")
        name = first_cols[1].text_input("Tên sinh viên")

        second_cols = st.columns(2)
        card = second_cols[0].file_uploader(
            "Ảnh thẻ sinh viên", type=["jpg", "jpeg", "png"]
        )
        selfie = second_cols[1].file_uploader(
            "Ảnh chân dung", type=["jpg", "jpeg", "png"]
        )

        cols = st.columns(8)
        btnSubmit = cols[0].form_submit_button(
            ":material/add: Thêm", use_container_width=True
        )
        btnClose = cols[1].form_submit_button(
            ":material/close: Đóng", use_container_width=True
        )

    if btnSubmit:
        is_valid = True
        if id.strip() == "":
            first_cols[0].error("Mã sinh viên không được để trống.")
            is_valid = False
        if name.strip() == "":
            first_cols[1].error("Tên sinh viên không được để trống.")
            is_valid = False
        if card is None:
            second_cols[0].error("Ảnh thẻ sinh viên không được để trống.")
            is_valid = False
        if selfie is None:
            second_cols[1].error("Ảnh chân dung không được để trống.")
            is_valid = False

        if is_valid:
            result = studentService.insert(id, name, card, selfie)
            if result == "Thêm sinh viên thành công":
                hidden_all_forms()
                get_table_data.clear()
                st.toast(result, icon=":material/check:")
            else:
                st.toast(result, icon=":material/error:")

    if btnClose:
        hidden_all_forms()
        st.rerun(scope="fragment")


@st.fragment
def display_student_manager():
    with st.container(border=True):
        cols = st.columns(8)
        with cols[0]:
            st.button(
                ":material/refresh: Làm mới",
                use_container_width=True,
                on_click=lambda: get_table_data.clear(),
            )

        with cols[1]:

            def show_form_add():
                hidden_all_forms()
                show_form("form_add_student")

            st.button(
                ":material/add: Thêm",
                use_container_width=True,
                on_click=show_form_add,
            )

        with cols[2]:

            def show_form_search():
                hidden_all_forms()
                show_form("form_search_student")

            st.button(
                ":material/search: Tìm kiếm",
                use_container_width=True,
                on_click=show_form_search,
            )

        if st.session_state["form_add_student"] == True:
            display_form_add_student()

        with st.container():
            table_data = get_table_data(
                {
                    "id": st.session_state["filter_id"],
                    "name": st.session_state["filter_name"],
                }
            )
            if len(table_data["id"]) == 0:
                st.write("Không có sinh viên nào.")
                return pd.DataFrame(table_data)

            data_editor = st.data_editor(
                pd.DataFrame(table_data),
                column_config={
                    "checkbox": st.column_config.CheckboxColumn("Chọn"),
                    "id": st.column_config.TextColumn("Mã sinh viên", disabled=True),
                    "name": st.column_config.TextColumn("Tên sinh viên", disabled=True),
                    "card": st.column_config.ImageColumn("Thẻ sinh viên"),
                    "selfie": st.column_config.ImageColumn("Chân dung"),
                },
                use_container_width=True,
                hide_index=True,
            )

            return data_editor
