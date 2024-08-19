from gui import create_gui
from database import init_db

def main():
    init_db()
    create_gui()

if __name__ == "__main__":
    main()
