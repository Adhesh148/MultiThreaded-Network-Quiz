
def getQuestions(questions,solutions):
	file = open("questionBank.txt","r")
	print("[FILE IO] File has been opened")

	# read until beginning of Quesitons.
	line = file.readline()
	while line:
		if line.strip().split(" ")[0] == "BEGIN":
			break
		line = file.readline()

	# ignore line
	file.readline()

	# start reading the questions
	while(1):
		line = file.readline().strip().split(" ")
		if(line[0] == "END"):
			break

		ques = file.readline().strip()
		file.readline()
		option_list = []
		for i in range(4):
			options = file.readline().strip()
			if(options.split(" ")[0] == "Correct:"):
				solutions.append(chr(97 + i))
				options = ' '.join(map(str, options.split(" ")[1:])) 
			option_list.append(options)
		ques_str = ques + "\n a. "+option_list[0] + "\n b. "+option_list[1] + "\n c. "+option_list[2]+"\n d. "+option_list[3]
		questions.append(ques_str)

		# ignore line
		file.readline()
		
	print("[FILE IO] questions and solutions have been updated.")
	# print(questions)
	# print(solutions)
	

def main():
	questions = []
	solutions = []
	getQuestions(questions,solutions)

if __name__ == "__main__":
	main()
	