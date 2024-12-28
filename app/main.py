import sys


def main():
    #Uncomment this block to pass the first stage
    valid_command = []

    #Wait for user input
    while True:
        command = input()
        sys.stdout.write("$ ")
        sys.stdout.flush()

        if command not in valid_command:
            print(f"{command}: command not found")
            continue


if __name__ == "__main__":
    main()
