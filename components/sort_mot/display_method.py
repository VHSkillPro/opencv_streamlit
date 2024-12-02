import streamlit as st


@st.fragment()
def display_method():
    st.header("2. Phương pháp")
    st.write(
        """
        - **SORT** là một thuật toán theo dõi nhiều đối tượng **(Multi-Object Tracking - MOT)** dựa trên **tracking-by-detection**.
        Đặc điểm của lớp các thuật toán **tracking-by-detection** là sử dụng mô hình detector để xác định vị trí của đối tượng, 
        sau đó tìm cách liên kết các vị trí của đối tượng qua các frame liên tiếp để theo dõi đối tượng. 
        - Vì vậy, **SORT** cần một mô hình detector để xác định vị trí của đối tượng trong mỗi frame, 
        có thể sử dụng các mô hình detector như **YOLO**, **Faster R-CNN**, **SSD**, **RetinaNet**, **EfficientDet**, ....
        Trong bài báo gốc, tác giả sử dụng **Faster Region CNN (FrCnn)** với backbone là **VGG 16** để xác định vị trí của các đối tượng.
        """
    )

    st.columns([1, 8, 1])[1].image(
        "services/sort_mot/overview-SORT.png",
        use_column_width=True,
        caption="Hình ảnh minh họa quá trình hoạt động của SORT",
    )

    st.write(
        """
        - **SORT** sử dụng **Kalman Filter** và thuật toán **Hungarian** để thực hiện quá trình theo dõi đối tượng.
        Quá trình hoạt động của **SORT** bao gồm bốn bước sau:
            - Bước 1: **Phát hiện** các đối tượng trong frame hiện tại bằng mô hình detector.
            - Bước 2: **Dự đoán** vị trí các đối tượng trong frame hiện tại dựa trên trạng thái của các đối tượng trong frame trước và **Kalman Filter**.
            - Bước 3: **Ghép nối** các vị trí phát hiện được ở **bước 1** với các vị trí dự đoán ở **bước 2** bằng thuật toán **Hungarian**.
            - Bước 4: **Cập nhật** trạng thái của các đối tượng dựa trên kết quả ghép nối ở **bước 3**.
        """
    )

    st.subheader("2.1. Dự đoán vị trí của đối tượng bằng Kalman Filter")
    st.write(
        """
        - **SORT** xấp xỉ sự dịch chuyển giữa các khung hình của mỗi đối tượng bằng mô hình vận tốc không đổi tuyến tính, 
        độc lập với các đối tượng khác và độc lập với chuyển động của máy ảnh. 
        - Trạng thái của mỗi đối tượng được mô tả bằng một vector $x = [u, v, s, r, \dot{u}, \dot{v}, \dot{s}]^T$, trong đó:
            - $(u, v)$ là tọa độ của trung tâm của bounding box của đối tượng.
            - $s$ là tỷ lệ giữa chiều rộng và chiều cao của bounding box của đối tượng.
            - $r$ là tỷ lệ giữa chiều rộng và chiều cao của bounding box của đối tượng.
            - $(\dot{u}, \dot{v})$ là vận tốc của trung tâm của bounding box của đối tượng.
            - $\dot{s}$ là vận tốc của tỷ lệ giữa chiều rộng và chiều cao của bounding box của đối tượng.
        - **SORT** sẽ sử dụng [**Kalman Filter**](https://www.unitedthc.com/DSP/Kalman1960.pdf) để dự đoán vị trí tiếp theo của mỗi đối tượng đã được theo dõi dựa trên trạng thái hiện tại của chúng.
        """
    )

    st.subheader(
        "2.2. Ghép nối các vị trí phát hiện với các vị trí dự đoán bằng thuật toán Hungarian"
    )
    st.write(
        """
        - Để ghép nối các vị trí phát hiện được với các vị trí dự đoán, một ma trận chi phí ghép nối $C$ được xây dựng 
        với phần tử ở hàng $i$, cột $j$ là chi phí khi ghép nối vị trí phát hiện thứ $i$ với vị trí dự đoán thứ $j$. 
        Chi phí này thường được tính bằng IoU giữa hai bounding box.
        - Sau đó, **SORT** sử dụng thuật toán [**Hungarian**](https://web.eecs.umich.edu/~pettie/matching/Kuhn-hungarian-assignment.pdf) 
        trên ma trận $C$ để tìm cách ghép nối các vị trí phát hiện với các vị trí dự đoán sao cho tổng chi phí ghép nối là lớn nhất có thể.
        """
    )

    st.subheader("2.3. Cập nhật trạng thái của các đối tượng")
    st.write(
        """
        - Sau khi đã ghép nối, **SORT** cập nhật trạng thái của các đối tượng đã được ghép nối.
        - Đối với các đối tượng (được phát hiện từ mô hình detector) không được ghép nối, **SORT** sẽ gán cho chúng một ID mới.
        - Đối với các đối tượng dự đoán không được ghép nối trong $T_{Lost}$ khung hình liên tiếp, **SORT** sẽ xóa chúng khỏi danh sách theo dõi.
        - Trong bài báo gốc, tác giả sử dụng $T_{Lost} = 1$ để đánh giá hiệu suất của **SORT**.
        """
    )
