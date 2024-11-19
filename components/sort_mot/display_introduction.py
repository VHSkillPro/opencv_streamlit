import streamlit as st


@st.fragment()
def display_introduction():
    st.header("1. Giới thiệu")

    cols = st.columns([3, 1])
    cols[1].image(
        "services/sort_mot/benchmark-performance.jpg",
        use_column_width=True,
        caption="""
        Đánh giá hiệu suất của SORT so với các thuật toán khác trong MOTChallenge 2015. (Nguồn: Simple Online and Realtime Tracking).
        """,
    )

    with cols[0]:
        st.write(
            """
            - **SORT** là một thuật toán theo dõi nhiều đối tượng **(Multi-Object Tracking - MOT)** đơn giản, nhanh, và hiệu quả, 
            được thiết kế cho việc theo dõi các đối tượng trong thời gian thực, với khả năng xử lý video trực tuyến.
            - **SORT** được giới thiệu vào năm 2016 trong bài báo [Simple Online and Realtime Tracking](https://arxiv.org/abs/1602.00763) 
            của Alex Bewley, Zongyuan Ge, Lionel Ott, Fabio Ramos, và Ben Upcroft.
            - Biểu đồ bên phải thể hiện hiệu suất của **SORT** so với các thuật toán khác trong **MOTChallenge 2015**. Mỗi điểm đánh dấu cho biết độ chính xác (đo bởi MOTA) 
            và tốc độ (được đo bởi FPS hay Hz) của một thuật toán theo dõi. Từ biểu đồ, ta có thể thấy rằng:
                - **SORT** đạt được tốc độ cao trong khi độ chính xác vẫn được đảm bảo so với các thuật toán khác.
                - Trong khi đó, các thuật toán khác có sự đánh đổi giữa tốc độ và độ chính xác.
            - Dù **SORT** đạt được hiệu suất tốt trong việc theo dõi đối tượng, nó vẫn có một số hạn chế như:
                - Không thể duy trì theo dõi đối tượng khi đối tượng bị che khuất hoặc thoát khỏi khung hình và quay trở lại.
                - Không thể phân biệt giữa các đối tượng có hình dạng, màu sắc, hoặc kích thước tương tự nhau.
                - Phụ thuộc nhiều vào mô hình detector để xác định vị trí của đối tượng.
                - Không thể xử lý được các trường hợp đối tượng chuyển động nhanh hoặc chuyển động không tuyến tính.
            """
        )
