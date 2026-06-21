import pymupdf

doc = pymupdf.open("D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf")
pag1 = doc[0]
text = pag1.get_text()
print(text)

for page_num, page in enumerate(doc, start=1):

    data = page.get_text("dict")

    chapter_name = []   # ✅ move OUTSIDE block loop

    for block in data["blocks"]:

        if "lines" in block:

            for line in block["lines"]:

                full_text = ""
                max_font = 0

                for span in line["spans"]:
                    full_text += span["text"]
                    max_font = max(max_font, span["size"])

                if max_font > 20:
                    print("Text:", full_text, "| font size:", max_font)
                    chapter_name.append(full_text)

    print(f"Page {page_num} chapters:", chapter_name)