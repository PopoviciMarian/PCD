import os
#generate a file of 200MB 

def generate_file(file_name, size):
    with open(file_name, 'wb') as file:
        file.write(os.urandom(size))

if __name__ == '__main__':
    generate_file("200MB.txt", 500 * 1024 * 1024) # 200MB
    