import os
import subprocess
import difflib
import time

# Change the arguments as needed
path = "-p ./public"
delay = "-d 0"
threads = "-t 5"
max_proc = "-m 20"

def execute_program(path, delay, threads, max_proc):
    command = f"./ems {path} {delay} {threads} {max_proc}"
    print(f"Executing: {command}")
    try:
        start_time = time.time()
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
        exec_time = time.time() - start_time
        return exec_time
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        diff = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file1, tofile=file2)
        diff = ''.join(diff)
        if diff:
            print(f"\033[1mTesting {f1} \033[0m")
            for line in diff.splitlines():
                if line.startswith(' '):
                    print(line)
                elif line.startswith('-'):
                    if (len(line.split('+'))==2):
                        print('\033[91m' + line.split('+')[0] + '\033[0m')  # Red for wrong lines
                        print('\033[92m+' + line.split('+')[1] + '\033[0m')  # Green for correct lines
                    else:
                        print('\033[91m' + line + '\033[0m')  # Red for wrong lines
                elif line.startswith('+'):
                    print('\033[92m' + line + '\033[0m')  # Green for correct lines

            return False
        else:
            return True
        

def process_files():
    rpath = path.split(' ')[1]
    files = os.listdir(rpath)
    passed = 0
    total = 0
    color = '\033[93m'
    
    for file in files:
        if file.endswith(".out"):
            total += 1
            try:
                if compare_files(f"{rpath}/{file}", f"{rpath}/{file.replace('.out', '.result')}"):
                    passed += 1
                else: print("\n")
            except FileNotFoundError as e: print(f"Error: {e}")
            print("\n")
    if passed == total:
        color = '\033[92m'
    elif passed == 0:
        color = '\033[91m'
    print(f"\033[1m{color}Passed: {passed}/{total} \033[0m")

def main():
    time = execute_program(path, delay, threads, max_proc)
    process_files()
    print(f"Execution time: {time:.2f}s")

if __name__ == "__main__":
    main()