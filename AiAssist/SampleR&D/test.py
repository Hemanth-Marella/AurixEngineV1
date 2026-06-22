import pymupdf

doc = pymupdf.open("D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf")
pag1 = doc[0]
text = pag1.get_text()
print(text)

for page_num, page in enumerate(doc, start=1):

    data = page.get_text("dict")

    chapter_name = []   # move OUTSIDE block loop

    for block in data["blocks"]:

        if "lines" in block:

            for line in block["lines"]:

                full_text = ""
                max_font = 0

                for span in line["spans"]:
                    text = span['text']
                    font_size = span["size"]
                    font_name = span["font"]

                    print(
                        "text " , text,
                        "font_size " , font_size,
                        "font_name " , font_name
                    )

    # print(f"Page {page_num} chapters:", chapter_name)