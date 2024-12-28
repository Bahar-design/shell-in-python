import sys


def main():
    #Uncomment this block to pass the first stage
    sys.stdout.write("$ ")
    valid_command = []

    #Wait for user input
    command = input()
    while True:
        if command not in valid_command:
            print(f"{command}: command not found")

            continue


if __name__ == "__main__":
    main()
