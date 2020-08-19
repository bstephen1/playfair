from copy import deepcopy

	
#global constants 
#character to use for double letters
repeatChar = "X"
#size of matrix (6x6)
size = 6
#alphabet (includes numbers)
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
#amount of letters in a block (formatting)
block = 5
#blocks per line (formatting)
bpl = 15


#converts the message to form readable by the cipher
def getRawMessage(aMessage, encipher) :

	aMessage = aMessage.replace(" ", "")
	aMessage = aMessage.upper()	
	rawList = list(aMessage)

	#add value to repeating characters (encipher only)
	if encipher :
		x = 0
		while x < len(rawList) - 1 :
			#ignore newlines
			if rawList[x] == "\r" or rawList[x] == "\n" :
				rawList[x] = ""
			if not x % 2 and rawList[x] == rawList[x + 1]	:
				rawList.insert(x + 1, repeatChar)
			x += 1
	
		#check for odd length (should only be for enciphering)
		if len(rawList) % 2 == 1 :
			rawList.append(repeatChar)
	
	#decipher -- remove newlines
	else :	
		x = 0
		while x < len(rawList) - 1 :
			#ignore newlines
			if rawList[x] == "\r" or rawList[x] == "\n" :
				rawList[x] = ""
			x += 1
	
	message = "".join(rawList)
	return message


#creates the matrix, using the key word, and filling in the rest of the alphabet
def createMatrix(key) :
	
	key = list(key)
	key.extend(list(alphabet))
	key = "".join(key)
	key = key.upper()
	key = removeDups(key)
	
	#dictionary for looking up the position of a letter
	matDict = {}
	col = 0
	for x in range(len(key)) :
		if x > 0 and x % size == 0 :
			col += 1
		matDict[key[x]] = [col, x % size]
		
	#list for looking up the letter at a position
	matList = []
	col = []
	for x in key :
		col.append(x)
		if len(col) == size :
			matList.append(deepcopy(col))
			col = []
	
	matrix = (matDict, matList)
	return(matrix)

#removes all the duplicate letters and numbers in a string
def removeDups(aString) :
	aString = aString.replace(" ", "")
	aString = list(aString)
	for x in range(len(aString) - 1) :
		y = x + 1
		while y < len(aString) : 
			if aString[x] == aString[y] :
				del aString[y]
				y -= 1
			y += 1
	aString = "".join(aString)
	return aString
	

#enciphers the message
def encipher(aMessage, aMatrix) :
	
	#the enciphered message
	newMes = []

	for x in range(0, len(aMessage), 2) :
		one = aMatrix[0][aMessage[x]]
		two = aMatrix[0][aMessage[x + 1]]
		
		#if rows are the same, increase col by 1 mod size (6)
		if one[0] == two[0] :
			newMes.append(aMatrix[1][one[0]][(one[1] + 1) % size])
			newMes.append(aMatrix[1][two[0]][(two[1] + 1) % size])
		
		#if cols are the same, increase row by 1 mod size (6)
		elif one[1] == two[1] :
			newMes.append(aMatrix[1][(one[0] + 1) % size][one[1]])
			newMes.append(aMatrix[1][(two[0] + 1) % size][two[1]])
		
		#else pick same row, swap columns
		else :
			newMes.append(aMatrix[1][one[0]][two[1]])
			newMes.append(aMatrix[1][two[0]][one[1]])
	
	return format(newMes)

	
#deciphers the message
def decipher(aMessage, aMatrix) :	
	
	#the deciphered message
	newMes = []

	for x in range(0, len(aMessage), 2) :
		one = aMatrix[0][aMessage[x]]
		two = aMatrix[0][aMessage[x + 1]]
		
		#if rows are the same, deccrease col by 1 mod size (6)
		if one[0] == two[0] :
			newMes.append(aMatrix[1][one[0]][(one[1] - 1) % size])
			newMes.append(aMatrix[1][two[0]][(two[1] - 1) % size])
		
		#if cols are the same, deccrease row by 1 mod size (6)
		elif one[1] == two[1] :
			newMes.append(aMatrix[1][(one[0] - 1) % size][one[1]])
			newMes.append(aMatrix[1][(two[0] - 1) % size][two[1]])
		
		#else pick same row, swap columns
		else :
			newMes.append(aMatrix[1][one[0]][two[1]])
			newMes.append(aMatrix[1][two[0]][one[1]])
	
	return format(newMes) 
	
	

#formats the string to be in blocks 
def format(s) :
	mes = []
	for x in range(len(s)) :
		if not (x % (bpl * block)) and x != 0 :
			mes.append("\n")
			mes.append(s[x])
		elif x % block or x == 0 :
			mes.append(s[x])
		else :
			mes.append(" ")
			mes.append(s[x])
			
	mes = "".join(mes)
	return mes
	
#main loop	
def main() :
	
	print "\nWelcome to Playfair cipher program.\n"
	aKey = raw_input("Enter a key: ")
	matrix = createMatrix(aKey)
	
	
	cont = True
	while cont :
		choice = int(raw_input("1 -- encipher\n2 -- decipher\n3 -- encipher from file\n4 -- decipher from file\n5 -- quit\n"))
		if choice == 1 :
			message = raw_input("Enter a message to encipher: ")
			message = getRawMessage(message, True)
			print "Enciphered message:" , encipher(message, matrix)
		elif choice == 2 :
			message = raw_input("Enter a message to decipher: ")
			message = getRawMessage(message, False)
			print "Deciphered message:" , decipher(message, matrix)
		elif choice == 3 :
			print "Enciphering from \"encipher.txt\" to \"output.txt\"..."
			text = open("encipher.txt", "r")
			out = open("output.txt" , "w")
			message = getRawMessage(text.read(), True) 
			out.write(encipher(message, matrix))
			text.close()
			out.close()
		elif choice == 4 :
			print "Deciphering from \"decipher.txt\" to \"output.txt\"..."
			text = open("decipher.txt" , "r")
			out = open("output.txt" , "w")
			message = getRawMessage(text.read(), False)
			out.write(decipher(message, matrix))
			text.close()
			out.close()
		elif choice ==  5 :
			cont = False
		else :
			print "Invalid symbol."
	
	
main()
	