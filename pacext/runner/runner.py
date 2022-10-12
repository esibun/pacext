import subprocess

def run_pacman(args):
    ex = ["pacman"] + args
    subprocess.run(ex)
