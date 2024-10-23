accent_tables = str.maketrans(
    "ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴáàảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ",
    "A" * 17
    + "D"
    + "E" * 11
    + "I" * 5
    + "O" * 17
    + "U" * 11
    + "Y" * 5
    + "a" * 17
    + "d"
    + "e" * 11
    + "i" * 5
    + "o" * 17
    + "u" * 11
    + "y" * 5,
    chr(774)
    + chr(770)
    + chr(795)
    + chr(769)
    + chr(768)
    + chr(777)
    + chr(771)
    + chr(803),
)


def remove_vietnamese_accent(txt: str) -> str:
    return txt.translate(accent_tables)
