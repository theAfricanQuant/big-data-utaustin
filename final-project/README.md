# amazon-access-challenge
Our solution to Kaggle's Amazon Access Challenge.

- [Deliverables](#deliverable-locations)
- [Running the Code](#how-to-run)

## Deliverable Locations
1. The screenshot of our highest score is under `report/submission_screnshot.png`
2. Our code is in the `.ipynb` and `.py` files in the top level directory. Instructions on how to run are [below](#how-to-run).
3. Our submission CSV is under `output/xgb_logreg_rf.csv`
4. Our report is under `report/report.pdf`

## How to Run
> Note: You must have [XGBoost](https://xgboost.readthedocs.io/en/latest/) installed in order to re-run the models. If you just wish to run the final ensemble, you do not need the library installed.

Since we have saved the output of all of our individual models, it is easy to run the ensemble by itself. From the top level directory, simply run:

```bash
$ python rankedavg.py submission
```

The `submission` command line argument is the name of the file. The result will be saved to `output/submission.csv`.

---

If you wish to re-train the models, use the following steps:

**1. Run the starter code logistic regressions**

First move into the `reference-code` directory.

```bash
$ cd reference-code/
```

Then, run the starter code.

```bash
$ python starter.py
```

When you are prompted to enter a name for the submission file, enter: `starter_submission`

**2. Run our models**

Go back to the top level directory.

```bash
$ cd ../
```

Then, run the file.

```bash
$ python models.py
```

**3. Now you can run `rankedavg.py` again to get the final ensembled submission**
