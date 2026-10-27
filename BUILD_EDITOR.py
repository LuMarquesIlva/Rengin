#!.venv/bin/python
import subprocess

RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

SETTINGSLIST = [
    ["builddir", 'EDITOR'],
    ["reconf", False],
    ["wipe", False],
    ["download", True]
]

def run_meson_build(build_dir=SETTINGSLIST[0]):
    # 1. Configure the build (equivalent to 'meson setup build')
    # Note: Replace 'meson' with 'python -m mesonbuild.mesonmain' if meson is not in PATH

    # builddir [0][1]
    # reconf [1][1]
    # wipe [2][1]
    # download [3][1]

    print(f"""[]--------Settings--------[]\n
      {SETTINGSLIST[0][0]} : {SETTINGSLIST[0][1]}
      {SETTINGSLIST[1][0]} : {SETTINGSLIST[1][1]}
      {SETTINGSLIST[2][0]} : {SETTINGSLIST[2][1]}
      {SETTINGSLIST[3][0]} : {SETTINGSLIST[3][1]}""")

    if SETTINGSLIST[3][1] is True:
        try:
            preSetup_cmd = ['meson', 'subprojects', 'download']
            print(f"\nRunning: {' '.join(preSetup_cmd)}\n")
            subprocess.run(preSetup_cmd, check=True)
        finally:
            print(f"\n{GREEN}-- Subprojects Downloaded --{RESET}\n")

    if SETTINGSLIST[1][1] is False and SETTINGSLIST[2][1] is False:
        try:
            setup_cmd = ['meson', 'setup', SETTINGSLIST[0][1]]
            print(f"\nRunning: {RED}{' '.join(setup_cmd)}{RESET}\n")
            subprocess.run(setup_cmd, check=True)
        finally:
            print(f"\n{GREEN}-- Project Configured --{RESET}")
    elif SETTINGSLIST[1][1] is True:
        try:
            setup_cmd = ['meson', 'setup', '--reconfigure', SETTINGSLIST[0][1]]
            print(f"\nRunning: {RED}{' '.join(setup_cmd)}{RESET}\n")
            subprocess.run(setup_cmd, check=True)
        finally:
            print(f"\n{GREEN}-- Project Configured --{RESET}")
    elif SETTINGSLIST[2][1] is True:
        try:
            setup_cmd = ['meson', 'setup', '--wipe', SETTINGSLIST[0][1]]
            print(f"\nRunning: {GREEN}{' '.join(setup_cmd)}{RESET}\n")
            subprocess.run(setup_cmd, check=True)
        finally:
            print(f"\n{GREEN}-- Project Configured --{RESET}")
    else:
        raise RuntimeError("-- Uncheck either <reconf> or <wipe> to proceed --")

    # 2. Build the project (equivalent to 'ninja -C build' or 'meson compile -C build')
    try:
        compile_cmd = ['meson', 'compile', '-C', SETTINGSLIST[0][1]]
        print(f"\nRunning: {RED}{' '.join(compile_cmd)}{RESET}\n")
        subprocess.run(compile_cmd, check=True)
    except RuntimeError:
        raise RuntimeError(f"Something Went Wrong During Compiling!")


if __name__ == "__main__":
    run_meson_build()