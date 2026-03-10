import argparse
from ini_handler import IniHandler

def main():
    parser = argparse.ArgumentParser(description="INI file editor")

    parser.add_argument("file", help="INI file path")
    parser.add_argument("--get", nargs=2, metavar=("SECTION", "KEY"))
    parser.add_argument("--set", nargs=3, metavar=("SECTION", "KEY", "VALUE"))

    args = parser.parse_args()

    ini = IniHandler(args.file)

    if args.get:
        section, key = args.get
        value = ini.get(section, key)
        print(value)

    elif args.set:
        section, key, value = args.set
        ini.set(section, key, value)
        ini.save()
        print("Value updated")

if __name__ == "__main__":
    main()
