import pandas as pd
from PIL import Image
import streamlit as st
from services.face_verification.db import StudentService

studentService = StudentService()

if "submit_form" not in st.session_state:
    st.session_state["submit_form"] = False

if "show_form_add" not in st.session_state:
    st.session_state["show_form_add"] = False


@st.cache_data(ttl="1h")
def get_table_data():
    students = studentService.get_all()
    table_data = {"checkbox": [], "id": [], "card": [], "selfie": []}
    for id, student in students.items():
        table_data["checkbox"].append(False)
        table_data["id"].append(student["id"])
        table_data["card"].append(studentService.get_url_from_storage(student["card"]))
        table_data["selfie"].append(
            studentService.get_url_from_storage(student["selfie"], 3600)
        )
    return table_data


def display_table_students():
    table_data = get_table_data()
    if len(table_data["id"]) == 0:
        st.write("Không có sinh viên nào.")
        return pd.DataFrame(table_data)

    return st.data_editor(
        pd.DataFrame(table_data),
        column_config={
            "checkbox": st.column_config.CheckboxColumn("Chọn"),
            "id": st.column_config.TextColumn("Mã sinh viên", disabled=True),
            "card": st.column_config.ImageColumn("Thẻ sinh viên"),
            "selfie": st.column_config.ImageColumn("Chân dung"),
        },
        use_container_width=True,
        hide_index=True,
    )


def display_manage_students():
    def show_form_add():
        st.session_state["show_form_add"] = True
        st.session_state["submit_form"] = False

    def hide_form_add():
        st.session_state["show_form_add"] = False
        st.session_state["submit_form"] = False

    st.header("1. Danh sách sinh viên")
    container_action = st.container()
    container_form_add = st.container()
    data_editor = display_table_students()
    st.caption("- Click đúp vào ô ảnh cần xem để phóng to ảnh.")

    with container_action:
        cols = st.columns([1, 1, 8])
        with cols[0]:
            st.button("Thêm", use_container_width=True, on_click=show_form_add)
        with cols[1]:

            @st.dialog("Bạn có chắc chắn muốn xóa sinh viên đã chọn không?")
            def handle_remove_students():
                st.write("Danh sách sinh viên sẽ không thể khôi phục sau khi xóa.")
                st.write("Hãy chắc chắn trước khi xóa.")
                if st.button("Xác nhận"):
                    ids = data_editor[data_editor["checkbox"] == True]["id"].tolist()
                    haveChanges = False
                    for id in ids:
                        if studentService.delete(id):
                            haveChanges = True
                            st.toast(
                                f"Xóa sinh viên {id} thành công",
                                icon=":material/check:",
                            )
                        else:
                            st.toast(
                                f"Xóa sinh viên {id} thất bại", icon=":material/close:"
                            )

                    if haveChanges:
                        st.cache_data.clear()
                        st.rerun()

            if (data_editor["checkbox"] == True).sum() > 0:
                st.button(
                    "Xóa", use_container_width=True, on_click=handle_remove_students
                )

    if st.session_state["show_form_add"]:
        with container_form_add:
            with st.form("form_add"):
                st.markdown("#### Thêm sinh viên mới")
                id = st.text_input("Mã sinh viên")
                container_error_id = st.container()
                with container_error_id:
                    if st.session_state["submit_form"] and id.strip() == "":
                        st.caption(":red[Mã sinh viên không được để trống]")

                cols = st.columns(2)
                with cols[0]:
                    card = st.file_uploader("Thẻ sinh viên")
                    if st.session_state["submit_form"] and card is None:
                        st.caption(":red[Ảnh thẻ sinh viên không được để trống]")

                with cols[1]:
                    selfie = st.file_uploader("Chân dung")
                    if st.session_state["submit_form"] and selfie is None:
                        st.caption(":red[Ảnh chân dung không được để trống]")

                def handle_add():
                    st.session_state["submit_form"] = True
                    if id.strip() == "" or card is None or selfie is None:
                        return

                    isCreated = studentService.add(id, card, selfie)
                    if not isCreated:
                        container_error_id.caption(":red[Mã sinh viên đã tồn tại]")

                    st.cache_data.clear()
                    hide_form_add()
                    st.toast("Thêm sinh viên thành công", icon=":material/check:")
                    st.rerun()

                cols = st.columns([1, 1, 8])
                btn_submit = cols[0].form_submit_button(
                    "Thêm", use_container_width=True
                )
                cols[1].form_submit_button(
                    "Hủy", use_container_width=True, on_click=hide_form_add
                )

                if btn_submit:
                    handle_add()


st.set_page_config(
    page_title="Face Verification",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Ứng dụng xác thực khuôn mặt")
display_manage_students()
