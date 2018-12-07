from flask import Flask
from flask import jsonify
import xgboost as xgb
import pickle
import pandas as pd 
import numpy as np
from tabulate import tabulate
import logging

logging.basicConfig(format = '%(asctime)s - %(levelname)s - %(name)s -   %(message)s', 
                    datefmt = '%m/%d/%Y %H:%M:%S',
                    level = logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route("/user/<userID>")
def show_user_credit(userID):
	# load model
	model = pickle.load(open("model.pkl","rb"))

	# load dataset
	val_df = pd.read_csv("val_df.csv")

	# define useful column
	target = 'default.payment.next.month'
	predictors = ['LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE', 
	              'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
	              'BILL_AMT1','BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
	              'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']
	inpu_id = int(userID)
	test_row = val_df.loc[lambda val_df: val_df.ID==inpu_id, :]
	logger.info(tabulate(test_row.T, headers='keys'))

	dvalid = xgb.DMatrix(test_row[predictors], test_row[target].values)
	logger.info("XGBoost inference...")

	output = model.predict(dvalid)[0]
	logger.info("probability of default payment: %s" % str(output))

	Odds=output/(1-output)
	FICO = 437-58*np.log(Odds)
	logger.info("Transformed score: %s" % str(FICO))
	# return 'Credit score of user %s: %s; FICO score:%s' % (userID, str(output), str(FICO))
	return jsonify(user_id=userID, original_prob=str(output), FICO_score=str(FICO))
if __name__ == "__main__":
    app.run()