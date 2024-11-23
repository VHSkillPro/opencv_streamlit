import streamlit as st


@st.fragment()
def display_evaluation():
    st.header("3. Đánh giá")
    st.write(
        """
        - Đánh giá mức độ **Matching Keypoint** bằng **SIFT**, **ORB** và **SuperPoint** 
        trên tiêu chí **Rotation** với các góc quay $0\degree, 10\degree, 20\degree, ..., 350\degree$ 
        dựa trên keypoint ground truth đã cung cấp sẵn trong tập dữ liệu.
        - Đối với một tập keypoint ground truth, sau khi xoay ảnh một góc quay $\theta$, các keypoint nằm 
        trong khung hình sẽ được giữ lại, các keypoint nằm ngoài khung hình sẽ bị loại bỏ.
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
        - Độ đo được sử dụng là **accuracy**, được tính bằng tỉ lệ số keypoint matching đúng trên tổng số keypoint.
        """
    )
    cols = st.columns(2, gap="large", vertical_alignment="center")
    with cols[0]:
        st.image(
            "services/keypoint_matching/euclidean-distance-formula-24tutorials.png",
            caption="Khoảng cách Euclidean",
            use_column_width=True,
        )
    with cols[1]:
        st.image(
            "services/keypoint_matching/Example-of-Hamming-Distance.png",
            caption="Khoảng cách Hamming",
            use_column_width=True,
        )

    st.write(
        """
        - Cơ chế hoạt động của **Lowe's ratio test**:
            - với mỗi keypoint trong ảnh gốc (ảnh thứ nhất), ta tìm hai keypoint gần nhất trong ảnh thứ hai 
            dựa trên khoảng cách Euclidean của các descriptor. Giả sử:
                - $D_1$ là khoảng cách giữa keypoint trong ảnh gốc và keypoint gần nhất trong ảnh thứ hai.
                - $D_2$ là khoảng cách giữa keypoint trong ảnh gốc và keypoint gần nhất thứ hai trong ảnh thứ hai.
            - Lowe's Ratio Test dựa trên tỷ lệ giữa $D_1$ và $D_2$:
                - Nếu $\\frac{D_1}{D_2} < ratio$, ta giữ lại cặp keypoint trong ảnh gốc và keypoint gần nhất trong ảnh thứ hai.
                - Ngược lại, ta loại bỏ keypoint trong ảnh gốc.
        """,
    )

    st.write(
        """
        - Cơ chế hoạt động của **crossCheck**:
            - Quá trình khớp theo chiều thuận:
                - Đối với mỗi keypoint trong ảnh gốc (ảnh thứ nhất), ta tìm keypoint gần nhất trong ảnh thứ hai 
                dựa trên khoảng cách Hamming của các descriptor.
                - Quá trình này sẽ tạo ra một danh sách $L_1$ các keypoint matching $(i, j)$, 
                trong đó $i$ là chỉ số của keypoint trong ảnh gốc và $j$ là chỉ số của keypoint gần nhất trong ảnh thứ hai.
            - Quá trình khớp theo chiều ngược lại:
                - Đối với mỗi keypoint trong ảnh thứ hai, ta tìm keypoint gần nhất trong ảnh gốc dựa trên khoảng cách Hamming của các descriptor.
                - Quá trình này sẽ tạo ra một danh sách $L_2$ các keypoint matching $(j, i)$, 
                trong đó $j$ là chỉ số của keypoint trong ảnh thứ hai và $i$ là chỉ số của keypoint gần nhất trong ảnh gốc.
            - Quá trình kiểm tra chéo:
                - Ta giữ lại các cặp keypoint matching $(i, j)$ trong $L_1$ mà sao cho $(j, i)$ cũng nằm trong $L_2$.
        """
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
        Khi **crossCheck = True**, **BFMatcher** chỉ giữ lại các cặp descriptors thỏa mãn khớp hai chiều, 
        từ đó giúp loại bỏ các điểm khớp yếu và nhiễu, 
        tăng độ chính xác của kết quả.
            - **Lowe's ratio test** hoạt động dựa trên việc tính tỷ lệ khoảng cách giữa match tốt nhất và match tốt thứ hai. 
            Đối với các descriptors của **SIFT** và **SuperPoint**, điều này giúp phát hiện những điểm khớp không đủ 
            đặc trưng bằng cách so sánh mức độ gần gũi của các matches. Trong trường hợp **ORB**, các matches 
            giữa các descriptors nhị phân thường có số lượng **khoảng cách Hamming** rất gần nhau. 
            Tức là, nhiều descriptors có thể có **khoảng cách Hamming** tương tự nhau, 
            dẫn đến tỷ lệ Lowe's không thực sự hữu ích để loại bỏ các điểm khớp yếu.
        """
    )
