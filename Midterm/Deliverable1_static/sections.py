
# find the most probable sections in PE structure file for both Malware and Benign

mal = set()
bgn = set()

f = open("sect_mal.txt",'r')
lines = f.readlines()
for i in lines:
    i = i.replace("\n", "") 
    mal.add(i)
f.close()

f = open("sect_ben.txt",'r')
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


