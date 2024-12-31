import sys
import os
import subprocess
import shlex

builtins = {"echo", "exit", "pwd", "cd", "type"}

def handle_redirection(cmd_args):
    """Parses & removes redirection operators from command."""
    redirect_target = None
    if ">" in cmd_args:
        try:
            index = cmd_args.index(">")
            if index + 1 < len(cmd_args):
                redirect_target = cmd_args[index + 1]
                cmd_args = cmd_args[:index]
            else:
                print("Error: Missing file target for redirection")
                return None, None
        except ValueError:
            pass

    if "1>" in cmd_args:
        try:
            index = cmd_args.index("1>")
            if index + 1 < len(cmd_args):
                redirect_target = cmd_args[index + 1]
                cmd_args = cmd_args[:index]
            else:
                print("Error: Missing file target for redirection")
                return None, None
        except ValueError:
            pass

    return cmd_args, redirect_target

def execute_external_command(cmd_args, redirect_target):
    """Execute external commands & handle redirection when necessary"""
    program = cmd_args[0]
    path_dirs = os.environ.get("PATH", "").split(":")
    executable = None

    for directory in path_dirs:
        potential_path = os.path.join(directory, program)
        if os.path.isfile(potential_path) and os.access(potential_path, os.X_OK):
            executable = potential_path
            break

    if not executable:
        print(f"{program}: command not found")
        return

    if redirect_target:
        with open(redirect_target, "w") if redirect_target else sys.stdout as f:
            subprocess.run(cmd_args, stdout=f, stderr=sys.stderr)
    else:
        subprocess.run(cmd_args, stdout=sys.stdout, stderr=sys.stderr)


def main():

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input().strip()
        if not command:
            continue
        
        try:
            cmd_args = shlex.split(command)
        except ValueError as err:
            print(f"Error parsing command: {err}")

        if not cmd_args:
            continue

        cmd_args, redirect_target = handle_redirection(cmd_args)
        if cmd_args is None:
            continue

        program = cmd_args[0]

        if program == "exit" and len(cmd_args) > 1 and cmd_args[1] == "0":
            break

        if program == "echo":
            output = " ".join(cmd_args[1:]) + "\n"
            if redirect_target:
                with open(redirect_target, "w") as f:
                    f.write(output)
            else:
                print(output.strip())
            continue

        if program == "pwd":
            output = os.getcwd() + "\n"
            if redirect_target:
                with open(redirect_target, "w") as f:
                    f.write(output)
            else:
                print(output.strip())
            continue

        if program == "cd":
            if len(cmd_args) == 1 or cmd_args[1] == "~":
                path = os.environ.get("HOME", "")
            else:
                path = cmd_args[1]

            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")
            continue

        if program == "type":
            if len(cmd_args) < 2:
                print("type: missing operand")
                continue

            cmd_name = cmd_args[1]
            if cmd_name in builtins:
                output = f"{cmd_name} is a shell builtin\n"
            else:
                path_dirs = os.environ.get("PATH", "").split(":")
                executable = None
                for directory in path_dirs:
                    potential_path = os.path.join(directory, cmd_name)
                    if os.path.isfile(potential_path) and os.access(potential_path, os.X_OK):
                        executable = potential_path
                        break

                if executable:
                    output = f"{cmd_name} is {executable}\n"
                else:
                    output = f"{cmd_name}: not found\n"

            if redirect_target:
                with open(redirect_target, "w") as f:
                    f.write(output)
            else:
                print(output.strip())
            continue

        execute_external_command(cmd_args, redirect_target)

if __name__ == "__main__":
    main()
