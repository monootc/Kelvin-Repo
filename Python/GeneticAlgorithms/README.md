Description:	Chartists are financial experts who look for recurring shape patterns in stock prices
				and then use those patterns to predict future stock movements. For this project you will be creating
				a genetic algorithm to detect 2-day chart patterns in financial data.

				
Training File Data:	You will be provided with two files of data: genAlgData1.txt and
					genAlgData2.txt. The files each contain training data based on 30 years of price data for the S&P
					500. For debugging purposes you are required to create small hand-designed data files to test for
					correctness – you will turn in the testing file(s) as part of your submission.

Fitness Function:	When it comes to computing the fitness of a chromosome, you will sweep
					through all of the historical data in the data file you’re using. You will check each line to see if it
					matches the pattern specified by the chromosome and then compute the total gain/loss, if the
					trader had followed the chromosome’s recommendation.


Creating the Next Generation:	You will create the next generation using a combination of
								selection, crossover and mutation. First you will select X of the chromosomes from the current
								generation to be cloned into the next generation. Then you will use crossover the create the
								remaining (PopulationSize – X) of the chromosomes for the next generation. Once the new
								chromosomes have been created, you should iterate over them and with a Z% probability, trigger a
								mutation on each gene.


Output:	After each 10 generations your program should display the max, min and average (mean or
		median is fine) fitness of the chromosomes in the population (which should be straightforward if you
		sorted your population as part of the selection process). At the end of running all the generations,
		your code should find the highest fitness chromosome from the final generation and display the
		chromosome to the screen.