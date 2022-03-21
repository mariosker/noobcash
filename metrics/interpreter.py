# import os

# directory = os.path.join("c:\\", "path")
# for root, dirs, files in os.walk(directory):
#     for file in files:
#         if file.endswith(".log") or file.endswith(".txt"):
#             f = open(file, 'r')
#             for line in f:
#                 if userstring in line:
#                     print "file: " + os.path.join(root, file)
#                     break
#             f.close()
