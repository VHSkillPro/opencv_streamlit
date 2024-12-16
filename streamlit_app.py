import streamlit as st

st.navigation(
    [
        st.Page(
            "_pages/grabcut.py",
            title="1. Ứng dụng tách nền bằng thuật toán GrabCut",
        ),
        st.Page(
            "_pages/watershed.py",
            title="2. Phân đoạn ký tự bằng Watershed Segmentation",
        ),
        st.Page(
            "_pages/haar_knn.py",
            title="3. Phát hiện khuôn mặt với Haar Features và KNN",
        ),
        st.Page(
            "_pages/face_verification.py",
            title="4. Ứng dụng xác nhận khuôn mặt",
        ),
        st.Page(
            "_pages/keypoint_detection.py",
            title="5. Phát hiện Keypoint trên Synthetic Shapes Dataset",
        ),
        st.Page(
            "_pages/keypoint_matching.py",
            title="6. So khớp Keypoint dựa trên tiêu chí Rotation",
        ),
        st.Page(
            "_pages/instance_search.py",
            title="7. Tìm kiếm ảnh chứa đối tượng truy vấn",
        ),
        st.Page(
            "_pages/tracking.py",
            title="8. Theo dõi đối tượng (SOT) bằng thuật toán KCF",
        ),
        st.Page(
            "_pages/sort_mot.py",
            title="9. Thuật toán SORT (Simple Online Realtime Tracking)",
        ),
        st.Page(
            "_pages/handwriting_letter_recognition.py",
            title="10. Nhận dạng chữ viết tay",
        ),
        st.Page(
            "_pages/processing_image.py",
            title="11. Ứng dụng xử lý ảnh"
        )
    ]
).run()
