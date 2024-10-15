import os
import sys
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from pickle import load


numerical = (
     "host_is_superhost",
     "host_total_listings_count",
     'latitude',
     'longitude', 'accommodates', 'bathrooms', 'minimum_nights',
     'maximum_nights', 'availability_90', 'number_of_reviews',
     'review_scores_accuracy', 'calculated_host_listings_count'
)
categorical = (
    "host_response_time",
    "neighbourhood",
    "property_type",
    "room_type",
    "time_since_first_review",
    "time_since_last_review"
)
bins = (
    "review_scores_rating",
    "time_since_first_review",
    "time_since_last_review"
)
amenities = (
    'air_conditioning', 'bed_linen', 'tv', 'coffee_machine',
    'cooking_basics', 'white_goods', 'elevator', 'parking',
    'host_greeting', 'internet', 'long_term_stays', 'private_entrance'
)


def get_time_since_first_review(days: int) -> str:
    bins = [182, 365, 730, 1460, 5000]
    labels = ['0-6 months',
              '6-12 months',
              '1-2 years',
              '2-3 years',
              '4+ years']
    for bin, label in zip(bins, labels):
        if days < bin:
            return label


def get_time_since_last_review(days: int) -> str:
    bins = [14, 60, 182, 365, 5000]
    labels = ['0-2 weeks',
              '2-8 weeks',
              '2-6 months',
              '6-12 months',
              '1+ year']
    for bin, label in zip(bins, labels):
        if days < bin:
            return label


def preprocess_request(params: dict,
                       model_name="airbnb_predictor.json",
                       feature_scaler_name="feature_scaler.pkl"
                       ) -> pd.DataFrame:
    """
    :param params: a dictionary containing all features for prediction (as described in Notion)
    :param model_name: name of file containing pretrained model
    :param feature_scaler_name: name of file containing pretrained feature scaler
    :return: pd.DataFrame containing 1 object with processed features
    """
    model = XGBRegressor()
    model.load_model(model_name)
    result = pd.DataFrame(np.zeros((1, len(model.feature_names_in_))),
                          columns=model.feature_names_in_)
    for feature, value in params.items():
        if feature in numerical:
            result[feature][0] = float(value)
        if feature in categorical:
            col_name = f"{feature}_{value}"
            result[col_name][0] = 1
        if feature in bins:
            if "first" in feature:
                result[feature][0] = get_time_since_first_review(value)
            elif "last" in feature:
                result[feature][0] = get_time_since_last_review(value)
            else:
                if value < 80:
                    result["review_scores_rating_0-79/100"] = 1
        if type(value) == list:
            for elem in value:
                if elem in amenities:
                    result[elem][0] = 1
    if feature_scaler_name:
        feature_scaler_ = load(open(feature_scaler_name, 'rb'))
        result = feature_scaler_.transform(result)
    return result


def _predict(obj: pd.DataFrame,
             model_name="airbnb_predictor.json",
             target_scaler_name="target_scaler.pkl") -> float:
    """
    :param obj: object with features prepared for prediction
    :param model_name: name of file containing pretrained model
    :param target_scaler_name: name of file containing pretrained target scaler
    :return: float model price prediction
    """
    target_scaler_ = load(open(target_scaler_name, 'rb'))
    model = XGBRegressor()
    model.load_model(model_name)
    result = round(abs(model.predict(obj) * target_scaler_.scale_)[0])
    return result


def get_prediction(params: dict) -> float:
    """
    :param params: a dictionary containing all features for prediction (as described in Notion)
    :return: price prediction
    """
    obj = preprocess_request(params,
                             model_name="model/trained_objects/airbnb_predictor.json",
                             feature_scaler_name="model/trained_objects/feature_scaler.pkl")
    price = _predict(obj,
                     model_name='model/trained_objects/airbnb_predictor.json',
                     target_scaler_name="model/trained_objects/target_scaler.pkl")
    return price
