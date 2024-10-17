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

    students = studentService.find(filter)
    table_data = {"checkbox": [], "id": [], "name": [], "card": []}
    for id, student in students.items():
        table_data["checkbox"].append(False)
        table_data["id"].append(student["id"])
        table_data["name"].append(student["name"])
        table_data["card"].append(studentService.storage.get_url(student["card"], 3600))

        st.session_state["face_labels"].append(student["id"])
        st.session_state["card_face_features"].append(student["card_face_feature"])

    return table_data


def display_form_add_student():
    with st.form(key="form_add"):
        st.markdown("#### Thêm sinh viên")

        first_cols = st.columns(2)
        id = first_cols[0].text_input("Mã sinh viên")
        name = first_cols[1].text_input("Tên sinh viên")

        second_cols = st.container()
        card = second_cols.file_uploader(
            "Ảnh thẻ sinh viên", type=["jpg", "jpeg", "png"]
        )

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
            first_cols[0].error("Mã sinh viên không được để trống.")
            is_valid = False
        if name.strip() == "":
            first_cols[1].error("Tên sinh viên không được để trống.")
            is_valid = False
        if card is None:
            second_cols.error("Ảnh thẻ sinh viên không được để trống.")
            is_valid = False

        if is_valid:
            result = studentService.insert(id, name, card)
            if result == "Thêm sinh viên thành công":
                get_table_data.clear()
                st.toast(result, icon=":material/check:")
            else:
                st.toast(result, icon=":material/error:")


def display_form_search_student():
    with st.form(key="form_search"):
        st.markdown("#### Tìm kiếm sinh viên")

        cols = st.columns(2)
        id = cols[0].text_input("Mã sinh viên")
        name = cols[1].text_input("Tên sinh viên")

        cols = st.columns(8)
        btnSubmit = cols[0].form_submit_button(
            ":material/search: Tìm kiếm", use_container_width=True
        )
        cols[1].form_submit_button(
            ":material/close: Đóng", use_container_width=True, on_click=hidden_all_forms
        )

    if btnSubmit:
        st.session_state["filter_id"] = id
        st.session_state["filter_name"] = name
        get_table_data.clear()


def display_form_edit_student():
    if len(st.session_state["selected_students"]) != 1:
        return

    with st.form(key="form_edit"):
        st.markdown("#### Chỉnh sửa thông tin sinh viên")

        first_cols = st.columns((2, 1), gap="large")
        id = first_cols[0].text_input(
            "Mã sinh viên",
            value=st.session_state["selected_students"]["id"].values[0],
            disabled=True,
        )
        name = first_cols[0].text_input(
            "Tên sinh viên",
            value=st.session_state["selected_students"]["name"].values[0],
        )
        card = first_cols[0].file_uploader(
            "Ảnh thẻ sinh viên", type=["jpg", "jpeg", "png"]
        )

        first_cols[1].image(
            st.session_state["selected_students"]["card"].values[0],
            use_column_width=True,
            caption="Ảnh thẻ sinh viên hiện tại",
        )

        cols = st.columns(8)
        btnSubmit = cols[0].form_submit_button(
            ":material/edit: Chỉnh sửa", use_container_width=True
        )
        cols[1].form_submit_button(
            ":material/close: Đóng", use_container_width=True, on_click=hidden_all_forms
        )

    if btnSubmit:
        is_valid = True
        if name.strip() == "":
            first_cols[0].error("Tên sinh viên không được để trống.")
            is_valid = False

        if is_valid:
            result = studentService.update(id, name, card)
            if result == "Cập nhật sinh viên thành công":
                get_table_data.clear()
                st.session_state["selected_students"] = []
                st.toast(result, icon=":material/check:")
            else:
                st.toast(result, icon=":material/error:")


@st.fragment
def display_student_manager():
    with st.container(border=True):
        cols = st.columns(8)
        with cols[0]:

            def handle_refresh():
                st.session_state["filter_id"] = ""
                st.session_state["filter_name"] = ""
                get_table_data.clear()

            st.button(
                ":material/refresh: Làm mới",
                use_container_width=True,
                on_click=handle_refresh,
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
        elif st.session_state["form_search_student"] == True:
            display_form_search_student()
        elif st.session_state["form_edit_student"] == True:
            display_form_edit_student()

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
                    "checkbox": st.column_config.CheckboxColumn("Chọn", width="small"),
                    "id": st.column_config.TextColumn(
                        "Mã sinh viên", disabled=True, width="large"
                    ),
                    "name": st.column_config.TextColumn(
                        "Tên sinh viên", disabled=True, width="large"
                    ),
                    "card": st.column_config.ImageColumn(
                        "Thẻ sinh viên", width="medium"
                    ),
                },
                use_container_width=True,
                hide_index=True,
            )
            st.caption("- Click đúp vào ô ảnh cần xem để phóng to ảnh.")

            st.session_state["selected_students"] = data_editor[
                data_editor["checkbox"] == True
            ]

        @st.dialog("Xác nhận xóa")
        def handle_remove():
            st.write("Bạn có chắc chắn muốn xóa sinh viên đã chọn không?")
            st.write("Hành động này không thể hoàn tác.")

            if st.button("Xóa"):
                ids = st.session_state["selected_students"]["id"].values
                for id in ids:
                    result = studentService.delete(id)
                    st.session_state["toasts"].append(
                        {
                            "body": result,
                            "icon": (
                                ":material/check:"
                                if result == f"Xóa sinh viên {id} thành công"
                                else ":material/error:"
                            ),
                        }
                    )
                st.session_state["selected_students"] = []
                get_table_data.clear()
                st.rerun()

        if len(st.session_state["selected_students"]) > 0:
            with cols[3]:
                st.button(
                    ":material/delete: Xóa",
                    use_container_width=True,
                    on_click=handle_remove,
                )

            if len(st.session_state["selected_students"]) == 1:
                with cols[4]:

                    def show_form_edit():
                        hidden_all_forms()
                        show_form("form_edit_student")

                    st.button(
                        ":material/edit: Chỉnh sửa",
                        use_container_width=True,
                        on_click=show_form_edit,
                    )

            return data_editor
