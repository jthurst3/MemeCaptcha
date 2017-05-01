import csv
import os
import sys
csv.field_size_limit(sys.maxsize)

folder = "/public/jthurst3/MemeCaptcha/data"

images = ""
imageList = []
# print(os.listdir(folder))

for filename in os.listdir(folder):
    filename = folder + "/" + filename
    with open(filename,'rb') as read:
        row = csv.reader(read, delimiter='\t')
        for rows in row:
            if "i do push ups" in rows:
                print (rows)
            # if(len(rows)>0):
#                 image = rows[0].split('/')[-1]
#                 print(image)
#                 imageList.append(image)
#                      # if(row[0] not in imageList)
#
# print(imageList[0])

# row = imageList[0][0].split('/')[-1]
#
# print(row)

