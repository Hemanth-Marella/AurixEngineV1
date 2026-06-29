from langchain_text_splitters import RecursiveCharacterTextSplitter
# from .LoadPdf import PdfToDocument   # if run this file uncomment the import

file_path = "D:\projects\personalProject\Education\EducationChatbotServer\data\9thclass\Biology\9_biology1.pdf"

def embedding_chunking(documents,chunk_size,chunk_overlap):

    documents_chunking = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        length_function = len,
        separators=["\n\n","\n"," ",""]
    )

    chunk_pages = documents_chunking.split_documents(documents)

    return chunk_pages

# load_documents = embedding_chunking(file_path).load_pdf_to_documents()
# chuns = embedding_chunking(load_documents,500,80)
# print(type(chuns))
# print(len(chuns))


# Don't choose a chunk size based on the embedding model's dimensions. Choose it based on retrieval quality.