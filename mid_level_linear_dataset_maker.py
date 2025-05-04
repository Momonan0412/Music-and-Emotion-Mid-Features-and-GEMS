import os
import h5py
import numpy as np
import pandas as pd
from keras.api.models import load_model, Model

class MidLevelLinearDatasetMaker:
    def __init__(self, directory):
        self.__directory = directory
        self.__data = None
        self.__model = None
        
        self.__set_data()  # Initialize the data storage
    
    def __set_data(self):
        """Initialize the data dictionary as an instance variable."""
        self.data = {
            "train": [],
            "label": []
        }
        
    def _load_data(self):
        with h5py.File("Data/Emotify_Data_For_Correlation.h5", "r") as hf:
            train = hf["train"][:]
            label = hf["label"][:]
        data = { "train": train, "label": label}
        self._data_setter(data)
    
    def _annotator(self):
        data_array = self._data_getter()["train"][..., np.newaxis]
        for data in data_array:
            single_input = data[np.newaxis, ...]
            prediction = self._predictor(single_input)
            self.data["train"].append(prediction)
            print(prediction)
        self.data["label"] = self._data_getter()["label"]
    
    def _load_model(self):
        model = load_model(self._directory_getter())
        self._model_setter(model)
    
    def _predictor(self, data):
        predictions = self._model_getter().predict(data)
        predicted_labels = np.array(predictions, dtype=np.float32)
        return predicted_labels[0]
    
    # Getters and Setters
    def _data_setter(self, data):
        self.__data = data
    
    def _data_getter(self):
        return self.__data
    
    def _model_setter(self, model):
        self.__model = model
    
    def _model_getter(self):
        return self.__model
    
    def _directory_getter(self):
        return self.__directory
    
    def _get_data(self):
        return self.data

    def _save_to_h5(self, h5_file_path="Data/Mid_Level_Linear_Dataset_Data_For_Correlation.h5"):
        if self.data != None:
            with h5py.File(h5_file_path, "w") as hf:
                hf.create_dataset("train", data=np.array(self.data["train"], dtype=np.float32)) # Keeps float32 for DL efficiency
                # hf.create_dataset("label", data=np.array(self.data["label"], dtype=np.int8)) # int8 for binary labels
                hf.create_dataset("label", data=np.array(self.data["label"], dtype=np.float32)) # For Correlation
if __name__ == "__main__":
    model_dir = "Mid-Level_Perceptual_Features_Multi-Label Version 1.keras"
    da = MidLevelLinearDatasetMaker(model_dir)
    da._load_data()
    da._load_model()
    da._annotator()
    # print("Type: ", type(da._get_data()))
    # print("Shape Train: ", da._get_data()['train'][0].shape)
    # print("Shape Label: ", da._get_data()['label'][0].shape)
    da._save_to_h5()