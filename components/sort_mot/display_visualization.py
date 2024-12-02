import streamlit as st


@st.fragment()
def display_visualization():
    st.header("3. Minh hoạ thuật toán")
    st.write(
        "- Dưới đây là một số video minh hoạ kết quả phát hiện người đi bộ với mô hình YOLO và theo dõi bằng thuật toán SORT:"
    )
    cols = st.columns([3, 4])

    with cols[0]:
        st.video("services/sort_mot/YOLO people detection + SORT tracking.mp4")
        st.write(
            """
            - Trong video, từ giây thứ 0:05, ta thấy rằng người có id $1$ bị che khuất bởi cột đèn và tới giây thứ 0:14, 
            người đó mới xuất hiện trở lại khung hình. Tuy nhiên, id của người này đã bị thay đổi thành $14$. Điều này là do thuật toán **SORT**
            không có cơ chế duy trì id trong trường hợp đối tượng biến mất khỏi khung hình một khoảng thời gian,
            sau đó xuất hiện trở lại. Khi người có id $1$ biến mất quá thời gian quy định, **SORT** sẽ xoá track mang id $1$.
            Sau một khoảng thời gian, khi người đó xuất hiện trở lại, **SORT** không nhận ra đây là người đã từng xuất hiện và tạo một track mới với id mới.
            """
        )

    with cols[1]:
        st.video("services/sort_mot/sort_demo_2.mp4")
        st.write(
            """
            - Tại giây thứ 0:07, người có id $2$ sau một giây biến mất khỏi khung hình 
            và xuất hiện trở lại tại giây thứ 0:08 thì đã bị ReId thành $81$. 
            Giống như trường hợp bên trái, khi đối tượng mang id $2$ biến mất quá thời gian quy định, 
            thuật toán **SORT** sẽ xoá track mang id $2$. Sau khi đối tượng đó xuất hiện trở lại,
            **SORT** không nhận ra đây là đối tượng đã từng xuất hiện và tạo một track mới với id mới. 
            """
        )

    st.write(
        """
        - Từ hai video trên, ta thấy rõ nhược điểm của thuật toán **SORT** là không thể duy trì id của đối tượng 
        khi đối tượng biến mất khỏi khung hình một khoảng thời gian.
        """
    )
