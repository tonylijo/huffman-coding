code_dict = {}
def frequncy(string):
	freq_dict = {}
	for i in string:
		if i in freq_dict.keys():
			freq_dict[i] = freq_dict[i] + 1
		else:
			freq_dict[i] = 1
	freq_list = freq_dict.items()
	freq_list = sorted(freq_list,key=lambda x:x[-1])
	return freq_list
def build_tree(freq_list):
	if freq_list.__len__() > 1:
		new_list = [((freq_list[0],freq_list[1]),freq_list[0][1] + freq_list[1][1])] + freq_list[2:]
		new_list = sorted(new_list,key=lambda x:x[-1])
	if new_list.__len__() > 1:
		prev = build_tree(new_list)
		return prev
	else:
		return new_list[0]
def trim(tuple_tree):
	if type(tuple_tree[0]) == type(""):
		return tuple_tree[0]
	else:
		return (trim(tuple_tree[0][0]),trim(tuple_tree[0][1]))
def give_codes(tuple_tree,path=""):
	global code_dict
	if type(tuple_tree) == type(""):
		code_dict[tuple_tree] = path
	else:
		give_codes(tuple_tree[0],path+'0')
		give_codes(tuple_tree[1],path+'1')
encodelist = []
bitcount = 0	
def new_encode(string):
	output = ''
	global bitcount
	global encodelist
	global code_dict
	for i in string:
		for j in code_dict[i]:
			if (bitcount % 8) == 0:
				newbyte = 0
				newbyte = newbyte | (int(j) << 7)
				#print chr(newbyte)
				encodelist.append(chr(newbyte))
				bitcount = bitcount + 1
			else:
				newbyte = encodelist[-1]
				newbyte = chr((ord(newbyte) | (int(j) << (7 - (bitcount % 8)))))
				#print newbyte
				encodelist[-1] = newbyte
				bitcount = bitcount + 1
	str = ''
	for i in encodelist:
		str = str + i
	#print str
	return str
def decode_new(string,tree):
	output = '' 
	new_tree = tree
	for i in string:
		count = 0
		while True:
			if ((ord(i) & (1 << (7-count))) >> (7 - count) == 0):
				new_tree = new_tree[0]
			        count = count + 1
			else:
				count = count + 1
			        new_tree = new_tree[1]
			if type(new_tree) == type(""):
				output = output + new_tree
			        new_tree = tree
			if count % 8 == 0:
				count = 0
				break
	return output
def main():
	global code_dict
	f1 = open('ne.py','r')
	input_str = f1.read()
	freq_list = frequncy(input_str)
	tuple_tree = build_tree(freq_list)
	new_tuple_tree = trim(tuple_tree)
	give_codes(new_tuple_tree)
	#print code_dict.items()
	k = []
	for i in input_str:
		k.append(i)
	#print k
	output = new_encode(input_str)
	f2 = open('new','w')
	f2.write(output)
	f2.close()
	f2 = open('new','r')
	input_str = f2.read()
	output = decode_new(input_str,new_tuple_tree)
	f2.close()
	f3 = open('new_out','w')
	f3.write(output)
	f3.close()
if __name__ == "__main__":
	main()
