import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import platform
import os
import sys
import subprocess
import hashlib
from tkinter import simpledialog
import ctypes
import sched
import time
from dateutil.parser import parse as parse_date
from datetime import datetime

class WebsiteBlockerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Website Blocker")
        self.root.geometry("400x500")
        self.check_password()

        self.create_widgets()
        self.create_menu()
        self.check_admin_privileges()

    def check_admin_privileges(self):
        if os.name == "nt" and not ctypes.windll.shell32.IsUserAnAdmin():
            result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            if result != 42:
                tk.messagebox.showerror("Admin Privileges Required", "This program requires administrator privileges to run.")
                sys.exit()


    def hash_password(self, password):
        # Use SHA-256 for password hashing
        return hashlib.sha256(password.encode()).hexdigest()

    def ask_password(self):
        password = simpledialog.askstring("Password", "Please enter the password:", show="*")
        return self.hash_password(password)
    
    def check_password(self):
        try:
            with open("config.txt", "r") as file:
                stored_hashed_password = file.read().strip()
        except FileNotFoundError:
            stored_hashed_password = None

        if not stored_hashed_password:
            # If the config.txt file doesn't exist or is empty, prompt the user to set a new password
            entered_password = self.ask_password()
            with open("config.txt", "w") as file:
                file.write(entered_password)

            messagebox.showinfo("Password Set", "Password set successfully.")

        else:
            # Password is already set, prompt the user to enter the password and check it
            entered_password = self.ask_password()
            if entered_password != stored_hashed_password:
                # Show an error message and exit the program
                messagebox.showerror("Incorrect Password", "Invalid password.")
                sys.exit()


    def create_widgets(self):
        title_font = ("Helvetica", 20, "bold")
        self.title_label = ttk.Label(self.root, text="Website Blocker", font=title_font)
        self.title_label.pack(pady=20, padx=10)

        label = ttk.Label(self.root, text="Enter the sites to block/unblock (separate each site with a space):")
        label.pack(pady=10)

        self.entry = ttk.Entry(self.root, width=50)
        self.entry.pack(pady=10)

        block_button = ttk.Button(self.root, text="Block Sites", command=self.block_sites)
        block_button.pack(pady=5)

        unblock_button = ttk.Button(self.root, text="Unblock Sites", command=self.unblock_sites)
        unblock_button.pack(pady=5)

        list_button = ttk.Button(self.root, text="List Blocked Sites", command=self.list_blocked_sites)
        list_button.pack(pady=5)

        whitelist_button = ttk.Button(self.root, text="Whitelist All Sites", command=self.whitelist_sites)
        whitelist_button.pack(pady=5)

        check_button = ttk.Button(self.root, text="Check Blocking Status", command=self.confirm_blocking_status)
        check_button.pack(pady=5)

        self.output_text = tk.Text(self.root, wrap=tk.WORD, height=10)
        self.output_text.pack(pady=5, padx=20)
        self.output_text.insert(tk.END, "Results will appear here.")

        self.schedule_time_label = ttk.Label(self.root, text="Enter the schedule time (YYYY-MM-DD HH:MM:SS):")
        self.schedule_time_label.pack(pady=5)
        self.schedule_time_entry = ttk.Entry(self.root, width=30)
        self.schedule_time_entry.pack(pady=5)

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="Copy Blocked Sites", command=self.copy_blocked_sites)
        file_menu.add_command(label="Exit", command=self.exit_program)

        help_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="Help", menu=help_menu)

        help_menu.add_command(label="About", command=self.show_help)

    def block_sites(self):
        system_type = platform.system()

        if system_type == "Windows":
            host_file_path = r"C:\Windows\System32\drivers\etc\hosts"
        elif system_type in ("Linux", "Darwin"):
            host_file_path = "/etc/hosts"
        else:
            print("Unsupported operating system.")
            return

        try:
            # Ask the user to enter sites to be blocked
            sites_to_block = self.entry.get().split()

            # Check if the entry field is empty
            if not sites_to_block:
                tk.messagebox.showerror("Empty Field", "Please enter a site to block.")
                return

            # Read the existing host file content
            with open(host_file_path, "r") as file:
                host_content = file.read()

            # Add the lines to block sites to the host file content
            for site in sites_to_block:
                line_to_add = f"0.0.0.0 {site}"
                if line_to_add not in host_content:
                    with open(host_file_path, "a") as file:
                        file.write("\n" + line_to_add)
                    tk.messagebox.showinfo("Blocked Site", f"{site} blocked successfully.")
                else:
                    tk.messagebox.showinfo("Already Blocked", f"{site} is already blocked.")
        except FileNotFoundError:
            print("Hosts file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def unblock_sites(self):
        system_type = platform.system()

        if system_type == "Windows":
            host_file_path = r"C:\Windows\System32\drivers\etc\hosts"
        elif system_type in ("Linux", "Darwin"):
            host_file_path = "/etc/hosts"
        else:
            print("Unsupported operating system.")
            return

        try:
            # Ask the user to enter sites to be unblocked
            sites_to_unblock = self.entry.get().split()

            # Check if the entry field is empty
            if not sites_to_unblock:
                tk.messagebox.showerror("Empty Field", "Please enter a site to unblock.")
                return

            # Read the existing host file content
            with open(host_file_path, "r") as file:
                host_content = file.read()

            # Remove the lines to unblock sites from the host file content
            for site in sites_to_unblock:
                line_to_remove = f"0.0.0.0 {site}"
                if line_to_remove in host_content:
                    host_content = host_content.replace(line_to_remove, "")

            # Write the updated host file content
            with open(host_file_path, "w") as file:
                file.write(host_content)

            tk.messagebox.showinfo("Unblocked Site", "Selected sites unblocked successfully.")
        except FileNotFoundError:
            print("Hosts file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def list_blocked_sites(self):
        global blocked_sites_set

        system_type = platform.system()
        if system_type == "Windows":
            host_file_path = r"C:\Windows\System32\drivers\etc\hosts"
        elif system_type in ("Linux", "Darwin"):
            host_file_path = "/etc/hosts"
        else:
            print("Unsupported operating system.")
            return

        try:
            # Read the existing host file content
            with open(host_file_path, "r") as file:
                host_content = file.read()

            # Get the blocked sites from the host file content and store in blocked_sites_set
            blocked_sites_set = set()
            for line in host_content.splitlines():
                if line.strip().startswith("0.0.0.0"):
                    site = line.strip().split()[1]
                    blocked_sites_set.add(site)

            if blocked_sites_set:
                blocked_sites_str = "\n".join(sorted(blocked_sites_set))
                tk.messagebox.showinfo("Blocked Sites", f"The following sites are blocked:\n{blocked_sites_str}")
            else:
                tk.messagebox.showinfo("Blocked Sites", "No sites are currently blocked.")
        except FileNotFoundError:
            print("Hosts file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")




    def whitelist_sites(self):
        system_type = platform.system()
        if system_type == "Windows":
            host_file_path = r"C:\Windows\System32\drivers\etc\hosts"
        elif system_type in ("Linux", "Darwin"):
            host_file_path = "/etc/hosts"
        else:
            tk.messagebox.showerror("Unsupported OS", "Unsupported operating system.")
            return

        try:
            # Read the existing host file content
            with open(host_file_path, "r") as file:
                host_content = file.read()

            # Get the blocked sites from the host file content
            blocked_sites = set()
            for line in host_content.splitlines():
                if line.strip().startswith("0.0.0.0"):
                    site = line.strip().split()[1]
                    blocked_sites.add(site)

            if blocked_sites:
                # Display a warning message to confirm the action
                if tk.messagebox.askokcancel("Whitelist Sites", "Are you sure you want to whitelist all blocked sites?"):
                    # Remove the lines containing all blocked sites from the host file content
                    for site in blocked_sites:
                        line_to_remove = f"0.0.0.0 {site}"
                        if line_to_remove in host_content:
                            host_content = host_content.replace(line_to_remove, "")

                    # Write the updated host file content
                    with open(host_file_path, "w") as file:
                        file.write(host_content)

                    tk.messagebox.showinfo("Whitelisted Sites", "All blocked sites are whitelisted successfully.")
            else:
                tk.messagebox.showinfo("No Blocked Sites", "There are no blocked sites to whitelist.")
        except FileNotFoundError:
            print("Hosts file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")




    def ping_site2(self, site):
        try:
            # Use the ping command to check the site's accessibility
            # On Windows, use '-n' to specify the number of ping requests
            # On Linux/Mac, use '-c' to specify the number of ping requests
            if platform.system() == "Windows":
                result = subprocess.run(["ping", "-n", "1", site], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            else:
                result = subprocess.run(["ping", "-c", "1", site], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Check the return code to determine if the ping was successful or not
            if result.returncode == 0:
                return f"{site} is reachable."
            else:
                return f"{site} is blocked."
        except Exception as e:
            return f"Error occurred while pinging {site}: {e}"

    def ping_site(self, site, num_requests=3):
        try:
            response = subprocess.check_output(["ping", "-n", str(num_requests), site])
            return response.decode()
        except subprocess.CalledProcessError:
            return f"Failed to ping {site}."



    def confirm_blocking_status(self):
        sites_to_check = self.entry.get().split()

        if not sites_to_check:
            tk.messagebox.showerror("Empty Field", "Please enter sites to check.")
            return

        blocking_status = ""
        for site in sites_to_check:
            status = self.ping_site2(site)
            blocking_status += f"{status}\n"

        ping_responses = ""
        for site in sites_to_check:
            response = self.ping_site(site)
            ping_responses += f"Ping responses for {site}:\n{response}\n\n"

        # Clear the output text widget and display the results
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, ping_responses)

        # Show the results in a message box
        tk.messagebox.showinfo("Blocking Status", blocking_status)


    def copy_blocked_sites(self):
        try:
            # Call the list_blocked_sites() method to update blocked_sites_set
            self.list_blocked_sites()

            # Copy blocked sites to the clipboard
            blocked_sites_str = "\n".join(sorted(blocked_sites_set))
            self.root.clipboard_clear()
            self.root.clipboard_append(blocked_sites_str)

            tk.messagebox.showinfo("Copy Blocked Sites", "Blocked sites copied to the clipboard.")
        except Exception as e:
            print(f"An error occurred: {e}")


    def schedule_site_blocking(self, schedule_time, sites, action):
        s = sched.scheduler(time.time, time.sleep)
        for site in sites:
            s.enterabs(schedule_time, 1, self.perform_blocking_action, argument=(site, action))
        s.run()

    def perform_blocking_action(self, site, action):
        if action == "block":
            self.block_sites(site)
        elif action == "unblock":
            self.unblock_sites(site)


    def schedule_blocking(self):
        date_str = self.schedule_time_entry.get()
        try:
            # Parse the user input string to a datetime object
            schedule_time = parse_date(date_str)

            # Get the current time
            current_time = datetime.now()

            # Calculate the time difference (in seconds) between the schedule time and current time
            time_difference = (schedule_time - current_time).total_seconds()

            # Schedule the blocking after the time difference
            self.root.after(int(time_difference * 1000), self.block_sites)

            # Show a pop-up message confirming the schedule
            messagebox.showinfo("Schedule Set", "The blocking is scheduled successfully.")

        except ValueError:
            messagebox.showerror("Invalid Date Format", "Invalid date format. Please use YYYY-MM-DD HH:MM:SS format.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def schedule_unblocking(self):
        date_str = self.schedule_time_entry.get()
        try:
            # Parse the user input string to a datetime object
            schedule_time = parse_date(date_str)

            # Get the current time
            current_time = datetime.now()

            # Calculate the time difference (in seconds) between the schedule time and current time
            time_difference = (schedule_time - current_time).total_seconds()

            # Schedule the unblocking after the time difference
            self.root.after(int(time_difference * 1000), self.unblock_sites)

            # Show a pop-up message confirming the schedule
            messagebox.showinfo("Schedule Set", "The unblocking is scheduled successfully.")

        except ValueError:
            messagebox.showerror("Invalid Date Format", "Invalid date format. Please use YYYY-MM-DD HH:MM:SS format.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")



        


    def exit_program(self):
        if messagebox.askokcancel("Exit", "!!!Do you really want to exit the program ?"):
            self.root.destroy()

    def show_help(self):
        help_text = """This is a simple website blocker.
Please feel free to ask any queries at www.linkedin.com/in/pemba-sherpa-40a188263"""
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebsiteBlockerApp(root)
    root.mainloop()





