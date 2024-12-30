import sys
import os


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

                path_dir = os.environ.get("PATH", "").split(":")
                found = False
                for directory in path_dir:
                    potential_path = os.path.join(directory, type)
                    if os.path.isfile(potential_path) and os.access(potential_path, os.X_OK):
                        print(f"{type} is {potential_path}")
                        found = True
                        break

                if not found:
                    print(f"{type}: not found")

            else:
                print(f"{command}: command not found")
    except EOFError:
        sys.exit(0)


if __name__ == "__main__":
    main()
