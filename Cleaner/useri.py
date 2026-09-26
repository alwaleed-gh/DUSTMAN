import os
import sys
import questionary
from prompt_toolkit.styles import Style
from cleaner.config import TARGETS, DEFAULT_MAX_AGE_DAYS
from cleaner.cleaner import scan_directory, clean_directory

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

custom_style = Style.from_dict({
    'question': 'bold cyan',
    'selected': 'bold green',
    'pointer': 'bold yellow',
    'checkbox-selected': 'green',
})

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    banner = """
  ____  _   _ ____ _____ __  _   _ 
 |  _ \| | | / ___|_   _|  \/  | \ | |
 | | | | | | \___ \ | | | |\/| |  \| |
 | |_| | |_| |___) || | | |  | | | | |
 |____/ \___/|____/ |_| |_|  |_|_| \_| v1.0
"""
    print(f"{CYAN}{banner}{'═' * 50}{RESET}")
    
def ask_max_age_days() -> int:
    
    days_str = questionary.text(
        "Enter maximum file age in days (files older than this will be processed):",
        default=str(DEFAULT_MAX_AGE_DAYS),
        validate=lambda val: val.isdigit() and int(val) >= 0 or "Please enter a valid positive number!",
        style=custom_style
    ).ask()
    
    if days_str is None:  
        return DEFAULT_MAX_AGE_DAYS
    return int(days_str)

def select_targets():
    choices = [
        questionary.Choice(title=f"{target}", value=target, checked=True)
        for target in TARGETS
    ]
    
    selected = questionary.checkbox(
        "Select directories to clean (Use SPACE to select/deselect, ENTER to confirm):",
        choices=choices,
        style=custom_style
    ).ask()
    
    return selected

def start_ui():
    while True:
        clear_screen()
        print_header()

        action = questionary.select(
            "Select operation mode:",
            choices=[
                "🔍 Dry-Run (Scan without deleting)",
                "🗑️  Live Clean (Permanently delete files)",
                "⚙️  View Current Config",
                "❌ Exit"
            ],
            style=custom_style
        ).ask()

        if action is None or "Exit" in action:
            print(f"\n{YELLOW}Exiting dustman. Goodbye!{RESET}")
            sys.exit(0)

        elif "View Current Config" in action:
            print(f"\n{BOLD}📋 Configured Targets:{RESET}")
            for t in TARGETS:
                print(f"  - {t}")
            print(f"\n{BOLD}⏱️ Default File Age Threshold:{RESET} {DEFAULT_MAX_AGE_DAYS} days")
            questionary.press_any_key_to_continue().ask()

        elif "Dry-Run" in action:
            max_age = ask_max_age_days()
            selected_targets = select_targets()
            
            if not selected_targets:
                print(f"\n{YELLOW}⚠️ No directories selected.{RESET}")
            else:
                print(f"\n{CYAN}--- 📊 Scanning files older than {max_age} days ---{RESET}")
                total_files = 0
                total_space = 0.0

                for target in selected_targets:
                    files, space = scan_directory(target, max_age)
                    total_files += files
                    total_space += space

                print(f"\n{CYAN}{'═' * 45}{RESET}")
                print(f"{BOLD}{GREEN}📊 SCAN SUMMARY{RESET}")
                print(f"📦 Total Files Flagged : {BOLD}{total_files}{RESET}")
                print(f"💾 Total Space to Free : {BOLD}{GREEN}{total_space:.2f} MB{RESET}")
                print(f"{CYAN}{'═' * 45}{RESET}")
            
            questionary.press_any_key_to_continue().ask()

        elif "Live Clean" in action:
            max_age = ask_max_age_days()
            selected_targets = select_targets()

            if not selected_targets:
                print(f"\n{YELLOW}⚠️ No directories selected.{RESET}")
            else:
                confirm = questionary.confirm(
                    f"⚠️ Permanently delete files older than {max_age} days in selected directories?",
                    default=False,
                    style=custom_style
                ).ask()

                if confirm:
                    print(f"\n{RED}--- 🚀 Cleaning files older than {max_age} days ---{RESET}")
                    total_files_cleaned = 0
                    total_space_freed = 0.0

                    for target in selected_targets:
                        files, space = clean_directory(target, max_age, dry_run=False)
                        total_files_cleaned += files
                        total_space_freed += space

                    print(f"\n{CYAN}{'═' * 45}{RESET}")
                    print(f"{BOLD}{GREEN}🎉 CLEANUP COMPLETE!{RESET}")
                    print(f"📦 Total Files Removed : {BOLD}{total_files_cleaned}{RESET}")
                    print(f"💾 Total Space Freed   : {BOLD}{GREEN}{total_space_freed:.2f} MB{RESET}")
                    print(f"{CYAN}{'═' * 45}{RESET}")
                else:
                    print(f"\n{YELLOW}❌ Operation cancelled.{RESET}")

            questionary.press_any_key_to_continue().ask()