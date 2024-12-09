import streamlit as st


@st.fragment()
def display_method():
    st.header("2. Phương pháp")
    st.write(
        """
        - Mô hình **CNN** được sử dụng để nhận dạng chữ số viết tay trong bài toán này với kiến trúc như sau:
        """
    )
    st.image(
        "services\handwriting_letter_recognition\cnn_flow.png", use_container_width=True
    )
    st.write(
        """
        - Trong đó:
            - **Convolutional Layer**: Dùng để trích xuất các đặc trưng của ảnh.
            - **Max Pooling Layer**: Giảm kích thuớc của ảnh nhằm giảm chi phí tính toán.
            - **Flatten Layer**: Chuyển ảnh từ ma trận 2 chiều sang vector 1 chiều.
            - **Softmax Layer**: Dùng để phân loại ảnh vào các lớp.
        - Mô hình được huấn luyện trên tập dữ liệu **MNIST** được phân chia như sau:
            - **Training set**: $50,000$ ảnh đầu tiên trong training set ban đầu.
            - **Validation set**: $10,000$ ảnh còn lại trong training set ban đầu.
            - **Test set**: $10,000$ ảnh của test set ban đầu.
        - Hàm mất mát được sử dụng là **Categorical Cross-Entropy**.
        - Thuật toán tối ưu được sử dụng là **Adam** với **learning rate** = $0.001$.
        - Số epochs huấn luyện là $20$.
        """
    )
