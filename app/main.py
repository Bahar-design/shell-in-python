import sys
import os
import subprocess
import shlex


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input()

        cmd_args = shlex.split(command)

        if command == "exit 0":
            break

        elif command.startswith("echo "):
            print(" ".join(cmd_args[1:]))
            continue

        elif command.startswith("type "):
            type = command[5:]
            builtin = {"echo", "exit", "type", "pwd", "cd"}

            if type in builtin:
                print(f"{type} is a shell builtin")
                continue

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
            continue

        elif command == "pwd":
            print(os.getcwd())
            continue

        elif command.startswith("cd"):
            path = command[3:].strip()
            if path == "~":
                path = os.environ.get("HOME", "")

            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")
            continue

        
        cmd_args = command.split()
        program = cmd_args[0]

        path_dir = os.environ.get("PATH", "").split(":")
        execute = None
        for directory in path_dir:
            potential_path = os.path.join(directory, program)
            if os.path.isfile(potential_path) and os.access(potential_path, os.X_OK):
                execute = potential_path
                break

        if not execute:
            print(f"{program}: command not found")
            continue

        subprocess.run([execute] + cmd_args[1:])

if __name__ == "__main__":
    main()
