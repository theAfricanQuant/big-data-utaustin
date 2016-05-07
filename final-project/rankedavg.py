import sys

from collections import defaultdict

def rank_avg(files, outfile):
    with open(outfile, 'w') as out:
        ranks = defaultdict(list)
        for i, f in enumerate(files):
            file_ranks = []

            lines = open(f).readlines()
            lines = [lines[0]] + sorted(lines[1:])
            for e, line in enumerate(lines):
                if e > 0:
                    r = line.strip().split(",")
                    file_ranks.append((float(r[1]), e, r[0]))

            for rank, item in enumerate(sorted(file_ranks)):
                ranks[(item[1],item[2])].append(rank)

        average_ranks = []
        for k in sorted(ranks):
            average_ranks.append((sum(ranks[k])/len(ranks[k]), k))

        ranked_ranks = []
        for rank, k in enumerate(sorted(average_ranks)):
            ranked_ranks.append((k[1][0], k[1][1], rank/(len(average_ranks) - 1)))

        out.write('Id,Action\n')
        for k in sorted(ranked_ranks):
            out.write('{},{}\n'.format(k[1], k[2]))

def main():
    if len(sys.argv) != 2:
        print('Usage: python rankavg.py OUTFILE\nDo not include the \'.csv\' extension.')
        exit(1)

    # These files are the submissions that we are throwing together in the ensemble.
    files = [
        'reference-code/starter_submission.csv', # Logistic Regression from Paul Duan.
        'output/xgb_155trees_colsampletree.5_learningrate0.3_maxdepth8_.86928.csv', # XGBoost
        'output/rf_1ktrees_entropy_auto_bootstrapped_.86757.csv', # Random Forest
    ]
    
    outfile = 'output/{}.csv'.format(sys.argv[1])
    rank_avg(files, outfile)

if __name__ == '__main__':
    main()
