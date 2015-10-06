import os 
import sys
import math
from operator import itemgetter
from collections import OrderedDict


#==============================================================================|
#@name: get_filenames_from_dir(corpus_dir)									   |
#@input: Path to directory where corpus files are present.					   |
#@output: List having filenames												   |
#@brief: 																	   |
#      This function returns a list of all the files with .txt as extension    |
#      present in "corpus_dir" path											   |
#==============================================================================|
def get_filenames_from_dir(corpus_dir):
	#files_list	=	[]
	#files_list = os.listdir(corpus_dir)
	#return files_list
	return os.listdir(corpus_dir)

#==============================================================================|
#@name: get_IDF(corpus_dir,files_list,word)									   |
#@input: corpus_dir: Directory where corpus files are present				   |
#        files_list: List of filename present in corpus_dir path			   |
#		 word: word from the query enetred by the user						   |
#@output: dictionary														   |
#@brief: 																	   |
#      This function returns a dictionary having words of the query string as  |
#	   keys and thier IDF in the filename as the values for the keys.		   |
#==============================================================================|		
def get_IDF(corpus_dir,filenames,word):
	num_of_docs					=	len(filenames)
	num_of_docs_having_word		=	0
	word						=	word.lower()
	
	for filename in filenames:
		# Increment num_of_docs_having_word by 1 for each file having the word
		mfile = open(corpus_dir + filename ,"r")
		file = mfile.read().lower()
		words_of_file = file.lower().split()
		mfile.close()
		if words_of_file.__contains__(word) :
			num_of_docs_having_word = num_of_docs_having_word + 1
	if(num_of_docs_having_word > 0):
		#print word + " Found !!"
		#print num_of_docs, num_of_docs_having_word
		return math.log10(float(num_of_docs)/float(num_of_docs_having_word))
	else:
		#print word + " not found !!"
		return 0
		
#==============================================================================|
#@name: get_TF(corpus_dir,files_list,ip_query)								   |
#@input: corpus_dir: Directory where corput files are present				   |
#        files_list: List of filename present in corpus_dir path			   |
#		 query_string: Query enetred by the user							   |
#@output: dictionary														   |
#@brief: 																	   |
#      This function returns a dictionary having words of the query string as  |
#	   keys and thier TF in the filename as the values for the keys.		   |
#==============================================================================|		
def get_TF(corpus_dir,filename,query_string):
	ret_dict 		=   {}
	
	
	#		Step 1: Convert the string in lower case. 
	#		Step 2: Spilt the string at word boundary and store the words in a list
	#       Step 3: Find the frequency of each word of the query string  in the 
	# 				above created list and store it ret_dict dictionary.
	#		Step 4: Return the above cretaed dictionary.
	mfile = open(corpus_dir+filename,"r")
	file = mfile.read().lower()
	words_of_file = file.lower().split()
	mfile.close()
	#ip_list = []
	#ip_list = ip_list.lower()
	ip_list = query_string.lower().split()
	for query_word in ip_list :
		count_of_word = 0
		for word in words_of_file :
			if(query_word.lower() == word.lower()):
				count_of_word = count_of_word + 1
			ret_dict[query_word] = (0.5 + float((0.5*count_of_word)/len(words_of_file)))
	return ret_dict

#==============================================================================|
#@name: get_input()															   |
#@input: void																   |
#@output: dictionary														   |
#@brief: 																	   |
#      This function reads the command line arguments to get  the query string.|
#	   If a valid query string is found it returns a dictionary with value for |
#	   key 'is_valid',  set as True and for 'user_input' the query string.	   |
#      In case of invalid input value for 'is_valid' and 'user_input' is set   |
#      as False and null respectively. 										   |
#==============================================================================|
def get_input()	:
	user_input = ""
	is_valid = False
	#print "\n--------------------PRINTING ARGUMENTS--------------------\n"
	#print sys.argv
	#user_input = sys.argv[1].lower
	
	try:
		user_input = sys.argv[1].lower()
		is_valid = True
		#TODO: Impplement Me
	except:
		print "Usage: #python tf_idf.py <Query String>"
		#TODO: Impplement Me
	return {"is_valid":is_valid , "user_input":user_input }
		

if __name__ == "__main__":

	input = get_input()
	
	if(input["is_valid"]):
		ip_query		=	input["user_input"]
		tf_dict			=	{}
		idf_dict		=	{}
		filenames		=	[]
		
		# Path to the corpus
		corpus_dir	=	"./../corpus/"
		
		filenames = get_filenames_from_dir(corpus_dir)
		
		#print input["user_input"]
		
		for word in ip_query.lower().split():
			idf_dict[word]	=	get_IDF(corpus_dir,filenames,word)
			
		for filename in filenames:
			tf_dict[filename] = get_TF(corpus_dir,filename,ip_query) 
			
		#print idf_dict
		#print "--------------------------------------------\n\n"
		#print tf_dict
		#print "--------------------------------------------\n\n"
		
		TF_IDF_Score = {}
		for filename in filenames:
			ret_dict = {}
			ip_list = ip_query.lower().split()
			TF_IDF_Score[filename]  =   0
			
			for query_word in ip_list:
				query_word = query_word.lower()
				#TODO: Set the right value of word_tf and word_idf
				try:
					word_idf = idf_dict[query_word]
				except:
					print "Error : IDF for "+query_word + " not found in the dictionary !!"
					word_idf = 0
				try:
					word_tf = tf_dict[filename][query_word]
				except:
					print "Error : TF for "+query_word + " not found in the dictionary !!"
					word_tf = 0
				
				TF_IDF_Score[filename] = TF_IDF_Score[filename] +(word_idf*word_tf)
		#print "\n-----------------THE TF-IDF DICTIONARY IS--------------------\n"
		#print TF_IDF_Score
				
		
		# Below we are sorting the TF_IDF_Score dictionary on the basis of value
		# and printing it.
		ordered_dict = OrderedDict(sorted(TF_IDF_Score.items(), key=itemgetter(1)))
		sorted_keys = ordered_dict.keys()
			
		idx	=	len(sorted_keys) -1 
		print "\n\nQUERY IS :"+ input["user_input"]
		print "\n------- FILES SORTED IN THE ORDER OF THEIR RELEVANCE -----------------\n"
		while(idx>=0):
			key = sorted_keys[idx]
			print sorted_keys[idx] + "\t"+str(TF_IDF_Score[key])  
			idx = idx -1
		print "\n\n-------------------THE MOST RELEVANT FILE------------------------\n\n"
		print sorted_keys[idx]
