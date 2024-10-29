import pandas as pd
import streamlit as st
from components.face_verification import get_class_table_data
from components.face_verification.student_manager import hidden_all_forms, show_form
from services.face_verification.service import ClassService

classService = ClassService()


def display_form_add_class():
    with st.form(key="form_add_class"):
        st.markdown("#### Thêm lớp học")

        first_cols = st.columns(2)
        id = first_cols[0].text_input("Mã lớp học")
        name = first_cols[1].text_input("Tên lớp học")

        cols = st.columns(8)
        btnSubmit = cols[0].form_submit_button(
            ":material/add: Thêm", use_container_width=True
        )
        cols[1].form_submit_button(
            ":material/close: Đóng", use_container_width=True, on_click=hidden_all_forms
        )

    if btnSubmit:
        is_valid = True
        if id.strip() == "":
            first_cols[0].error("Mã lớp học không được để trống.")
            is_valid = False
        if name.strip() == "":
            first_cols[1].error("Tên lớp học không được để trống.")
            is_valid = False

        if is_valid:
            result = classService.insert(id, name)
            if result == f"Thêm lớp {id} thành công":
                get_class_table_data.clear()
                st.toast(result, icon=":material/check:")
            else:
                st.toast(result, icon=":material/check:")


def display_form_search_class():
    with st.form(key="form_search_class"):
        st.markdown("#### Tìm kiếm lớp học")

        first_cols = st.columns(2)
        id = first_cols[0].text_input("Mã lớp học")
        name = first_cols[1].text_input("Tên lớp học")

        cols = st.columns(8)
        btnSubmit = cols[0].form_submit_button(
            ":material/search: Tìm kiếm", use_container_width=True
        )
        cols[1].form_submit_button(
            ":material/close: Đóng", use_container_width=True, on_click=hidden_all_forms
        )

    if btnSubmit:
        st.session_state["filter_class"] = {
            "class_id": id,
            "class_name": name,
        }
        get_class_table_data.clear()


def display_form_edit_class():
    if len(st.session_state["selected_classes"]) != 1:
        return

    with st.form(key="_form_edit_class"):
        st.markdown("#### Chỉnh sửa thông tin lớp học")

        first_cols = st.columns(2)
        id = first_cols[0].text_input(
            "Mã lớp học",
            value=st.session_state["selected_classes"]["id"].values[0],
            disabled=True,
        )
        name = first_cols[1].text_input(
            "Tên lớp học",
            value=st.session_state["selected_classes"]["name"].values[0],
        )

        cols = st.columns(8)
        btnSubmit = cols[0].form_submit_button(
            ":material/edit: Sửa", use_container_width=True
        )
        cols[1].form_submit_button(
            ":material/close: Đóng", use_container_width=True, on_click=hidden_all_forms
        )

    if btnSubmit:
        is_valid = True
        if name.strip() == "":
            first_cols[1].error("Tên lớp học không được để trống.")
            is_valid = False

        if is_valid:
            result = classService.update(id, name)
            if result == f"Cập nhật lớp {id} thành công":
                get_class_table_data.clear()
                st.session_state["selected_classes"] = []
                st.toast(result, icon=":material/check:")
            else:
                st.toast(result, icon=":material/error:")


def handle_refresh():
    """
    Handle refresh button click
    """

    st.session_state["filter_class"] = {
        "class_id": "",
        "class_name": "",
    }
    st.session_state["selected_classes"] = []
    get_class_table_data.clear()


@st.fragment()
def display_class_manager():
    st.header(":material/manage_accounts: Quản lý lớp học")
    with st.container(border=True):
        button_cols = st.columns(8)

        # Show button refresh
        with button_cols[0]:
            st.button(
                ":material/refresh: Làm mới",
                use_container_width=True,
                on_click=handle_refresh,
                key="button_refresh_class",
            )

        # Show button add class
        with button_cols[1]:
            st.button(
                ":material/add: Thêm",
                use_container_width=True,
                on_click=lambda: show_form("form_add_class"),
                key="button_add_class",
            )

        # Show button search class
        with button_cols[2]:
            st.button(
                ":material/search: Tìm kiếm",
                use_container_width=True,
                on_click=lambda: show_form("form_search_class"),
                key="button_search_class",
            )

        # Show form actions
        if st.session_state["forms_state"]["form_add_class"] == True:
            display_form_add_class()
        elif st.session_state["forms_state"]["form_search_class"] == True:
            display_form_search_class()
        elif st.session_state["forms_state"]["form_edit_class"] == True:
            display_form_edit_class()

        # Show table data of classes
        with st.container():
            table_data = get_class_table_data(
                st.session_state["filter_class"]["class_id"],
                st.session_state["filter_class"]["class_name"],
            )

            if len(table_data["id"]) == 0:
                st.write("Không có lớp học nào.")
                return pd.DataFrame(table_data)

            data_editor = st.data_editor(
                pd.DataFrame(table_data),
                column_config={
                    "checkbox": st.column_config.CheckboxColumn("Chọn"),
                    "id": st.column_config.TextColumn("Mã lớp học", disabled=True),
                    "name": st.column_config.TextColumn("Tên lớp học", disabled=True),
                },
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                """
                - Chọn một lớp học để chỉnh sửa.
                - Chọn một hoặc nhiều lớp học để xóa.
                """
            )

        # Save selected classes
        st.session_state["selected_classes"] = data_editor[
            data_editor["checkbox"] == True
        ]

        # Show button delete
        with button_cols[3]:

            @st.dialog("Xác nhận xóa")
            def handle_remove():
                st.write("Bạn có chắc chắn muốn xóa lớp đã chọn không?")
                st.write("Hành động này không thể hoàn tác.")

                if st.button("Xóa"):
                    ids = st.session_state["selected_classes"]["id"].values
                    for id in ids:
                        result = classService.delete(id)
                        st.session_state["toasts"].append(
                            {
                                "body": result,
                                "icon": (
                                    ":material/check:"
                                    if result == f"Xóa lớp {id} thành công"
                                    else ":material/error:"
                                ),
                            }
                        )
                    st.session_state["selected_classes"] = []
                    get_class_table_data.clear()
                    st.rerun()

            if len(st.session_state["selected_classes"]) > 0:
                st.button(
                    ":material/delete: Xóa",
                    use_container_width=True,
                    on_click=handle_remove,
                )

        # Show button edit
        with button_cols[4]:
            if len(st.session_state["selected_classes"]) == 1:
                st.button(
                    ":material/edit: Chỉnh sửa",
                    use_container_width=True,
                    on_click=lambda: show_form("form_edit_class"),
                )

    return data_editor
