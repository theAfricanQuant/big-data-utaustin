DIR=./output
if [ -d "$DIR" ]; then
    printf '%s\n' "Removing output directory"
    rm -rf "$DIR"
fi
hadoop jar /usr/local/hadoop/hadoop-streaming.jar -files src/mapper.py,src/reducer.py -mapper src/mapper.py -reducer src/reducer.py -input data/book.txt -output output
