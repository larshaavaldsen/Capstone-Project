import curses
import os
import webbrowser

documentation_link = "www.youtube.com"
scoring_link = "www.google.com"
#Start the webhook container
os.system(f"docker compose -f 'docker-compose-webhook-container.yaml' up -d > /dev/null 2>&1")

def get_compose_files():
    compose_files = []
    for file_name in os.listdir("Challenge Compose Files"):
        if file_name.endswith(".yaml") or file_name.endswith(".yml"):
            compose_files.append(file_name)
    return compose_files

def get_label_from_file(file_name):
    with open(f"Challenge Compose Files/{file_name}", "r") as file:
        first_line = file.readline().strip()
        if first_line.startswith("#"):
            return first_line[1:].strip()
    return None

def print_menu(stdscr, selected_row_idx, compose_files):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # ASCII Art Banner for "HACKER GAUNTLET"
    banner_lines = [
" █████   █████                    █████                              █████████                                   █████    ████            █████   ",
"░░███   ░░███                    ░░███                              ███░░░░░███                                 ░░███    ░░███           ░░███    ",
" ░███    ░███   ██████    ██████  ░███ █████  ██████  ████████     ███     ░░░   ██████   █████ ████ ████████   ███████   ░███   ██████  ███████  ",
" ░███████████  ░░░░░███  ███░░███ ░███░░███  ███░░███░░███░░███   ░███          ░░░░░███ ░░███ ░███ ░░███░░███ ░░░███░    ░███  ███░░███░░░███░   ",
" ░███░░░░░███   ███████ ░███ ░░░  ░██████░  ░███████  ░███ ░░░    ░███    █████  ███████  ░███ ░███  ░███ ░███   ░███     ░███ ░███████   ░███    ",
" ░███    ░███  ███░░███ ░███  ███ ░███░░███ ░███░░░   ░███        ░░███  ░░███  ███░░███  ░███ ░███  ░███ ░███   ░███ ███ ░███ ░███░░░    ░███ ███",
" █████   █████░░████████░░██████  ████ █████░░██████  █████        ░░█████████ ░░████████ ░░████████ ████ █████  ░░█████  █████░░██████   ░░█████ ",
"░░░░░   ░░░░░  ░░░░░░░░  ░░░░░░  ░░░░ ░░░░░  ░░░░░░  ░░░░░          ░░░░░░░░░   ░░░░░░░░   ░░░░░░░░ ░░░░ ░░░░░    ░░░░░  ░░░░░  ░░░░░░     ░░░░░  "
    ]

    # Print Banner
    banner_start_y = 1
    if w > len(banner_lines[0])+ 4:
        for i, line in enumerate(banner_lines):
            stdscr.addstr(banner_start_y + i, (w - len(line)) // 2, line)  

    # Adjust menu start position based on the banner
    menu_start_y = banner_start_y + len(banner_lines) + 1
    for idx, file_name in enumerate(compose_files):
        label = get_label_from_file(file_name) if file_name.endswith((".yaml", ".yml")) else file_name
        x = w//2 - len(label)//2
        y = menu_start_y + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, label)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, label)
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    compose_files = get_compose_files()
    if not compose_files:
        stdscr.addstr(0, 0, "No Docker Compose files found in the current directory.")
        stdscr.refresh()
        stdscr.getch()
        return
    compose_files.append("Documentation/Guides")
    compose_files.append("Scoring")
    compose_files.append("Exit")
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
            if current_row_idx == len(compose_files) - 3:
                webbrowser.open_new_tab(documentation_link)
            elif current_row_idx == len(compose_files) - 2:
                webbrowser.open_new_tab(scoring_link)
            elif current_row_idx == len(compose_files) - 1:
                break  # Exit the loop if "Exit" is selected
            else:
                selected_file = compose_files[current_row_idx]
                selected_label = get_label_from_file(selected_file)
                if selected_label:
                    stdscr.addstr(0, 0, f"Selected: {selected_label}. Running docker compose... \n")
                    stdscr.refresh()
                    os.system(f"docker compose -f 'Challenge Compose Files/{selected_file}' up -d > /dev/null 2>&1")
                    os.system(f"docker compose -f 'Challenge Compose Files/{selected_file}' exec kali /bin/bash")
                    print("Turning Off Challenge...")
                    os.system(f"docker compose -f 'Challenge Compose Files/{selected_file}' down > /dev/null 2>&1")
                else:
                    stdscr.addstr(0, 0, "Error: No label found for selected file.")
                    stdscr.refresh()
                    stdscr.getch()
        print_menu(stdscr, current_row_idx, compose_files)

if __name__ == "__main__":
    curses.wrapper(main)

