import pandas as pd
from constants import FileDef
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from sklearn.model_selection import RepeatedStratifiedKFold, GridSearchCV


def load_data(train_path: str, val_path: str, test_path: str) -> pd.DataFrame:
    train = pd.read_csv(train_path)
    val = pd.read_csv(val_path)
    test = pd.read_csv(test_path)

    return train, val, test


def preprocess_data(
    train: pd.DataFrame, val: pd.DataFrame, test: pd.DataFrame
) -> pd.DataFrame:
    drop_cols = ["domain", "class"]
    X_train = train.drop(columns=drop_cols).convert_dtypes()
    y_train = train["class"].convert_dtypes()
    X_val = val.drop(columns=drop_cols).convert_dtypes()
    y_val = val["class"].convert_dtypes()
    X_test = test.drop(columns=drop_cols).convert_dtypes()
    y_test = test["class"].convert_dtypes()

    return X_train, y_train, X_val, y_val, X_test, y_test


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.DataFrame,
    # X_val: pd.DataFrame,
    # y_val: pd.DataFrame,
    params: dict,
) -> XGBClassifier:
    print("*** TRAINING ***")
    model = XGBClassifier(**params)
    model.fit(
        X_train,
        y_train,
        # eval_set=[(X_train, y_train)],
        verbose=True,
    )

    return model


def tune_model(model: XGBClassifier, X_val: pd.DataFrame, y_val: pd.DataFrame) -> dict:
    print("*** TUNING ***")
    # define the parameter grid
    param_grid = {
        "learning_rate": [0.01, 0.05, 0.1, 0.2],
        "max_depth": [3, 6, 9, 12],
        "subsample": [0.6, 0.8, 1.0],
        "colsample_bytree": [0.6, 0.8, 1.0],
    }

    # define the cross-validation strategy
    cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)

    # perform the grid search
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=cv,
        n_jobs=-1,
        scoring="accuracy",
    )

    # fit the grid search to the data
    grid_search.fit(X_val, y_val)

    # get the best hyperparameters
    best_params = grid_search.best_params_

    return best_params


def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-score:", f1)
    print("Confusion matrix:\n", cm)


def main():
    train, val, test = load_data(
        FileDef.TRAIN.value, FileDef.VALIDATE.value, FileDef.TEST.value
    )
    X_train, y_train, X_val, y_val, X_test, y_test = preprocess_data(train, val, test)

    # define our parameters for the model
    train_params = {
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "learning_rate": 0.1,
        "early_stopping_rounds": 10,
        "booster": "gbtree",
        "grow_policy": "lossguide",
        "n_jobs": -1,
    }
    model = train_model(X_train, y_train, train_params)

    tuned_params = tune_model(model, X_val, y_val)
    # retrain using better parameters
    tuned_model = train_model(X_train, y_train, tuned_params)

    evaluate_model(tuned_model, X_test, y_test)


if __name__ == "__main__":
    main()
