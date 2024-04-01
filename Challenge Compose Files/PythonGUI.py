import curses
import os

def get_compose_files():
    compose_files = []
    for file_name in os.listdir("."):
        if file_name.endswith(".yaml") or file_name.endswith(".yml"):
            compose_files.append(file_name)
    return compose_files

def get_label_from_file(file_name):
    with open(f"{file_name}", "r") as file:
        first_line = file.readline().strip()
        if first_line.startswith("#"):
            return first_line[1:].strip()
    return None

def print_menu(stdscr, selected_row_idx, compose_files):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    for idx, file_name in enumerate(compose_files):
        x = w//2 - len(file_name)//2
        y = h//2 - len(compose_files)//2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, file_name)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, file_name)
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    compose_files = get_compose_files()
    if not compose_files:
        stdscr.addstr(0, 0, "No Docker Compose files found in 'Challenge Compose Files' directory.")
        stdscr.refresh()
        stdscr.getch()
        return
    current_row_idx = 0
    print_menu(stdscr, current_row_idx, compose_files)
    while True:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(compose_files) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            selected_file = compose_files[current_row_idx]
            selected_label = get_label_from_file(selected_file)
            if selected_label:
                stdscr.addstr(0, 0, f"Selected: {selected_label}. Running docker-compose...")
                stdscr.refresh()
                os.system(f"docker compose -f '{selected_file}' up -d > docker-compose.log 2>&1")
                print(f"docker compose -f '{selected_file}' up -d > docker-compose.log 2>&1")
                os.system(f"docker compose -f '{selected_file}' exec kali /bin/bash")
                break
            else:
                stdscr.addstr(0, 0, "Error: No label found for selected file.")
                stdscr.refresh()
                stdscr.getch()
        print_menu(stdscr, current_row_idx, compose_files)

if __name__ == "__main__":
    curses.wrapper(main)
