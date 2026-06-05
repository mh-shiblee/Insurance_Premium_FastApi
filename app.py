from fastapi import FastAPI
from fastapi.responses import JSONResponse

from model.predict import predict_premium, Model_version, model

from schema.client_input import UserData

from schema.response import Response

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to the Insurance Premium Prediction API. Use the /predict endpoint to get a premium prediction based on your data."}


@app.get("/health")
def health_check():
    return {"status": "ok",
            "version": Model_version,
            "model_loaded": model is not None
            }


@app.post("/predict", response_model=Response)
def predict(data: UserData):
    # convert the user data to a dataframe
    user_input = {
        "bmi": data.bmi,
        "lifestyle_risk": data.lifestyle_risk,
        "age_group": data.age_group,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }
    # make the prediction
    try:
        prediction = predict_premium(user_input)
        return JSONResponse(content={"Response": prediction})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
