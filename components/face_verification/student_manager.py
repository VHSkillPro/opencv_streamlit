import pandas as pd
import streamlit as st
from components.face_verification import get_table_data
from services.face_verification.service import (
    ClassService,
    StudentClassService,
    StudentService,
)

studentService = StudentService()
classService = ClassService()
studentClassService = StudentClassService()


@st.cache_data(ttl=3600)
def get_list_classes():
    classes = classService.repository.index()
    return classes


def show_form(id: str):
    hidden_all_forms()
    st.session_state["forms_state"][id] = True


def hidden_all_forms():
    for key in st.session_state["forms_state"].keys():
        st.session_state["forms_state"][key] = False


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
            second_cols[0].error("Ảnh thẻ sinh viên không được để trống.")
            is_valid = False
        if selfie is None:
            second_cols[1].error("Ảnh chụp mặt không được để trống.")
            is_valid = False

        if is_valid:
            result = studentService.insert(id, name, card, selfie)
            if result == "Thêm sinh viên thành công":
                get_table_data.clear()
                st.toast(result, icon=":material/check:")
            else:
                st.toast(result, icon=":material/error:")


def display_form_add_student_in_class():
    with st.form(key="form_add_student_in_class"):
        st.markdown(
            f"#### Thêm sinh viên vào lớp {st.session_state['filter_student']['class_id']}"
        )
        student_id_container = st.container()
        student_id = student_id_container.text_input("Mã sinh viên")

        cols = st.columns(8)
        btnSubmit = cols[0].form_submit_button(
            ":material/add: Thêm", use_container_width=True
        )
        cols[1].form_submit_button(
            ":material/close: Đóng", use_container_width=True, on_click=hidden_all_forms
        )

    if btnSubmit:
        is_valid = True
        if student_id.strip() == "":
            student_id_container.error("Mã sinh viên không được để trống.")
            is_valid = False

        if is_valid:
            result = studentClassService.insert(
                st.session_state["filter_student"]["class_id"], student_id
            )

            class_id = st.session_state["filter_student"]["class_id"]
            if result == f"Thêm sinh viên {student_id} vào lớp {class_id} thành công":
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
        st.session_state["filter_student"] = {"student_id": id, "student_name": name}
        get_table_data.clear()


def display_form_edit_student():
    if len(st.session_state["selected_students"]) != 1:
        return

    with st.form(key="form_edit"):
        st.markdown("#### Chỉnh sửa thông tin sinh viên")

        first_cols = st.columns(2)
        id = first_cols[0].text_input(
            "Mã sinh viên",
            value=st.session_state["selected_students"]["id"].values[0],
            disabled=True,
        )
        name = first_cols[1].text_input(
            "Tên sinh viên",
            value=st.session_state["selected_students"]["name"].values[0],
        )

        second_cols = st.columns(2)
        card = second_cols[0].file_uploader(
            "Ảnh thẻ sinh viên", type=["jpg", "jpeg", "png"]
        )
        second_cols[0].image(
            st.session_state["selected_students"]["card"].values[0],
            use_column_width=True,
            caption="Ảnh thẻ sinh viên hiện tại",
        )

        selfie = second_cols[1].file_uploader(
            "Ảnh chân dung", type=["jpg", "jpeg", "png"]
        )
        second_cols[1].image(
            st.session_state["selected_students"]["selfie"].values[0],
            use_column_width=True,
            caption="Ảnh chân dung hiện tại",
        )

        third_cols = st.columns(8)
        btnSubmit = third_cols[0].form_submit_button(
            ":material/edit: Chỉnh sửa", use_container_width=True
        )
        third_cols[1].form_submit_button(
            ":material/close: Đóng", use_container_width=True, on_click=hidden_all_forms
        )

    if btnSubmit:
        is_valid = True
        if name.strip() == "":
            first_cols[1].error("Tên sinh viên không được để trống.")
            is_valid = False

        if is_valid:
            result = studentService.update(id, name, card, selfie)
            if result == "Cập nhật sinh viên thành công":
                get_table_data.clear()
                st.session_state["selected_students"] = []
                st.toast(result, icon=":material/check:")
            else:
                st.toast(result, icon=":material/error:")


def handle_refresh():
    """
    Handle refresh button click event
    """

    st.session_state["filter_student"]["student_id"] = ""
    st.session_state["filter_student"]["student_name"] = ""
    get_table_data.clear()
    get_list_classes.clear()


@st.fragment()
def display_student_manager():
    st.header(":material/manage_accounts: Quản lý sinh viên")
    with st.container(border=True):
        button_cols = st.columns([1, 1, 1, 1, 1, 1, 2], vertical_alignment="center")

        # Show form actions
        if st.session_state["forms_state"]["form_add_student"] == True:
            if st.session_state["filter_student"]["class_id"] != "":
                display_form_add_student_in_class()
            else:
                display_form_add_student()
        elif st.session_state["forms_state"]["form_search_student"] == True:
            display_form_search_student()
        elif st.session_state["forms_state"]["form_edit_student"] == True:
            display_form_edit_student()

        # Show button refresh
        with button_cols[0]:
            st.button(
                ":material/refresh: Làm mới",
                use_container_width=True,
                on_click=handle_refresh,
            )

        # Show button add student
        with button_cols[1]:
            st.button(
                ":material/add: Thêm",
                use_container_width=True,
                on_click=lambda: show_form("form_add_student"),
            )

        # Show select class
        with button_cols[-1]:
            classes_raw = get_list_classes()
            classes = {class_["id"]: class_ for id, class_ in classes_raw.items()}
            classes_id = [""] + list(classes.keys())

            def on_change_class():
                st.session_state["filter_student"]["class_id"] = st.session_state[
                    "select_class"
                ]

            st.selectbox(
                "Chọn lớp",
                classes_id,
                format_func=lambda x: "Tất cả" if x == "" else classes[x]["name"],
                key="select_class",
                on_change=on_change_class,
            )

        # Show table data of students
        with st.container():
            table_data, students_raw = get_table_data(
                st.session_state["filter_student"]["student_id"],
                st.session_state["filter_student"]["student_name"],
                st.session_state["filter_student"]["class_id"],
            )

            # Update students data
            st.session_state["students_data"] = {
                "face_labels": [],
                "face_names": [],
                "card_face_features": [],
                "selfie_face_features": [],
            }

            for id, student in students_raw.items():
                st.session_state["students_data"]["face_labels"].append(student["id"])
                st.session_state["students_data"]["face_names"].append(student["name"])
                st.session_state["students_data"]["card_face_features"].append(
                    student["card_face_feature"]
                )
                st.session_state["students_data"]["selfie_face_features"].append(
                    student["selfie_face_feature"]
                )

            # Show table data
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
                    "selfie": st.column_config.ImageColumn("Ảnh chân dung"),
                },
                use_container_width=True,
                hide_index=True,
            )
            st.caption(
                """
                - Click đúp vào ô ảnh cần xem để phóng to ảnh.
                - Chọn một sinh viên để chỉnh sửa.
                - Chọn một hoặc nhiều sinh viên để xóa.
                - Nếu muốn thêm hoặc xoá sinh viên vào lớp, hãy chọn lớp trước khi thêm hoặc xoá sinh viên.
                """
            )

        # Save selected students
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

        @st.dialog("Xác nhận xóa")
        def handle_remove_student_in_class():
            st.write("Bạn có chắc chắn muốn xóa sinh viên đã chọn khỏi lớp không?")
            st.write("Hành động này không thể hoàn tác.")

            if st.button("Xóa"):
                ids = st.session_state["selected_students"]["id"].values
                class_id = st.session_state["filter_student"]["class_id"]
                for id in ids:
                    result = studentClassService.delete(class_id, id)
                    st.session_state["toasts"].append(
                        {
                            "body": result,
                            "icon": (
                                ":material/check:"
                                if result
                                == f"Xóa sinh viên {id} khỏi lớp {class_id} thành công"
                                else ":material/error:"
                            ),
                        }
                    )
                st.session_state["selected_students"] = []
                get_table_data.clear()
                st.rerun()

        # Show button search student
        with button_cols[2]:
            st.button(
                ":material/search: Tìm kiếm",
                use_container_width=True,
                on_click=lambda: show_form("form_search_student"),
            )

        # Show button remove student
        if len(st.session_state["selected_students"]) > 0:
            with button_cols[3]:
                if st.session_state["filter_student"]["class_id"] != "":
                    st.button(
                        ":material/delete: Xóa",
                        use_container_width=True,
                        on_click=handle_remove_student_in_class,
                    )
                else:
                    st.button(
                        ":material/delete: Xóa",
                        use_container_width=True,
                        on_click=handle_remove,
                    )

        # Show button edit student
        if len(st.session_state["selected_students"]) == 1:
            with button_cols[4]:
                st.button(
                    ":material/edit: Chỉnh sửa",
                    use_container_width=True,
                    on_click=lambda: show_form("form_edit_student"),
                )

        return data_editor
