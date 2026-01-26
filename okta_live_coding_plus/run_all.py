# This script simply runs the demo sections of all problem files.
import subprocess, sys, os, glob

def main():
    base = os.path.dirname(__file__)
    files = sorted(glob.glob(os.path.join(base, "problems", "*.py")))
    for f in files:
        print("\n" + "="*80)
        print("Running:", os.path.basename(f))
        print("="*80 + "\n")
        # Use the current Python executable to run each file
        result = subprocess.run([sys.executable, f], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

if __name__ == "__main__":
    main()
