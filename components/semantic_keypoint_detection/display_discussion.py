import streamlit as st


@st.fragment()
def display_discussion():
    st.header("5. Thảo luận")
    st.write(
        """
        - Đối với $5$ loại hình **checkboard**, **cube**, **multiple polygon**, **polygon** và **star**:
            - Do **ORB** hoạt động tốt trong việc nhận diện các góc cạnh rõ ràng, 
            điều này rất phổ biến trong $5$ loại hình đã đề cập ở trên 
            (ví dụ: các ô vuông với điểm góc rõ ràng và đa giác với các cạnh sắc nét).
            - **SIFT** còn bị ảnh hưởng bởi các nhiễu trong background, hình vuông, 
            tam giác ở $5$ loại hình trên (như trong hình 2.1.3.1).
        - Đổi với loại hình **stripes** và **lines**:
            - **ORB** thường phát hiện các keypoint dọc theo các cạnh 
            (ví dụ như trong hình 2.2.3.3, 2.2.3.4 và 2.2.3.8),
            nhưng trong tập ground truth thì các có rất ít điểm keypoint nằm trên các đường thẳng này,
            vì thế **ORB** cho precision thấp trong loại hình này.
        """
    )
