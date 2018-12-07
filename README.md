# auto-credit
Automatically provide credit score for a given customer based on his/her history payment data.
## Usage
```
curl -X GET https://auto-credit.herokuapp.com/user/{user id}
```
For example:
```
curl -X GET https://auto-credit.herokuapp.com/user/29909
```

The options for user id please refer to ID column in [val_df.csv](https://github.com/thtang/auto-credit/blob/master/val_df.csv).

#### Output Json:
```JSON
{"FICO_score": "509.009864269",
 "original_prob": "0.224166",
 "user_id": "29909"}
```
