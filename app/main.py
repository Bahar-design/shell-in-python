import sys
import os
import subprocess
import shlex

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

        command = input()
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

        program = cmd_args

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

        if program == "cd" and len(cmd_args) > 1:
            path = cmd_args[1]
            if path == "~":
                path = os.environ.get("HOME", "")

            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: {path}: No such file or directory")
            continue

        execute_external_command(cmd_args, redirect_target)


        """for i, arg in enumerate(cmd_args):
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
        program = cmd_args[0]

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
    """

if __name__ == "__main__":
    main()
