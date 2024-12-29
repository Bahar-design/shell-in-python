import sys


def main():
    try:
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()

            command = input()

            if command == "exit 0":
                break

            elif command.startswith("echo "):
                print(command[5:])

            elif command.startswith("type "):
                type = command[5:]
                builtin = {"echo", "exit", "type"}
                if type in builtin:
                    print(f"{type} is a shell builtin")
                else:
                    print(f"{type}: not found")

            else:
                print(f"{command}: command not found")
    except EOFError:
        sys.exit(0)


if __name__ == "__main__":
    main()
