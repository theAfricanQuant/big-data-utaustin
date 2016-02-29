# Part 2 starter code

from mrjob.job import MRJob
from mrjob.step import MRStep

class MRMovielens(MRJob):

    def steps(self):
	# This function defines the steps your job will follow. If you want to chain jobs, you can just have multiple steps.
        return [
	    # Running the same MapReduce job twice
            MRStep(mapper=self.mapper1, reducer=self.reducer1), 		
            MRStep(mapper=self.mapper1, reducer=self.reducer1),		
        ]


    def mapper1(self, _, value):
        return None


    def reducer1(self, key, value):
	return None


if __name__ == '__main__':
    MRMovielens.run()
