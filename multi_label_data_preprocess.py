import os
import numpy as np
import pandas as pd
import h5py
class AudioPreprocessor:
    def __init__(self, spectrogram_file_path, metadata_file_path):
        self._spectrogram_file_path = spectrogram_file_path
        self._metadata_file_path = metadata_file_path
        self.__set_data()  # Initialize the data storage
    
    def __set_data(self):
        """Initialize the data dictionary as an instance variable."""
        self.data = {
            "train": [],
            "label": []
        }
        
    def _get_data(self):
        return self.data
    
    def _file_handler(self):
        """Process files and store them in self.data."""
        spectrogram_file_path = self._spectrogram_file_path
        metadata = pd.read_csv(self._metadata_file_path)
        column_name = metadata.columns[0]
        # print(metadata.head)
        for (root, dirs, files) in os.walk(spectrogram_file_path):
            for file in files:
                audio_id = int(file.split('.')[0])
                path = os.path.join(root, file)
                
                row = metadata[metadata[column_name] == audio_id]
                # Load the spectrogram data
                spectrogram_data = np.load(path)
                if root.split('/')[0] == "Emotify":
                    label = row.values[:, 2:-1][0]  # Multi-hot encoded label
                    print("Emotify! ")
                elif root.split('/')[0] == "Mid-Level Perceptual Features":
                    label = row.values[:, 1:][0]  # Multi-hot encoded label
                    print("Mid-Level Perceptual Features! ")
                
                print(spectrogram_data)
                print(label)
                break
                # # Append to self.data dictionary
                # self.data["train"].append(spectrogram_data)
                # self.data["label"].append(label)
                
                # # Debugging prints
                # print(f"Audio ID: {audio_id}")
                # print("Spectrogram Data:", spectrogram_data)
                # print("Label (Multi-Hot Encoded):", label)
                # print("-" * 100)
    
    def _save_to_h5(self, h5_file_path):
        if self.data != None:
            with h5py.File(h5_file_path, "w") as hf:
                hf.create_dataset("train", data=np.array(self.data["train"], dtype=np.float32)) # Keeps float32 for DL efficiency
                hf.create_dataset("label", data=np.array(self.data["label"], dtype=np.int8)) # int8 for binary labels

if __name__ == "__main__":
    spectrogram_file_path = "Mid-Level Perceptual Features/spectrograms"
    metadata_file_path = "Mid-Level Perceptual Features/multi_hot_encoded_mid_level_features.csv"
    # spectrogram_file_path = "Emotify/spectrograms"
    # metadata_file_path = "Emotify/multi_hot_encoded_emotify.csv"
    ap = AudioPreprocessor(spectrogram_file_path, metadata_file_path)
    ap._file_handler()
    print(type(ap._get_data()['train']))
    print(type(ap._get_data()['label']))
    # ap._save_to_h5("Data/Emotify_Data.h5")
    # ap._save_to_h5("Data/Mid-Level_Perceptual_Features_Data.h5")