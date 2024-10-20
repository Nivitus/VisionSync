import subprocess
import time
import os
import sys

def run_server(command, cwd):
    return subprocess.Popen(command, cwd=cwd, shell=True)

def main():
    if sys.version_info < (3, 6):
        print("Warning: You are using Python {}.{}. Some features may not work correctly.".format(
            sys.version_info.major, sys.version_info.minor))
        print("It is recommended to use Python 3.6 or higher.")

    project_root = os.path.dirname(os.path.abspath(__file__))
    ai_backend_dir = os.path.join(project_root, 'ai_backend')
    ui_backend_dir = os.path.join(project_root, 'ui_backend')

    print("Starting AI backend server...")
    ai_server = run_server("python app.py", ai_backend_dir)
    time.sleep(5) 

    print("Starting UI backend server...")
    ui_server = run_server("python app.py", ui_backend_dir)

    print("\nBoth servers are now running.")
    print("Start the service: http://localhost:5001")
    print("\nPress Ctrl+C to stop both servers.")

    try:
        ai_server.wait()
        ui_server.wait()
    except KeyboardInterrupt:
        print("\nStopping servers...")
        ai_server.terminate()
        ui_server.terminate()
        print("Servers stopped.")

if __name__ == "__main__":
    main()
