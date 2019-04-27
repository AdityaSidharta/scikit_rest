import numpy as np
import pandas as pd
import datetime
from dateutil.parser import parse
from collections import OrderedDict
from flask_restful import Resource, reqparse

from scikit_rest.validator import validate_args
from scikit_rest.type import set_type


class Prediction(Resource):
    def __init__(self, **kwargs):
        self.col_list = kwargs["col_list"]
        self.col_types = kwargs["col_types"]
        self.transform_fn = kwargs["transform_fn"]
        self.predict_fn = kwargs["predict_fn"]
        self.is_nullable = kwargs["is_nullable"]

        self.parser = reqparse.RequestParser()
        for col in self.col_list:
            self.parser.add_argument(col)
        self.args = self.parser.parse_args()

        self.result = np.nan
        self.status_message = "Success"
        self.status_code = 200

        is_success, status_message = validate_args(self.args, self.col_types, self.is_nullable)
        if not is_success:
            self.status_message = status_message
            self.status_code = 400

    def output(self):
        return (
            {"data": {"result": self.result}, "message": {"status_message": self.status_message, "args": self.args}},
            self.status_code,
        )

    def get(self):
        if self.status_code == 200:
            input_dict = OrderedDict()
            for col in self.col_list:
                value = set_type(self.args[col], self.col_types[col])
                input_dict[col] = [value]
            input_df = pd.DataFrame(input_dict)
            transformed_df = self.transform_fn(input_df)
            self.result = self.predict_fn(transformed_df)
        return self.output()
