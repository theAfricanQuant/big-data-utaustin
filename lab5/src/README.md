To create and run the recommendation engine, use the following steps:

> NOTE: You _*MUST*_ run these commands from the lab5/src directory.

1) Run `init_recommender.py` using basic python to rate 10 random movies and have them be saved to a text file.

```bash
$ python init_recommender.py
```

2) Run `run_recommender.py` using spark-submit with the -r option to run the recommender and see which movies you should watch!

```bash
$ ..../spark-submit --master local[2] run_recommender.py -r
```

