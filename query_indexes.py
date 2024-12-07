import base64
import torch

print(torch.cuda.is_available())  # Должно вернуть True
print(torch.version.cuda)        # Показывает версию CUDA

import os 
from byaldi import RAGMultiModalModel


# os.environ["HF_token"] = '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' # to download the ColPali model
RAG_with_index = RAGMultiModalModel.from_index(
    index_path="./global_index",  # Путь к папке с индексом
    verbose=1,
    device="cuda"  # Укажите устройство, например "cuda" или "cpu"
)


# results = RAG_with_index.search("Расскажи про EBITDA ", k=10)
print(RAG_with_index.get_doc_ids_to_file_names())
# print(results)
# # RAG.model.model.save_pretrained('./colpali')
# # RAG.model.processor.save_pretrained("colpali")


# query = ["расскажи ченить"]
# results = RAG_with_index.search(query, k=10)

