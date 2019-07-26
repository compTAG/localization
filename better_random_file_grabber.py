import os, random

# Takes in a directory, & returns a random file in that directory (Sub directories not included)

#This one generates numbers sudo randomly, but is memory efficient.
def get_random_file1(dir, file_type):
      
  iter = 0
  random.seed();
  for root, dirs, files in os.walk(dir):
    for name in files:
      if name.endswith(file_type):
        iter = iter + 1
        if random.uniform(0, iter) < 1:
          print(name)
  print("No valid file found in directory:", dir)
  
# print(get_random_file('/home/geoengel/Documents/Undergraduate Research/localization/cell_collection/small_700_2019-07-25', '.json'))

# This one generates better random numbers, however probably loads more values into memory

def get_random_file2(dir, file_type):
      files = []
      for file in os.listdir(dir):
            if file.endswith(file_type):
                files.append(file)
              
      file_count = len(files)
      
      if len(files) < 1:
            print("No valid files of type:",file_type,", in directory:",dir)
      else:
            return random.choice(files)
          
print(get_random_file2('/home/geoengel/Documents/Undergraduate Research/localization/cell_collection/small_7000_2019-07-25', 'json'))