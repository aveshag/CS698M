
# extracting APIs and Sections used in PE structure files

from collections import Counter 

# filename_list = glob.glob('train/Malware/*/')[:100]
path_benign = "train/Benign/"
path_malware = "train/Malware/"

benign_files = [file for file in listdir(path_benign)]
malware_files = [file for file in listdir(path_malware)]

print(len(benign_files))
print(len(malware_files))



sections = {}
api = {}
count = 0
for j, b_file in enumerate(malware_files):
    count += 1
    print(count)
#     if count == 200:
#         break
#     print(b_file)
    f1 = open(path_malware + b_file + "/Structure_Info.txt", 'r')
    
    try:
        lines = f1.readlines()
    except:
        continue
    
    i = 0
    
    while i < len(lines):

        if lines[i].find("[IMAGE_SECTION_HEADER]") != -1:
            i += 1
            name = lines[i].split()
            if len(name) > 3:
                nname = name[3]
                if nname in sections.keys():
                    sections[nname] += 1
                else:
                    sections[nname] = 1
                
        elif lines[i].find(".dll.") != -1:
            cols = lines[i].split()
            dll = cols[0]
            if dll in api.keys():
                api[dll] += 1
            else:
                api[dll] = 1

        i += 1

    f1.close()
    
# print(sections)
# print(api)

sec_high = Counter(sections) 
high1 = sec_high.most_common(500)

f = open("sect_mal.txt",'w')
for i in high1:
    f.write(i[0] + "\n")
f.close()

api_high = Counter(api) 
high2 = api_high.most_common(500)
f2 = open("apis_mal.txt",'w')

for i in high2:
    f2.write(i[0] + "\n")
f2.close()

print(count)
 
  
  
