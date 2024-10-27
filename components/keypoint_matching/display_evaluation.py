import streamlit as st


@st.fragment()
def display_evaluation():
    st.header("3. Đánh giá")
    st.write(
        """
        - Đánh giá mức độ **Matching Keypoint** bằng **SIFT**, **ORB** và **SuperPoint** 
        trên tiêu chí **Rotation** với các góc quay $0\degree, 10\degree, 20\degree, ..., 350\degree$.
        - Đối với **SIFT** và **SuperPoint**:
            - Sử dụng **Brute-Force Matching** để tìm ra các keypoint matching 
        với tham số:
                - normType = **cv2.NORM_L2** (sử dụng **Euclidean** để tính khoảng cách giữa hai **description**).
            - Sau đó sử dụng **Lowe's ratio test** với $ratio = 0.75$ để giảm thiểu các keypoint matching yếu.
        - Đối với **ORB**, sử dụng **Brute-Force Matching** để tìm ra các keypoint matching 
        với tham số:
            - normType = **cv2.NORM_HAMMING** (sử dụng **Hamming** để tính khoảng cách giữa hai **description**).
            - crossCheck = **True** (chỉ lấy các keypoint matching $(i, j)$ mà sao cho description thứ $i$ 
            trong tập hợp $A$ khớp với description thứ $j$ trong tập hợp $B$ và ngược lại).
        - Độ đo được sử dụng là **accuracy**, được tính bằng tỉ lệ số keypoint matching trên tổng số keypoint.
        """
    )
    cols = st.columns(2, gap="large", vertical_alignment="center")
    with cols[0]:
        st.image(
            "https://www.24tutorials.com/wp-content/uploads/2018/09/euclidean-distance-formula-24tutorials.png",
            caption="Khoảng cách Euclidean",
            use_column_width=True,
        )
    with cols[1]:
        st.image(
            "https://www.researchgate.net/publication/264978395/figure/fig1/AS:295895569584128@1447558409105/Example-of-Hamming-Distance.png",
            caption="Khoảng cách Hamming",
            use_column_width=True,
        )
    st.write(
        """
        - Giải thích cho việc chọn tham số khác nhau giữa **SIFT** và **ORB**:
            - **SIFT descriptors** và **SuperPoint descriptors** là vector liên tục trong không gian **Euclidean**, 
        vì vậy **cv2.NORM_L2 (Euclidean)** cho phép so khớp chính xác và phản ánh 
        đúng khoảng cách giữa các descriptors. Đặc tính của (**SIFT** hoặc **SuperPoint**) và **Euclidean** 
        đã cung cấp độ chính xác cao trong việc keypoint matching nên crossCheck không bắt buộc 
        và thậm chí còn làm giảm hiệu quả.
            - **Khoảng cách Hamming** phù hợp với descriptors là dạng dữ liệu nhị phân của **ORB**, 
        cho phép tính toán nhanh hơn và hiệu quả hơn khi so khớp các vectors nhị phân. 
        Vì các vectors nhị phân có thể dễ dàng trùng khớp một phần với nhiều vectors nhị phân khác nhau, 
        việc chỉ sử dụng một phép so khớp một chiều có thể dẫn đến nhiều matches nhiễu.
        Khi **crossCheck = True**, **BFMatcher** chỉ giữ lại các cặp descriptors thỏa mãn khớp hai chiều. 
        Điều này có nghĩa là nếu descriptor $A$ trong ảnh $1$ khớp với descriptor $B$ trong ảnh $2$, 
        thì descriptor $B$ cũng phải khớp lại với descriptor $A$, từ đó giúp loại bỏ các điểm khớp yếu và nhiễu, 
        tăng độ chính xác của kết quả.
            - **Lowe's ratio test** hoạt động dựa trên việc tính tỷ lệ khoảng cách giữa match tốt nhất và match tốt thứ hai. 
            Đối với các descriptors của **SIFT** và **SuperPoint**, điều này giúp phát hiện những điểm khớp không đủ 
            đặc trưng bằng cách so sánh mức độ gần gũi của các matches. Trong trường hợp **ORB**, các matches 
            giữa các descriptors nhị phân thường có số lượng **khoảng cách Hamming** rất gần nhau. 
            Tức là, nhiều descriptors có thể có **khoảng cách Hamming** tương tự nhau, 
            dẫn đến tỷ lệ Lowe's không thực sự hữu ích để loại bỏ các điểm khớp yếu.
        """
    )
