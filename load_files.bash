#!/bin/bash

# Define the folder and download URLs
TEST_DATASET_FOLDER="test_dataset"
BYALDI_FOLDER=".byaldi"
COLPALI_FOLDER="colpali"

TEST_DATASET_URL="https://drive.usercontent.google.com/download?id=1AFSU1aeTbjbZ-cHmIPWJ0C9PDIDf1bHY&export=download&confirm=t&uuid=41de660c-c39f-4358-8726-9c1e4848f103"
BYALDI_URL="https://drive.usercontent.google.com/download?id=197SjbwY_ZowLWrAKXp3Wx7X8TxVdOboC&export=download&confirm=t&uuid=6e576b98-c69d-4273-8764-f6b974f09e04"
COLPALI_URL="https://drive.usercontent.google.com/download?id=15vR6j-JHJAKi6IjeIxDHshPTjH12vgZN&export=download&confirm=t&uuid=4c4fa357-743c-4fc7-9b8d-cc883ea8dfdf"

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
