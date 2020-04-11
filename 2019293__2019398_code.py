'''

Computer Organization Project-1



Group Member 1:

AJAY KUMAR

2019293

VIKRANT

2019






'''

import datetime

'''

	RETURN TYPE- String

	This function returns an opcode string for the respective instructions.

	It searches the string contents in a dictionary first which contains instructions as keys and their

	opcode as values and then returns if  it is there in desireable opcode string .



	'''

def OpFromLine(line):
	global OpCodes
	s=line.split()
	for i in s:
		if(i in OpCodes.keys()):
			return OpCodes[i]
	'''
	RETURN TYPE- integer
	This function returns the binary value of a number when it is called in a eight   bit format .
	'''	
def Bin8(x):
	a=x
	r=''
	while(a>0):
		r=str(a%2)+r
		a=int(a/2)
	r='0'*(8-len(r))+r
	return r
'''
	RETURN TYPE- void
	This function first reads the file input.txt and iterate over its lines. Through iterating it checks for various errors and reports
	it as soon as its caught. 
	'''

def GenSymTable():									#first pass
	global SymDict,NoLines,NoVars,OpCodes
	ReadFromFile=open("input.txt","r")				#open the file
	AddressPointer=0								#A counter that shows the address where the current instruction has to be written
	lines=list(ReadFromFile.readlines())			#reading the file content line by line
	CLine=0											# A counter that shows no. of lines in a instruction set
	for i in lines:
		CLine+=1
		if(i.find('//')>=0):
			i=i[:i.find('//')]						#looking for commented line
		if(i[-1]=='\n'):
			i=i[::-1]
			i=i[1:]
			i=i[::-1]
		if(len(list(i.split()))==0):				# checking if the length of list is 0 or not
			continue
		else:
			if(i=='STP'):							#Stop the process if it contains STP
				AddressPointer+=1
				continue
			temp=i.split()
			n=0
			for j in temp:							# count no. of opcodes in a temp  
				if(j in OpCodes.keys()):
					n+=1
			if(n==0):								# if no instructions are given in a line
				print("ERROR on Line "+str(CLine)+": No instruction given in this line.")
				print('\t'+i)
				print('\t^')
				return True
			elif(n>1):								# if no of instructions greater than 1
				print("ERROR on Line "+str(CLine)+": Multiple Instructions given in a line.")
				print('\t'+i)
				print('\t^')
				return True
			if(len(temp)==1):						# only stp and cla is called without any operand
				if(temp[0]!='CLA' and temp[0]!='STP'):
					print("ERROR on Line "+str(CLine)+": Insufficient variable/label provided.")
					print('\t'+i)
					print('\t^')
					return True
			elif(len(temp)==2):						
				if((temp[0] in OpCodes.keys())==False and (temp[1] in OpCodes.keys())==True and temp[1]!='CLA' and temp[1]!='STP'):
					print("ERROR on Line "+str(CLine)+": Formatting Error.")
					print('\t'+i)
					print('\t^')
					return True
			for k in range(len(temp)):
				if(temp[k] in OpCodes.keys()):
					if(len(temp)-k-1>1):					 # If more  variables are provided in the instructions
						print("ERROR on Line "+str(CLine)+": More than one variable/label provided.")
						print('\t'+i)
						print('\t^')
						return True
			if(len(temp)>=3):
				if((temp[0] in OpCodes.keys())==False and (temp[1] in OpCodes.keys())==False):
					print("ERROR on Line "+str(CLine)+": Formatting Error.")
					print('\t'+i)
					print('\t^')
					return True
			if(':' in i):									# it means label is  defined in the given instruction
				sym=i[:i.index(':')]
				sym=sym.strip()
				if(sym in OpCodes.keys()):
					print("ERROR on Line "+str(CLine)+": instructions name can not be an instruction.")
					print('\t'+i)
					print('\t^')
					return True
				if(sym in SymDict):
					if(SymDict[sym]==-1):
						print("ERROR on Line "+str(CLine)+": Variable with same name is already declared.")
						print('\t'+i)
						print('\t^')
						return True
					elif(SymDict[sym]!=-2):
						print("ERROR on Line "+str(CLine)+": Label is already declared with same name.")
						print('\t'+i) 
						print('\t^')
						return True
				if('STP' in i):
					SymDict[sym]=AddressPointer					#Giving address ptr value to the label just before 'STP'
					AddressPointer+=1
					continue
				i=i[i.index(':')+1:]
				SymDict[sym]=AddressPointer						#Giving address ptr value to the label
			elif(('BRZ' in i) or ('BRP' in i) or ('BRN' in i)):
				sym=temp[1]
				if(sym in OpCodes.keys()):
					print("ERROR on Line "+str(CLine)+": label name can not be an instruction.")
					print('\t'+i)
					print('\t^')
					return True
				if(sym in SymDict):					# for example BRN S where S is variable
					if(SymDict[sym]==-1):
						print("ERROR on Line "+str(CLine)+": Cannot branch to a variable.")
						print('\t'+i)
						print('\t^')
						return True
					else:
						AddressPointer+=1						#Simply increment address pointer value as label has already been declared before
						continue
				else:
					SymDict[sym]=-2
			elif(('INP' in i) or ('LAC' in i) or ('SAC' in i)):
				if(temp[1] in OpCodes.keys()):
					print("ERROR on Line "+str(CLine)+": instructions name can not be an instruction.")				# EXAMPLE INP SAC
					print('\t'+i)
					print('\t^')
					return True
				elif(temp[1] in SymDict):
					if(SymDict[temp[1]]!=-1):
						print("ERROR on Line "+str(CLine)+": "+temp[1]+" is a label type instructions.")
						print('\t'+i)
						print('\t^')
						return True
				SymDict[temp[1]]=-1	
			AddressPointer+=1									#Increment in address ptr value
		NoLines=AddressPointer
	ss=list(SymDict.keys())
	for i in ss:												#CHECKING WHETHER FORWARD REFRENCING HAPPEN 
		if(SymDict[i]==-1):
			NoVars+=1
			SymDict[i]=AddressPointer							#Give address pointer value to the literal
			AddressPointer+=1									#Increment address pointer value
		elif(SymDict[i]==-2):
			print("ERROR: Label "+i+" not defined.")
			return True
	NoLines=AddressPointer-NoVars
	if(NoLines+NoVars>256):											# Can only store upto 255 addresses
		print("ERROR: Address Overflow due to more number of instructions and variables(MEMORY LIMIT: 0-255).")
		return True
	return False
	""" 
	Return type - void 
	if no error is caught then only it will run . this function makes a new file Machinecode.txt , LiteralTable.txt and LabelTable.txt which stores
	the correct  machine code for the  given assembly code . it also converts instructions to opcode and integr addresses  to their binary equivalents 
	and then write it to the files 
	"""



def GenMachCode():
	global SymDict,NoLines,NoVars,OpCodes
	for i in SymDict.keys():
		x=SymDict[i]
		binary=Bin8(x)						#converting addresses to their binary equivalent from a pre defined function
		SymDict[i]=binary
	WriteInFile=open("MachineCode.txt","w")		#open a new file in write mode
	ReadFromFile=open("input.txt","r")			#reading lines (second pass) for writing the machine code
	lines=list(ReadFromFile.readlines())
	for i in lines:
		if('\n' in i):
			i=i[::-1]
			i=i[1:]
			i=i[::-1]
		if('//' in i):							#if commented then  please skip it
			i=i[:i.find('//')]
		if(i.find(':')!=-1):
			i=i[i.find(':')+1:]
		s=i.split()
		if(len(s)==0):
			continue
		if(len(s)==1):
			WriteInFile.write(OpFromLine(s[0])+" "+"00000000"+"\n")		# if an line does not  have any symbol or attributes  attached it will add 8 0s in front
		else:
			WriteInFile.write(OpFromLine(s[0])+" "+SymDict[s[1]]+"\n")		#concatenat opcode and address together and then adding it to file
	WriteInFile.close()
	WriteInFile1=open("LiteralTable.txt",'w')					#It makes a file for storing all the info of literals used in code
	WriteInFile2=open("LabelTable.txt",'w')						# #It makes a file for storing all the info of labels used in code
	WriteInFile1.write("LITERAL\t\tLOCATION\n")
	WriteInFile2.write("LABEL\t\tLOCATION\n")
	for i in SymDict.keys():
		if(int(SymDict[i],2)<NoLines):
			WriteInFile2.write(str(i)+'\t\t'+SymDict[i]+'\n')
		else:
			WriteInFile1.write(str(i)+'\t\t'+SymDict[i]+'\n')
	WriteInFile1.close()
	WriteInFile2.close()
t1=datetime.datetime.now()
SymDict={}
NoLines=0
NoVars=0
OpCodes={}
ReadFromFile=open("opcodes.txt","r")
Ops=list(ReadFromFile.readlines())
for i in Ops:
	i=i.split()
	OpCodes[i[0]]=i[1]
if(GenSymTable()==False):
	GenMachCode()
	t2=datetime.datetime.now()
	print('Program successfully assembled\nAssembly time:')
else:
	t2=datetime.datetime.now()
	print('Exited program midway\nRuntime:')
t=str(t2-t1)
t=t[::-1]
t=t[:t.find(':')]
t=t[::-1]
print(t+'s')