from src.model.model_structure import model

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
model(LinearRegression, mean_absolute_error)