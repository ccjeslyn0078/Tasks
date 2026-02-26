def create(file_name):
    with open(file_name, "x") as f:
        pass 
    print("File created successfully!")

def write(file_name, data):
    with open(file_name, "w") as f:
        f.write(data + "\n")
        print("Written to a file!")

def read(file_name):
    with open(file_name, "r") as f:
        print("\n File content")
        print(f.read())

def append(file_name, data):
    with open(file_name, "a") as f:
        f.write(data + "\n")
    
    with open(file_name, "r") as f:
        print("\n File content")
        print(f.read())

def modify(file_name, data):
    with open(file_name) as f:
        lines = f.readlines()
        lines[-1] = data + "\n"

    with open(file_name, "w") as f:
        f.writelines(lines)
    
    with open(file_name, "r") as f:
        print("File content")
        print(f.read())
        


def main():
    print("File Handling Operations")
    file_name = input("enter a file name that you want to create")

    while True:
        choice = int(input("""
            1. Create File
            2. Write to a File
            3. Read a file 
            4. Append to a file 
            5. Modify last line 
            6. exit   
        """))

        if(choice == 1):
            create(file_name)
            
        elif(choice == 2):
            data = input("enter data to write: \n")
            write(file_name, data)

        elif(choice == 3):
            read(file_name)

        elif(choice == 4):
            data = input("enter data to append: \n")
            append(file_name, data)

        elif(choice == 5):
            data = input("enter data to modify: \n")
            modify(file_name, data)
        
        elif(choice == 6):
            exit()

if __name__ == "__main__":
    main()
