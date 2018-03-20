# Declear constants:

# path to the test/training files, please change accordingly
BAD_REVIEW_TRAINING = r'C:\Users\Pacific\Desktop\Fall2017\COMP151_AI\project3\bad.txt'

GOOD_REVIEW_TRAINING = r'C:\Users\Pacific\Desktop\Fall2017\COMP151_AI\project3\good.txt'

TEST_FILE_PATH = 'C:\\Users\\Pacific\\Desktop\\Fall2017\\COMP151_AI\\project3\\'

# set this True test the test files provided from 1 to 8, set it to false if you want to test your own files
SELF_TEST_MODE = True

# please provide the full path of the test file if you set the SELF_TEST_MODE to false
TEST_OWN_FILE = ''

# this constant is to prevent 0 probability if a word in the test file doesn't exist in the training file
LOW_PROB = 0.00000001

# prevent underflow
MAGNIFYING_CONST = 1000

# display option for the dumpContentOfMap function, set to True if you want to display
DISPLAY = False

# outFile option for the dumpContentOfMap function, set the name of the name you want to save the contents to,
# set to None if you don't want to save
OUTFILE = None

# remove the common words
REMOVE_WORDS = ['the', 'a', 'and', 'is', 'of']