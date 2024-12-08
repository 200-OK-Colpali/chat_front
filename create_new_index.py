import base64
import torch
import os
from byaldi import RAGMultiModalModel
from os import listdir
from os.path import isfile, join


RAG = RAGMultiModalModel.from_pretrained("./colpali", verbose=1)


first_path = './test_pdf.pdf'
RAG.index(
    input_path=first_path,
    index_name="test_index_name",
    store_collection_with_index=False,  # set this to false if you don't want to store the base64 representation
    overwrite=False,
)
