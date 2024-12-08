# Чатбот с colpali мультимодальным поиском и генерацией ответа с помощью llama 3.2 vision 11b 
Команда 200 OK

## Запуск в Docker

Запуск

перед запуском загрузить тестовый датасет:
https://disk.yandex.com/d/5i24L_kpgaWYJA

индекс:
https://disk.yandex.com/d/dF7eBlPtJs9GNA

byaldi переименовать в .byaldi

Гарантируется работа на следуеших версиях ядра, ПО, драйверо и библиотек и hardware

### Drivers & libs
```
Docker version 24.0.7, build afdd53b
NVIDIA Container Runtime Hook version 1.17.2
NVIDIA Driver Version: 535.113.01
CUDA Version: 12.2  
Linux COMP 6.2.0-33-generic #33~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Sep  7 10:33:52 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
```

### Hardware
```
Ryzen 1700
Ram: 16GB
GPU: RTX2070 8gb -> Colpali машина 1
GPU: RTX4090 24gb -> инференс LlaMA3.2 машина 2
```
Решение запускалось на 2х машинах с gpu, так как не хватало GPU memory.
### ШАГИ

0 шаг!!!
```python
# зайти в файл pipelines.py изменить  в функции  generate_oollama_response_generator

url = "http://[указать тут адрес 2 машины]:8080/api/chat" # <--- Указать тут адрес 2 машины

```

```

На машине 2
1) docker run -it --gpus=all -p 3000:11434 --name ollama ollama/ollama:latest 

На машине 1
2) docker build -t=ragsol .
2) docker run -it --gpus=all -p 8080:8080 --name=ragsol -v=./docs:/app/docs -v ./test_dataset:/app/test_dataset -v=./.byaldi:/app/.byaldi -v ./colpali:/app/colpali ragsol
3) docker exec -it ragsol bash
4) streamlit run main.py --server.port=8080  # <- запуск фронта на 8080 порту на локал косте
   ^ на этом шаге при первом запуске произайдет загруска colpali модели ~ 6Гб
Нужно подождать... 

5) Можно заходить в браузер на http://[адрес машины 1]:8080 

```

