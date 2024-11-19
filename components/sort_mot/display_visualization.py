import streamlit as st


@st.fragment()
def display_visualization():
    st.header("3. Minh hoạ thuật toán")
    st.write(
        "- Dưới đây là một số video minh hoạ kết quả phát hiện người đi bộ với mô hình YOLO và theo dõi bằng thuật toán SORT:"
    )
    cols = st.columns(2)

    with cols[0]:
        st.video("services/sort_mot/YOLO people detection + SORT tracking.mp4")
        st.write(
            """
            - Trong video, từ giây thứ 0:05, ta thấy rằng người có id $1$ bị che khuất bởi cột đèn và tới giây thứ 0:14, 
            người đó mới xuất hiện trở lại khung hình. Tuy nhiên, id của người này đã bị thay đổi thành $14$.
            """
        )

    with cols[1]:
        st.video("services/sort_mot/sort_demo_2.mp4")
        st.write(
            """
            - Tại giây thứ 0:07, người có id $2$ sau một giây biến mất khỏi khung hình và xuất hiện trở lại tại giây thứ 0:08 thì đã bị ReId thành $81$.
            """
        )

    st.write(
        """
        - Từ hai video trên, ta thấy rõ nhược điểm của thuật toán **SORT** là không thể duy trì id của đối tượng 
        khi đối tượng biến mất khỏi khung hình một khoảng thời gian.
        """
    )
