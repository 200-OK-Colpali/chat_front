import base64
import torch
import os
from byaldi import RAGMultiModalModel
from os import listdir
from os.path import isfile, join


RAG = RAGMultiModalModel.from_pretrained("./colpali", verbose=1)


mypath = "./test_dataset"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

first = onlyfiles[0]
first_path = mypath + "/" + first
print(f"adding: {first_path}")
RAG.index(
    input_path=mypath + "/" + first,
    index_name="global_index",
    store_collection_with_index=False,  # set this to false if you don't want to store the base64 representation
    overwrite=False,
)

for filename in onlyfiles[1:]:
    curr_path = mypath + "/" + filename
    print(f"adding: {curr_path}")
    RAG.add_to_index(input_item=curr_path, store_collection_with_index=False)
