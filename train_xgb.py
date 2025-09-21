import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import joblib
import os

RND = 42
np.random.seed(RND)

def generate_synthetic(n=3000):
    """
    Create synthetic samples approximating relationships:
    - Lower NDVI -> higher baseline LST
    - Higher impervious_frac -> more warming under development
    - parks reduce LST; development increases LST
    """
    current_ndvi = np.clip(np.random.beta(2,5,size=n), 0, 1)   
    imperv = np.clip(np.random.beta(2,2,size=n), 0, 1)
    elevation = np.random.normal(50, 30, size=n).clip(0, 300)
    dist_water = np.random.exponential(scale=2.0, size=n)  
    current_lst = 15 + (1 - current_ndvi) * 15 + imperv * 3 + (elevation/200)*2 + np.random.normal(0,1,n)

    proposed_flag = np.random.choice([1, -1], size=n, p=[0.6, 0.4])

    
    base_effect = imperv * 2.5 - (current_ndvi * 1.5)
    change = proposed_flag * (1.0 + base_effect)  

    change += -0.2 * np.exp(-dist_water/1.0)

    change += -0.005 * elevation

    change += np.random.normal(0, 0.6, size=n)

    df = pd.DataFrame({
        "current_ndvi": current_ndvi,
        "impervious_frac": imperv,
        "elevation": elevation,
        "dist_to_water": dist_water,
        "current_lst": current_lst,
        "proposed_flag": proposed_flag,
        "delta_lst": change
    })
    return df

def train_and_save(df, save_path="xgb_model.joblib"):
    X = df[["current_ndvi","impervious_frac","elevation","dist_to_water","current_lst","proposed_flag"]]
    y = df["delta_lst"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=RND)

    model = xgb.XGBRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        random_state=RND,
        objective="reg:squarederror"
    )
    # simple fit without early stopping (compatible across versions)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test, preds) ** 0.5
    print(f"Test RMSE: {rmse:.3f} °C")

    joblib.dump({"model": model, "features": X.columns.tolist()}, save_path)
    print("Saved model to", save_path)


if __name__ == "__main__":
    df = generate_synthetic(3000)
    os.makedirs("models", exist_ok=True)
    train_and_save(df, save_path="models/xgb_model.joblib")
