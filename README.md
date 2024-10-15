# EPITECH 2022, Guided Project: Innovation Hub
## Airbnb Calculator

The idea of the project is to create a prototype of digital product and deploy it for beta testing.
After brainstorming and discussing several promising ideas we decided to create a **tool for Airbnb users**.
Presentation available [here](https://github.com/koliverdavera/innovation_hub_airbnb/tree/main/project%20presentation).

### Project description
We created a web application to estimate the best price for accommodation per night (PPN - price per night). 
A user enters information about housing to check and immediately gets predicted price. 
This product can be used by both property owners to get the best revenue from real estate and
by travelers to check whether the price for accommodation is adequate.

### Model for PPN prediction
We followed several steps to build appropriate model.
1. We chose an [Airbnb open dataset](http://insideairbnb.com/paris) to train the model.
2. We conducted extensive [EDA](https://github.com/koliverdavera/innovation_hub_airbnb/blob/main/backend/model/reports/Airbnb_EDA.ipynb)
to better understand the product and prepare it for model engineering and training.
3. The task for model to solve is a basic linear regression. We created several predicting [model baselines](https://github.com/koliverdavera/innovation_hub_airbnb/blob/main/backend/model/reports/Airbnb_model.ipynb).
Gradient boosting model (XGBoost) achieved the highest score.

In the future, we will implement time series forecasting so that PPN prediction becomes more accurate. 
There are noticeable trends in seasonality for accommodation prices on Airbnb.

### Frameworks used for development and deployment
Web application backend is built on Flask, frontend on Vue Js. Backend and frontend components interact using REST API. 
It was deployed on Microsoft Azure and Heroku.
