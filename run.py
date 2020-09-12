import json
import argparse

from brainfuck import Machine

def name_resolution(path, commands, toBrain=True):
    with open(path, "r", encoding="utf-8") as f:
        nr = json.load(f)
    correspondence_table = {k: v["command"] for k, v in nr.items()}
    for k, v in correspondence_table.items():
        if toBrain:
            commands = commands.replace(v, k)
        else:
            commands = commands.replace(k, v)
    return commands

def main():
    parser = argparse.ArgumentParser(description="Brainfuck Compiler")
    parser.add_argument("-cmd", help="command line")
    parser.add_argument("-nrf", help="Name Resolution File Path")
    parser.add_argument("-f", help="Comand Line File Path")
    parser.add_argument("-N", help="Tape Length", default=30000, type=int)
    args = parser.parse_args()

    if (cmd_path := args.f) is None:
        command = args.command
    else:
        with open(cmd_path, "r", encoding="utf-8") as f:
            command = f.read()

    if (nrf := args.nrf) is not None:
        command = name_resolution(nrf, command)
    N = args.N
    machine = Machine(N=N, cmd_lst=command)
    while not machine.is_accept():
        machine()

if __name__ == "__main__":
    main()