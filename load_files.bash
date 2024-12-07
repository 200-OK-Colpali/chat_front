#!/bin/bash

# Define the folder and download URLs
TEST_DATASET_FOLDER="test_dataset"
BYALDI_FOLDER=".byaldi"
COLPALI_FOLDER="colpali"

TEST_DATASET_URL="https://downloader.disk.yandex.com/disk/376fe26a52bd57cf6691bd46e9e7477a9cc374a75d3069f3c26e6891bc454558/6754e3b8/GORH-WLDFTp3elLhwAv8rS0MSFkozxDSyC_AMg9bs4GdFmsfD7FuWhS3sYuXZXSV9PHIbEa8aqvB6Nn4GUHf2Q%3D%3D?uid=0&filename=test_dataset.zip&disposition=attachment&hash=g2n4PBn4FKjZNRCfqiTwuDT6o0pqNKRH8KzjR%2BRzGEv1qWfBHIsIrYkb1d3PUeT8q/J6bpmRyOJonT3VoXnDag%3D%3D&limit=0&content_type=application%2Fzip&owner_uid=1489006053&fsize=450463412&hid=765b8b33a987679e69b943699ba7af9c&media_type=compressed&tknv=v2"
BYALDI_URL="https://downloader.disk.yandex.com/disk/323b8660bccb0402012beee2db90f31c7bf514489446ae9f740a81546d370c93/6754e465/GORH-WLDFTp3elLhwAv8rUUQR1lMuVpVXFVRqQRGMLWhzJZgb9xroIaqRtLn7ysRThTn00Bf6qc7pc9varfs0g%3D%3D?uid=0&filename=byaldi.zip&disposition=attachment&hash=p%2BBbSxQjFZT2fzkUP7uhizzVpWdzLY%2BruFhj90F%2Bhhii9PxziYwu0JMxb%2BeFi940q/J6bpmRyOJonT3VoXnDag%3D%3D&limit=0&content_type=application%2Fzip&owner_uid=1489006053&fsize=433829224&hid=fb080d1b268c767fdc145dcf07a26d5b&media_type=compressed&tknv=v2"
COLPALI_URL="https://downloader.disk.yandex.com/disk/a4b4b5c3ec8b20404416780e82392970392e7f4768ea73f646d343c19751c3dc/6754e781/GORH-WLDFTp3elLhwAv8rck0PBLxvriGqWJpmKWSWVqoTfks-kTsjyDRkMrqjf5h1h5RZhA6C2WccTlnVieBUg%3D%3D?uid=0&filename=colpali.zip&disposition=attachment&hash=flT1WEGKgix9VmXfJxz9FyTacEXGQKeiElJcQSj0gHVB4zPHL8HRG9YTHo%2BnmNZgq/J6bpmRyOJonT3VoXnDag%3D%3D&limit=0&content_type=application%2Fzip&owner_uid=1489006053&fsize=67253625&hid=9e176d1ec03840552e5763584d302d7e&media_type=compressed&tknv=v2"

# Download test_dataset.zip if test_dataset folder does not exist
if [ ! -d "$TEST_DATASET_FOLDER" ]; then
    echo "Folder '$TEST_DATASET_FOLDER' does not exist. Downloading test_dataset.zip..."
    wget -O "test_dataset.zip" "$TEST_DATASET_URL"
    echo "Download completed. Extracting test_dataset.zip..."
    unzip -o "test_dataset.zip"
    echo "Extraction completed. Deleting the zip file..."
    rm -f "test_dataset.zip"
else
    echo "Folder '$TEST_DATASET_FOLDER' already exists. Skipping download."
fi

# Download byaldi.zip if .byaldi folder does not exist
if [ ! -d "$BYALDI_FOLDER" ]; then
    echo "Folder '$BYALDI_FOLDER' does not exist. Downloading byaldi.zip..."
    wget -O "byaldi.zip" "$BYALDI_URL"
    echo "Download completed. Extracting byaldi.zip..."
    unzip -o "byaldi.zip"
    mv "byaldi" ".byaldi"
    echo "Extraction completed. Deleting the zip file..."
    rm -f "byaldi.zip"
else
    echo "Folder '$BYALDI_FOLDER' already exists. Skipping download."
fi


# Download COLPALI.zip if .COLPALI folder does not exist
if [ ! -d "$COLPALI_FOLDER" ]; then
    echo "Folder '$COLPALI_FOLDER' does not exist. Downloading colpali.zip..."
    wget -O "colpali.zip" "$COLPALI_URL"
    echo "Download completed. Extracting colpali.zip..."
    unzip -o "colpali.zip"
    echo "Extraction completed. Deleting the zip file..."
    rm -f "colpali.zip"
else
    echo "Folder '$COLPALI_FOLDER' already exists. Skipping download."
fi
