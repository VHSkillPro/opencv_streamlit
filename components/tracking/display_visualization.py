import streamlit as st


@st.fragment()
def display_visualization():
    st.header("3. Ví dụ minh hoạ")
    st.write(
        """
        - Dưới đây là một ví dụ minh hoạ về việc sử dụng **KCF** để theo dõi một chiếc oto màu đen đang đi trên đường. 
        Trong video, khung màu xanh dương đại diện cho vùng mà **KCF** đang theo dõi.
        Ta thấy trong video có rất nhiều oto giống với oto đang được theo dõi, nhưng **KCF** chỉ theo dõi oto màu đen được chỉ định.
        - Điều này cho thấy rằng **KCF** hoạt động tốt khi gặp trình trạng **background clutters**.
        """
    )

    st.columns([1, 3, 1])[1].video("services/tracking/background-cluster.mp4")

    st.write(
        """
        - Dưới đây là một ví dụ minh hoạ về việc sử dụng **KCF** để theo dõi người đi bộ.
        - Trong video, **KCF** theo dõi một người đi bộ mặc áo trắng cho tới khi người đó bị che khuất bởi một người khác đi ngược chiều. 
        Điều thầy cho thấy rằng **KCF** không hoạt động tốt khi gặp trình trạng **occlusion**.
        """
    )
    st.columns([1, 3, 1])[1].image(
        "https://d130b8xaedzatc.cloudfront.net/2024/02/kcf-1-4749e0d684e34f9284fe1ec0e798f7de.webp",
        use_column_width=True,
        caption="Minh hoạ việc sử dụng KCF để theo dõi người đi bộ",
    )

    st.write(
        """
        - Trong video dưới đây, **KCF** theo dõi một trực thăng điều khiển đang cất cánh với tốc độ cao. 
        Trong video, khung màu xanh dương đại diện cho vùng mà **KCF** đang theo dõi. 
        Ta thấy răng, khi trực thăng cất cánh và bay nhanh ở giây thứ 0:08 thì **KCF** không thể theo dõi được trực thăng nữa.
        - Điều này cho thấy rằng **KCF** không hoạt động tốt khi gặp trình trạng **fast motion**.
        """
    )
    st.columns([1, 3, 1])[1].video("services/tracking/fast-motion.mp4")

    st.write(
        """
        - Dựa vào thông số FPS của các video trên, ta thấy rằng **KCF** hoạt động nhanh, chỉ sau thuật toán *MOSSE*.
        """
    )
