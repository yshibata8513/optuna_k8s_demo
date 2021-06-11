import os
from logging import getLogger

from fastapi import FastAPI

import json
from logging import getLogger
from typing import Dict, List, Sequence

import numpy as np
import onnxruntime as rt
from pydantic import BaseModel
from src.app.configurations import ModelConfigurations

# from predictor import classifier


logger = getLogger(__name__)



class Classifier(object):
    def __init__(
        self,
        model_filepath: str,
        # label_filepath: str,
    ):
        self.model_filepath: str = model_filepath
        # self.label_filepath: str = label_filepath
        self.classifier = None
        # self.label: Dict[str, str] = {}
        self.input_name: str = ""
        # self.output_name: str = ""

        self.load_model()
        # self.load_label()

    def load_model(self):
        # logger.info(f"load model in {self.model_filepath}")
        self.classifier = rt.InferenceSession(self.model_filepath)
        self.input_name = self.classifier.get_inputs()[0].name
        # self.output_name = self.classifier.get_outputs()[0].name
        # logger.info(f"initialized model")

    # def load_label(self):
    #     logger.info(f"load label in {self.label_filepath}")
    #     with open(self.label_filepath, "r") as f:
    #         self.label = json.load(f)
    #     logger.info(f"label: {self.label}")

    def predict(self, x:float,y:float,head:float,v:float,delta:float) :
        np_data = np.array([x,y,head,v,delta]).astype(np.float32)
        prediction = self.classifier.run(None, {self.input_name: np_data})
        # print("prediction")
        # print(prediction)
        # output = np.array(list(prediction[0].values()))
        # print("output")
        # print(output)
        # # logger.info(f"predict proba {output}")
        return prediction[0]

    # def predict_label(self, data: List[List[int]]) -> str:
    #     prediction = self.predict(data=data)
    #     argmax = int(np.argmax(np.array(prediction)))
    #     return self.label[str(argmax)]


classifier = Classifier(
    model_filepath=ModelConfigurations().model_filepath,
    # label_filepath=ModelConfigurations().label_filepath,
)




app = FastAPI(
    title="kinematic_mode_test",
    description="kinematic_mode_test",
    version="0.1",
)


@app.get("/calc")
def calc(x:float,y:float,head:float,v:float,delta:float):
    prediction = classifier.predict(x,y,head,v,delta)
    x = prediction[0]
    y = prediction[1]
    head = prediction[2]
    output = str(x)+","+str(y)+","+str(head)
    return {"prediction":output}

@app.get("/simple")
def calc(x:float):
   
    return {"message": x}

@app.get("/")
def calc():
   
    return {"message": "hello"}
# def calc():

#     return {"message": "hello"}

# def calc(x:float,y:float):
#     z = x + y
#     return {"message": z}
