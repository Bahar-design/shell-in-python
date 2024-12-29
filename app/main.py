import sys


def main():
    try:

        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()

            command = input()

            if command == "exit 0":
                break

            if command.startswith("echo "):
                print(command[5:])

            print(f"{command}: command not found")
    except EOFError:
        sys.exit(0)


if __name__ == "__main__":
    main()
