#!/bin/bash

# Define the folder and download URLs
TEST_DATASET_FOLDER="test_dataset"
BYALDI_FOLDER=".byaldi"

TEST_DATASET_URL="https://downloader.disk.yandex.com/disk/376fe26a52bd57cf6691bd46e9e7477a9cc374a75d3069f3c26e6891bc454558/6754e3b8/GORH-WLDFTp3elLhwAv8rS0MSFkozxDSyC_AMg9bs4GdFmsfD7FuWhS3sYuXZXSV9PHIbEa8aqvB6Nn4GUHf2Q%3D%3D?uid=0&filename=test_dataset.zip&disposition=attachment&hash=g2n4PBn4FKjZNRCfqiTwuDT6o0pqNKRH8KzjR%2BRzGEv1qWfBHIsIrYkb1d3PUeT8q/J6bpmRyOJonT3VoXnDag%3D%3D&limit=0&content_type=application%2Fzip&owner_uid=1489006053&fsize=450463412&hid=765b8b33a987679e69b943699ba7af9c&media_type=compressed&tknv=v2"
BYALDI_URL="https://downloader.disk.yandex.com/disk/323b8660bccb0402012beee2db90f31c7bf514489446ae9f740a81546d370c93/6754e465/GORH-WLDFTp3elLhwAv8rUUQR1lMuVpVXFVRqQRGMLWhzJZgb9xroIaqRtLn7ysRThTn00Bf6qc7pc9varfs0g%3D%3D?uid=0&filename=byaldi.zip&disposition=attachment&hash=p%2BBbSxQjFZT2fzkUP7uhizzVpWdzLY%2BruFhj90F%2Bhhii9PxziYwu0JMxb%2BeFi940q/J6bpmRyOJonT3VoXnDag%3D%3D&limit=0&content_type=application%2Fzip&owner_uid=1489006053&fsize=433829224&hid=fb080d1b268c767fdc145dcf07a26d5b&media_type=compressed&tknv=v2"

# Download test_dataset.zip if test_dataset folder does not exist
if [ ! -d "$TEST_DATASET_FOLDER" ]; then
    echo "Folder '$TEST_DATASET_FOLDER' does not exist. Downloading test_dataset.zip..."
    wget -O "test_dataset.zip" "$TEST_DATASET_URL"
    echo "Download completed. Extracting test_dataset.zip..."
    unzip -o "test_dataset.zip" -d "$TEST_DATASET_FOLDER"
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
    unzip -o "byaldi.zip" -d "$BYALDI_FOLDER"
    echo "Extraction completed. Deleting the zip file..."
    rm -f "byaldi.zip"
else
    echo "Folder '$BYALDI_FOLDER' already exists. Skipping download."
fi
