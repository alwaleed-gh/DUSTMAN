import sys
import os


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cleaner.useri import start_ui

def main():
    start_ui()

if __name__ == "__main__":
    main()