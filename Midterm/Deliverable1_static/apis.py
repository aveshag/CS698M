

# check most frequent APIs among malware and Benign files given

mal = set()
bgn = set()

f = open("apis_mal.txt",'r')
lines = f.readlines()
for i in lines:
    i = i.replace("\n", "") 
    mal.add(i)
f.close()

f = open("apis_ben.txt",'r')
lines = f.readlines()
for i in lines:
    i = i.replace("\n", "")   
    bgn.add(i)
f.close()

print(mal)
print(bgn)
print()
print(mal.intersection(bgn))
print()
print(mal.difference(bgn))
print()
print(bgn.difference(mal))


