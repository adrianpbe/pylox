import sys

from pylox.lox import Lox


def main():
    print(sys.argv)
    lox = Lox()
    if len(sys.argv) == 1:
        lox.run_prompt()
    elif  len(sys.argv) > 1:
        lox.run_file(sys.argv[1])


if __name__ == "__main__":
    main()
