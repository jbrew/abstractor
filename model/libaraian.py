import csv
import nltk
import math
import dictionary


punctuation = ['.', ',', '!', '?', '(', ')', '$', ':', ';', '{', '}']


def get_data(path):
	with open(path) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		rows = [row for row in csv_reader]
		return rows

# taks a list of rows where the first row is the column titles
def user_chooses_column(rows):
	column_names = rows[0]
	col_name = get_user_choice(rows[0])
	return all_text_from_column(rows, col_name)

def get_user_choice(options):
	for i, opt in enumerate(options):
		print(str(i+1) + '. ' + opt)
	num_chosen = input('Choose by number:\n')
	try:
		num = int(num_chosen)
		return options[num-1]
	except:
		print('error')
		return "NOT VALID CHOICE"

def all_text_from_column(rows, col_name):

	if col_name in rows[0]:
		n = rows[0].index(col_name)
		return [row[n] for row in rows[1:]]
	else:
		return ''


### TEXT PROCESSING METHODS ###

def split_into_sentences(text):
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	return tokenizer.tokenize(text)

def split_into_words(sentence):
	return [w.lower() for w in nltk.word_tokenize(sentence) if not w in punctuation]


# a dictionary of all terms in the document of length n
def term_dict(doc, n=1):
	term_dict = {}
	words = split_into_words(doc)
	for i in range(len(words)+1-n):
		term = " ".join(words[i:i+n])
		if term in term_dict:
			term_dict[term] += 1
		else:
			term_dict[term] = 1
	return term_dict

def combined_term_dict(tds):
	return dictionary.union(tds)

# a list of dictionaries of terms in the document of length up to n
def term_dicts(corpus, n=1):
	return [term_dict(d, n) for d in corpus]

# list of integers representing term frequency across documents
def frequency_distribution(term, tds):
	freqs = []
	for td in tds:
		if term in td:
			freqs.append(td[term])
		else:
			freqs.append(0)
	return freqs

# how many times the term appears in the document
def term_frequency(term, doc):
	return term_dict(doc)[term]

# how many documents in the corpus include the term
def doc_frequency(term, all_tds):
	return len([1 for td in all_tds if term in td])

# a measure of how topical this term is for this document
def tf_idf(doc, corpus):
	pass

# list of the same length as the corpus list with top tf-idf candidates for topic words
def keywords(corpus, td_list, num_keywords):
	pass


# returns lower and upper bounds containing 95 percent of occurrence rates of the term
def tf_bounds(term, tds, n=2):
	distribution = frequency_distribution(term, tds)
	m = mean(distribution)
	sd = stdev(distribution)
	return m - n*sd, m + n*sd

# returns terms in a dictionary that occur in at least two (or n) dictionaries from a list of dictionaries
def non_unique_terms(term_dict, dict_list, n=2):
	return {k: v for k, v in term_dict.items() if doc_frequency(k, dict_list) >= n}


#### SEARCH ####

# takes a list of docs and a corresponding (equal length) list of term dicts
def docs_containing_term(term, docs, term_dicts):
	return [docs[i] for i, td in enumerate(term_dicts) if term in td]



### STATISTICAL METHODS ####

# standard deviation
def stdev(values):
	N = len(values)
	mean = sum(values) / N
	sum_squared_differences = sum([(x-mean)**2 for x in values])
	return math.sqrt(sum_squared_differences / (N-1))

def mean(values):
	return sum(values) / len(values)







#### TESTS #####

def nips_test():
	rows = get_data('data/Papers.csv')
	titles = all_text_from_column(rows, 'Title')
	abstracts = all_text_from_column(rows, 'Abstract')
	bodies = all_text_from_column(rows, 'PaperText')

	first_abstract = abstracts[0]
	tds = term_dicts(abstracts)

	print(doc_frequency('the', tds))
	print(doc_frequency('in', tds))
	print(term_frequency('the', first_abstract))

def stdev_test():
	print(stdev([1,2,3,4,4,5,6,7]))



def rb_rest():
	rows = get_data('data/Papers.csv')
	abstracts = all_text_from_column(rows, 'Abstract')
	tds = term_dicts(abstracts, 1)
	big_td = combined_term_dict(tds)
	to_save = non_unique_terms(big_td, tds, n=2)
	dictionary.to_tab_delimited(to_save, 'stats/abstracts_1.txt')
	print(docs_containing_term('rao-blackwellized',abstracts,tds))




if __name__ == '__main__':
	rows = get_data('data/Papers.csv')
	abstracts = all_text_from_column(rows, 'Abstract')
	tds = term_dicts(abstracts, 1)
	big_td = combined_term_dict(tds)
	to_save = non_unique_terms(big_td, tds, n=2)

	dictionary.to_tab_delimited(to_save, 'stats/abstracts_1.txt')

	print(docs_containing_term('rao-blackwellized',abstracts,tds))

	"""
	for w, freq in common_terms[:20]:
		print(w, tf_bounds(w, tds, n=1.5))
	"""




class CSVdata(object):

	def __init__(self, fields_requested=None):
		
		self.rows = get_data('data/Papers.csv')
		self.column_names = self.rows[0]

		if fields_requested:
			for f in fields_requested:
				text = all_text_from_column(self.rows, f)
				tds = term_dicts(text, 1)
				big_td = combined_term_dict(tds)


	def dict_and_text_for_field(self, fieldname, n=1):
		text = all_text_from_column(self.rows, fieldname)
		tds = term_dicts(text, n)
		all_term_rates = combined_term_dict(tds)
		return text, tds, all_term_rates

	# for ngrams up to a given size, saves data
	def save_data_from_field(self, field, max_n=2, count_threshold=2):
		pass





	


	


