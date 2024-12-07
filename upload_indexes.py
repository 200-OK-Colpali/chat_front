import base64
import torch

print(torch.cuda.is_available())  # Должно вернуть True
print(torch.version.cuda)        # Показывает версию CUDA

import os 
from byaldi import RAGMultiModalModel


# os.environ["HF_token"] = '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' # to download the ColPali model
RAG = RAGMultiModalModel.from_pretrained("./colpali", verbose=1)

# RAG.model.model.save_pretrained('./colpali')
# RAG.model.processor.save_pretrained("colpali")



RAG.index(
    input_path="./docs/attention_is_all_you_need.pdf",
    index_name="global_index",
    store_collection_with_index=False, # set this to false if you don't want to store the base64 representation
    overwrite=False
)


RAG.add_to_index(
    input_item="./docs/ММК2024.pdf",
    store_collection_with_index=False
)
