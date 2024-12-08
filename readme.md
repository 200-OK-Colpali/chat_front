# Чатбот с мультимодальным поиском на Colpali и генерацией ответов спомощью LLaMA 3.2 Vision 11b

**Команда: 200 OK**
**Трек: Мультимодальные RAG модели***

---

## Описание

Чатбот реализует мультимодальный поиск и ответы с использованием современных моделей инференса. Система запускается в Docker и подразумевает использование двух машин с GPU.

---

## Перед запуском

1. **Загрузить тестовый датасет:**
   [Ссылка на диск](https://disk.yandex.com/d/5i24L_kpgaWYJA)

2. **Загрузить индекс:**
   [Ссылка на диск](https://disk.yandex.com/d/dF7eBlPtJs9GNA)

3. **Файл `.byaldi`**
   Переименовать скачанный файл `byaldi` в `.byaldi`.

---

## Требования к окружению
Гарантируется работа на следуеших версиях ядра, ПО, драйверо и библиотек и hardware

### Версии ядра, драйверов и библиотек
```
Docker version 24.0.7, build afdd53b
NVIDIA Container Runtime Hook version 1.17.2
NVIDIA Driver Version: 535.113.01
CUDA Version: 12.2
Linux COMP 6.2.0-33-generic #33~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Thu Sep  7 10:33:52 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
```

### Оборудование
```
CPU: Ryzen 1700
RAM: 16GB
GPU: RTX2070 8GB (машина 1 для Colpali)
GPU: RTX4090 24GB (машина 2 для инференса LLaMA 3.2)
```

---
# Решение запускалось на 2х машинах с gpu, так как не хватало GPU memory.

## Шаги запуска

### 0. Перед запуском

Внести изменение в `pipelines.py`:
```python
# В функции generate_oollama_response_generator указать адрес 2-й машины
url = "http://[указать тут адрес 2 машины]:8080/api/chat"
```

### 1. Запуск на машине 2
```bash
docker run -it --gpus=all -p 3000:11434 --name ollama ollama/ollama:latest
```

### 2. Запуск на машине 1
```bash
docker build -t=ragsol .
```

```bash
docker run -it --gpus=all -p 8080:8080 --name=ragsol -v=./docs:/app/docs -v ./test_dataset:/app/test_dataset -v=./.byaldi:/app/.byaldi -v ./colpali:/app/colpali ragsol
```

```bash
docker exec -it ragsol bash
```

```bash
streamlit run main.py --server.port=8080  # <- запуск фронта на 8080 порту на локал хосте
```
❗️❗️❗️^ на этом шаге при первом запуске произайдет загруска colpali модели ~ 6Гб
⌛️ Нужно подождать...

😎 **FINAL** Можно заходить в браузер на http://[адрес машины 1]:8080
