from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def run_command(name,command):
    print(f"\n=={name}==")
    
    result  = subprocess.run(command, cwd=PROJECT_ROOT)

    return result.returncode == 0


if run_command("Unit tests", ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]):
    print("Tests passed.")
else:
    print("Tests failed.")
    raise SystemExit(1)

if run_command("docker build",["docker","build","--tag","konflux-poc:0.1","."]):
    print("Docker build successful.")
else:
    print("Docker build failed.")
    raise SystemExit(1)
