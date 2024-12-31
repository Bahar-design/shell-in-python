import sys
import os
import subprocess
import shlex


def main():
    builtin = {"echo", "exit", "type", "pwd", "cd"}

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input()
        
        cmd_args = shlex.split(command)
        if not cmd_args:
            continue
        program = cmd_args[0]

        redirect_target = None
        redirect_index = None

        for i, arg in enumerate(cmd_args):
            if arg in {">", "1>"}:
                if i + 1 < len(cmd_args):
                    redirect_target = cmd_args[i + 1]
                    redirect_index = i
                else:
                    print("Error: Missing file target for redirection")
                    break
        
        if redirect_target:
            cmd_args = cmd_args[:redirect_index]

        if not cmd_args:
            print("Error: Missing command for redirection")
            continue

        if program == "exit" and len(cmd_args) > 1 and cmd_args[1] == "0":
            break

        elif command.startswith("echo "):
            output = " ".join(cmd_args[1:]) + "\n"
            if redirect_target: #put into it's own func
                with open(redirect_target, "w") as f:
                    f.write(output)
            else:
                print(output.strip())
            continue

        elif command.startswith("type ") and len(cmd_args) > 1:
            type = cmd_args[1]

            if type in builtin:
                output = f"{type} is a shell builtin\n"
            else:
                path_dir = os.environ.get("PATH", "").split(":")
                found = False
                for directory in path_dir:
                    potential_path = os.path.join(directory, type)
                    if os.path.isfile(potential_path) and os.access(potential_path, os.X_OK):
                        output = f"{type} is {potential_path}\n"
                        found = True
                        break
                if not found:
                    output = f"{type}: not found\n"

            if redirect_target:
                with open(redirect_target, "w") as f:
                    f.write(output)
            else:
                print(output.strip())
            continue

        elif program == "pwd":
            output = os.getcwd() + "\n"
            if redirect_target:
                with open(redirect_target, "w") as f:
                    f.write(output)
            else:
                print(output.strip())
            continue

        elif command.startswith("cd") and len(cmd_args) > 1:
            path = cmd_args[1]
            if path == "~":
                path = os.environ.get("HOME", "")

            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")
            continue

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

        with open(redirect_target, "w") if redirect_target else sys.stdout as f:
            subprocess.run([execute] + cmd_args[1:], stdout=f, stderr=sys.stderr)

if __name__ == "__main__":
    main()
