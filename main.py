# Student ID: 012397081
# Gabriel Nevarez
# C950

from Menu import Menu


def main():
    """
    Main entry point for the WGUPS routing program.

    Creates the Menu object and repeatedly displays
    the user interface until the user chooses to exit.
    """

    # Creating the Menu object loads the package,
    # location, and distance data and runs the
    # delivery routing simulation.
    menu = Menu()

    running = True

    # Continue displaying the menu until getOption()
    # returns False when the user selects Exit.
    while running:
        menu.display()

        choice = input(
            "Select an option: "
        )

        running = menu.getOption(
            choice
        )


# Start the program only when this file
# is executed directly.
if __name__ == "__main__":
    main()