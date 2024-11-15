import streamlit as st


@st.fragment()
def display_methods():
    st.header("2. Phương pháp")
    st.image(
        "services/image_search_engine/flow.jpg",
        use_column_width=True,
        caption="Hình ảnh minh họa quy trình",
    )
    st.write(
        """
        - Các bước chính trong hệ thống bao gồm:
            - Bước $1$: Biến đổi ảnh truy vấn và ảnh cơ sở thành ảnh xám
            - Bước $2$: Sử dụng BFMatcher để tìm các matching giữa ảnh truy vấn và ảnh cơ sở 
            theo $4$ góc xoay khác nhau ($0\degree$, $90\degree$, $180\degree$, $270\degree$)
            - Bước $3$: Đếm số lượng matching và lấy độ tương đồng lớn nhất giữa ảnh truy vấn 
            và ảnh cơ sở dựa trên số lượng matching. 
        - Dựa vào độ tương đồng của ảnh truy vấn và ảnh trong cơ sở dữ liệu, 
        hệ thống sẽ trả về $k$ ảnh có độ tương đồng lớn nhất với ảnh truy vấn.
        """
    )
