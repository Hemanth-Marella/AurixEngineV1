from langchain_text_splitters import RecursiveCharacterTextSplitter
# from .LoadPdf import PdfToDocument   # if run this file uncomment the import

file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf"

def embedding_chunking(documents,chunk_size,chunk_overlap):

    # chunk_list = []

    documents_chunking = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
        separators=["\n\n","\n"," ",""]
    )

    chunk_pages = documents_chunking.split_documents(documents)

    return chunk_pages

# load_documents = PdfToDocument(file_path).load_pdf_to_documents()
# chuns = embedding_chunking(load_documents,400,50)
# print(type(chuns))
# print(len(chuns))