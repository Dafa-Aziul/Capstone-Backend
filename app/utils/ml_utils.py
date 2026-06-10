import joblib
import pandas as pd
import numpy as np
import shap


def load_ml_artifacts(model_path):
    try:
        artifacts = joblib.load(model_path)
        
        if isinstance(artifacts, dict) and 'model' in artifacts and 'preprocessor' in artifacts:
            model = artifacts['model']
            preprocessor = artifacts['preprocessor']
        elif isinstance(artifacts, tuple) and len(artifacts) == 2:
            model, preprocessor = artifacts
        else:
            raise RuntimeError("File .joblib tidak memiliki format yang diharapkan (bukan dict atau tuple).")
            
        if not hasattr(preprocessor, 'transform'):
            raise RuntimeError("Objek 'preprocessor' tidak memiliki fungsi transform(). Pastikan menggunakan ColumnTransformer.")
        if not hasattr(model, 'predict'):
            raise RuntimeError("Objek 'model' tidak memiliki fungsi predict().")
            
        return model, preprocessor
    except Exception as e:
        raise RuntimeError(f"Gagal memuat model atau preprocessor: {e}")


def get_clean_feature_names(preprocessor):
    feature_names = preprocessor.get_feature_names_out()
    return [f.split("__")[-1] if "__" in f else f for f in feature_names]


def transform_to_dataframe(transformed_data, clean_feature_names):
    if not isinstance(transformed_data, pd.DataFrame):
        if hasattr(transformed_data, "toarray"):  # Jika bentuknya sparse matrix
            transformed_data = transformed_data.toarray()
        return pd.DataFrame(transformed_data, columns=clean_feature_names)
    
    transformed_data.columns = clean_feature_names
    return transformed_data


def generate_shap_explanation(model, transformed_data, clean_feature_names):
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(transformed_data)
    
    expected_val = explainer.expected_value
    if isinstance(expected_val, (np.ndarray, list)):
        expected_val = expected_val[0]

    return {
        "base_value": float(expected_val),
        "feature_contributions": {
            feature: float(value) for feature, value in zip(clean_feature_names, shap_values[0])
        }
    }