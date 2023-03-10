import joblib # for loading model pickle file
import numpy as np # for array conversion
import pandas as pd # for dataframe conversion
from sklearn.preprocessing import StandardScaler # for standardisation

# FastAPI is a modern, fast (high-performance), web framework for building APIs with Python
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI() # instance of FastAPI class

# mount static folder files to /static route
app.mount("/static",StaticFiles(directory="static"),name="static")

# loads the ML model
model = joblib.load("model/insurance_predictor_1.pkl")


# sets the templates folder for the app
templates = Jinja2Templates(directory="templates")

@app.get("/",response_class=HTMLResponse)
async def home_index(request: Request):
	"""
    Function to render `index.html` at route '/' as a get request
    __Args__:
    - request (Request): request in path operation that will return a template
    __Returns__:
    - TemplateResponse: render `result.html`
    """
	return templates.TemplateResponse("index.html",{"request":request})


@app.post("/predict", response_class=HTMLResponse)
async def predict(
	request: Request,
    age: int = Form(...),
    sex: str = Form(...),
    bmi: float = Form(...),
    children: int = Form(...),
    smoker: str = Form(...)):
	"""
    Function to predict heart diasease classification
    and shows the result by rendering `index.html` at route `/predict`

    __Args__:
    - __request__: request in path operation that will return a template
    - __age__: age of the person ,
    - __sex__: sex of the person,
    - __bmi__: body mass index of the person,
    - __children__: number of children ,
    - __smoker__: does the person smoke or not?

    __Returns:__
    - __TemplateResponse__: render `result.html`
    """

	prediction=0

	sex = 1 if sex.lower() == "male" or "m" else 0
	smoker = 1 if smoker.lower() == "yes" or "y" else 0

	# standardisation
	sc = StandardScaler()

	# convert list to pandas dataframe
	values = pd.DataFrame([[age,sex,bmi,children,smoker]],
		columns=["Age","Sex","bmi","children","smoker"]
		)

	values = sc.fit_transform(values)

	output=model.predict(values) #predicts using the model

	prediction = round(output[0],2)
	
	return templates.TemplateResponse("result.html",context={"request":request,"prediction":prediction})


