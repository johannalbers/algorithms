
header = ["color", "diameter", "label"]




'''
helper functions
'''

def class_counts(rows):
	#counts is of form: {'Apple' -> 2, 'Birne' -> 1, ...}
	counts = {}
	for row in rows:
		label = row[-1]
		if label not in counts:
			counts[label] = 0
		counts[label] += 1
		
	return counts

	
def gini(rows):
	counts = class_counts(rows)
	impurity = 1
	for label in counts:
		label_prob = counts[label] / float(len(rows))
		impurity -= label_prob**2
		
	return impurity


def isNumeric(val):
	return isinstance(val, int) or isinstance(val, float)
	


	
	
'''
classes
'''

class Leaf():
	def __init__(self, rows):
		self.predictions = class_counts(rows)
		
		
class Decision_Node:
	def __init__(self, question, true_branch, false_branch):
		self.question = question
		self.true_branch = true_branch
		self.false_branch = false_branch
		
	
class Question:
	def __init__(self, column, value):
		self.column = column
		self.value = value
		
	def match(self, example_row):
		val = example_row[self.column]
		if isNumeric(val):
			return val >= self.value
		else:
			return val == self.value
			
	def __repr__(self):
		condition = "=="
		if isNumeric(self.value):
			condition = ">="
		return "Is %s %s %s" % (header[self.column], condition, str(self.value))
		
	
	
	
	
'''
main functions
'''

def partition(rows, question):
	true_rows, false_rows = [], []
	for row in rows:
		if question.match(row):
			true_rows.append(row)
		else:
			false_rows.append(row)
			
	return true_rows, false_rows
	
	
def info_gain(left, right, current_uncertainty):
	'''
	The uncertainty of the starting node, minus the weighted impurity of
    two child nodes.
    '''
	p = float(len(left)) / (len(left) + len(right))
	return current_uncertainty - p * gini(left) - (1 - p) * gini(right)
	
	
def find_best_split(rows):
	best_gain = 0
	best_question = None
	current_uncertainty = gini(rows)
	n_features = len(rows[0]) - 1
	
	for col in range(n_features):
		values = set(row[col] for row in rows)
		
		for value in values:
			question = Question(col, value)
			
			true_rows, false_rows = partition(rows, question)
			
			if len(true_rows) == 0 or len(false_rows) == 0:
				continue
				
			gain = info_gain(true_rows, false_rows, current_uncertainty)
			
			if gain >= best_gain:
				best_gain, best_question = gain, question
				
				
	return best_gain, best_question
				
				
def build_tree(rows):
	gain, question = find_best_split(rows)
	
	if gain == 0:
		return Leaf(rows)
		
	#Recursively build here
	true_rows, false_rows = partition(rows, question)
	
	true_branch = build_tree(true_rows)
	
	false_branch = build_tree(false_rows)
	
	return Decision_Node(question, true_branch, false_branch)
	
	
	
	
	
'''
functions to print the tree and test data
'''

def classify(row, node):
	if isinstance(node, Leaf):
		return node.predictions
		
	if node.question.match(row):
		return classify(row, node.true_branch)
	else:
		return classify(row, node.false_branch)

		
def print_leaf(counts):
	total = sum(counts.values()) * 1.0
	probs = {}
	for label in counts.keys():
		probs[label] = str(int(counts[label] / total * 100)) + "%"
	return probs
	
	
	
	
	
'''
prints the tree in a nice human readable form
'''
	
# functoin to print tree
def print_tree(node, spacing=""):

    # Base case: we've reached a leaf
    if isinstance(node, Leaf):
        print (spacing + "Predict", node.predictions)
        return

    # Print the question at this node
    print (spacing + str(node.question))

    # Call this function recursively on the true branch
    print (spacing + '--> True:')
    print_tree(node.true_branch, spacing + "  ")

    # Call this function recursively on the false branch
    print (spacing + '--> False:')
    print_tree(node.false_branch, spacing + "  ")

	
	
	
	
'''
main function
'''
	
if __name__ == "__main__":

	training_data = [
		['Green', 3, 'Apple'],
		['Yellow', 3, 'Apple'],
		['Red', 1, 'Grape'],
		['Red', 1, 'Grape'],
		['Yellow', 3, 'Lemon'],
	]
	
	first_tree = build_tree(training_data);
	
	print_tree(first_tree)
	
	
	
	
	#Evaluate
	testing_data = [
        ['Green', 3, 'Apple'],
        ['Yellow', 4, 'Apple'],
        ['Red', 2, 'Grape'],
        ['Red', 1, 'Grape'],
        ['Yellow', 3, 'Lemon'],
    ]


	for row in testing_data:
		print ("Actual: %s. Predicted: %s" % (row[-1], print_leaf(classify(row, first_tree))))