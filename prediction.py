import json
import numpy as np


class Prediction:
    def __init__(
        self,
        single_prediction: np.intp,
        confidence: float,
        full_prediction: np.ndarray,
        mapping_file: str = "filtered_map.json",
    ):
        self.single_prediction = single_prediction
        self.confidence = confidence
        self.full_prediction = full_prediction
        try:
            with open(mapping_file, "r") as file:
                data = json.load(file)
            self.plant_name = data[str(self.single_prediction)]
        except OSError:
            self.plant_name = "Error reading mapping file"
