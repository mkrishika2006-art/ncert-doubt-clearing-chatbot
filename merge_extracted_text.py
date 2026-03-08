from pypdf import PdfReader

pdf_files = [
    "Class 9 Mathematics.pdf",
    "Class 10 Mathematics.pdf",
    "Class 10 NCERT Science.pdf",
    "class9_ncert_science_topics.pdf"
]

with open("syllabus.txt", "a", encoding="utf-8") as outfile:

    for pdf in pdf_files:

        outfile.write(f"\n\n===== {pdf} =====\n\n")

        reader = PdfReader(pdf)

        for page in reader.pages:
            text = page.extract_text()

            if text:
                outfile.write(text + "\n")

print("PDF text extraction complete")