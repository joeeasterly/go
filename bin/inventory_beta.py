import os
import curses

from create_record import create_record
from search_records import search_records
from update_record import update_record
from update_consumable import update_consumable
from delete_record import delete_record

def centered_string(s, total_width):
    """Return a centered string based on the given width."""
    total_spaces = total_width - len(s)
    left_spaces = total_spaces // 2
    right_spaces = total_spaces - left_spaces  # This accounts for any odd space
    return ' ' * left_spaces + s + ' ' * right_spaces

def main(stdscr):
    # Create windows for each area
    header_win = curses.newwin(4, curses.COLS, 0, 0)

    # Calculate the height for display_win
    display_height = curses.LINES - 5  # Subtracting height of header_win and input_win and one extra line for spacing
    display_win = curses.newwin(display_height, curses.COLS, 4, 0)

    # Position the input window on the second to last line
    input_win = curses.newwin(1, curses.COLS, curses.LINES - 2, 0)

    more_menu = False

    def draw_banner(win):
        banner_title = 'Inventory Management System'
        banner_width = curses.COLS - 2  # Minus 2 for the '#' on each side
        centered_banner = centered_string(banner_title, banner_width)
        win.addstr(0, 0, '#' * curses.COLS)
        win.addstr(1, 0, '#' + centered_banner + '#')
        win.addstr(2, 0, '#' * curses.COLS)
        win.refresh()

    def draw_menu_one(win):
        win.addstr(3, 0, '1) Create  2) Search 3) Update 4) Count 5) More  ')
        win.refresh()

    def draw_menu_two(win):
        win.addstr(3, 0, '6) Update Github 7) Exit 8) Back               ')
        win.refresh()

    while True:
        try:
            # Ensure cursor is visible
            curses.curs_set(1)

            # Clear each window
            header_win.clear()
            display_win.clear()
            input_win.clear()

            # Draw the main menu
            draw_banner(header_win)
            if not more_menu:
                draw_menu_one(header_win)
            else:
                draw_menu_two(header_win)

            # Prompt the user in the input window
            prompt = "Enter your choice: "
            input_win.addstr(0, 0, prompt)
            input_win.move(0, len(prompt))  # Move the cursor to the end of the prompt

            # Get user input
            choice = input_win.getstr().decode('utf-8')  # getstr() returns bytes, so decode it

            if choice == '1':
                create_record()
            elif choice == '2':
                search_records()
            elif choice == '3':
                update_record()
            elif choice == '4':
                update_consumable()
            elif choice == '5' and not more_menu:
                more_menu = True
                continue
            elif choice == '6':
                os.system("python3 /usr/local/gh/go/bin/update_github.py")
            if choice == '7':
                display_win.addstr(5, 0, 'Goodbye!')  # Display the message in the display_win
                display_win.refresh()
                break
            elif choice == '8' and more_menu:
                more_menu = False
                continue
            else:
                display_win.addstr(5, 0, 'Invalid choice. Please select a valid option.')  # Display the error in the display_win
                display_win.refresh()
        except KeyboardInterrupt:
            # Handle Ctrl+C to gracefully exit
            break

if __name__ == "__main__":
    curses.wrapper(main)