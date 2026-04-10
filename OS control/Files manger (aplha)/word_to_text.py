def ocr_from_docx(path: str) -> str:
    text = ""

    # ---- Step 1: Normal text extraction ----
    from docx import Document
    doc = Document(path)

    for para in doc.paragraphs:
        if para.text:
            text += " " + para.text

    # ---- Step 2: Extract images from DOCX ----
    # DOCX is basically a ZIP → images stored inside /word/media/
    import zipfile
    from PIL import Image
    import io

    with zipfile.ZipFile(path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.startswith("word/media/"):
                image_data = zip_ref.read(file)

                image = Image.open(io.BytesIO(image_data))

                # ---- Step 3: OCR on image ----
                import pytesseract
                text += " " + pytesseract.image_to_string(image)

    return text


if __name__ == "__main__" :
    import main
    ## test code
    file_path = "test.docx"
    sub_c, score = main.predict_subject(file_path)
    model = main.load_code_name_mapping("subjects_Final.json")
    sub_n = model.get(sub_c,"Unknown subject")

    print(f"\nsubject code is : {sub_c}\nsubject name is : {sub_n}\nconfidence score : {score}")

## text file tested
## image file left (skip)