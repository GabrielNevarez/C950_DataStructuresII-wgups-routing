# Student ID: 012397081
# Gabriel Nevarez
# C950

from Menu import Menu


def main():
    menu = Menu()
    running = True

    while running:
        menu.display()
        choice = input("Select an option: ")
        running = menu.get_option(choice)


if __name__ == "__main__":
    main()