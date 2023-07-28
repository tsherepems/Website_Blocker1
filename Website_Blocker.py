
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


"""
def hash_password(password):
    # Use SHA-256 for password hashing
    return hashlib.sha256(password.encode()).hexdigest()

def ask_password():
    password = simpledialog.askstring("Password", "Please enter the password:", show="*")
    if password:
        # Only set the password_checked flag if the user entered a password
        global password_checked
        password_checked = True
    return hash_password(password)

password_checked = False

def check_password():
    global password_checked
    if not password_checked:
        # Read the stored hashed password from the config.txt file
        try:
            with open("config.txt", "r") as file:
                stored_hashed_password = file.read().strip()
        except FileNotFoundError:
            stored_hashed_password = None

        if not stored_hashed_password:
            # If the config.txt file doesn't exist or is empty, prompt the user to set a new password
            entered_password = ask_password()
            with open("config.txt", "w") as file:
                file.write(entered_password)
            
            messagebox.showinfo("Password Set", "Password set successfully.")
            
            # Check if the script is running on Windows and has admin privileges
            if os.name == "nt" and ctypes.windll.shell32.IsUserAnAdmin():
                # If the script has admin privileges, re-run the script without admin privileges
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit()

        else:
            # Password is already set, prompt the user to enter the password and check it
            entered_password = simpledialog.askstring("Password", "Please enter the password:", show="*")
            hashed_entered_password = hash_password(entered_password)

            if hashed_entered_password == stored_hashed_password:
                # Check if the script is running on Windows and has admin privileges
                if os.name == "nt" and not ctypes.windll.shell32.IsUserAnAdmin():
                    # If not, re-run the script with admin privileges using the same arguments
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                    sys.exit()
                
                # Password is correct, set the flag to True
                password_checked = True
            else:
                messagebox.showerror("Incorrect Password", "Invalid password. Exiting the program.")
                sys.exit()


"""


def hash_password(password):
    # Use SHA-256 for password hashing
    return hashlib.sha256(password.encode()).hexdigest()

def ask_password():
    password = simpledialog.askstring("Password", "Please enter the password:", show="*")
    return hash_password(password)

def check_password():
    # Read the stored hashed password from the config.txt file
    try:
        with open("config.txt", "r") as file:
            stored_hashed_password = file.read().strip()
    except FileNotFoundError:
        stored_hashed_password = None

    if not stored_hashed_password:
        # If the config.txt file doesn't exist or is empty, prompt the user to set a new password
        entered_password = ask_password()
        with open("config.txt", "w") as file:
            file.write(entered_password)
        
        messagebox.showinfo("Password Set", "Password set successfully.")
        
        # Check if the script is running on Windows and has admin privileges
        if os.name == "nt" and ctypes.windll.shell32.IsUserAnAdmin():
            # If the script has admin privileges, re-run the script without admin privileges
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()

    else:
        # Password is already set, prompt the user to enter the password and check it
        entered_password = simpledialog.askstring("Password", "Please enter the password:", show="*")
        hashed_entered_password = hash_password(entered_password)

        if hashed_entered_password == stored_hashed_password:
            # Check if the script is running on Windows and has admin privileges
            if os.name == "nt" and not ctypes.windll.shell32.IsUserAnAdmin():
                # If not, re-run the script with admin privileges using the same arguments
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit()
        else:
            messagebox.showerror("Incorrect Password", "Invalid password. Exiting the program.")
            sys.exit()



def block_sites():
    system_type = platform.system()

    if system_type == "Windows":
        host_file_path = r"C:\Windows\System32\drivers\etc\hosts"
    elif system_type == "Linux" or system_type == "Darwin":
        host_file_path = "/etc/hosts"
    else:
        print("Unsupported operating system.")
        return

    try:
        # Ask the user to enter sites to be blocked
        sites_to_block = entry.get().split()

        # Check if the entry field is empty
        if not sites_to_block:
            messagebox.showerror("Empty Field", "Please enter a site to block.")
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
                messagebox.showinfo("Blocked Site", f"{site} blocked successfully.")
            else:
                messagebox.showinfo("Already Blocked", f"{site} is already blocked.")
    except FileNotFoundError:
        print("Hosts file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")




def unblock_sites():
    system_type = platform.system()

    if system_type == "Windows":
        host_file_path = r"C:\Windows\System32\drivers\etc\hosts"
    elif system_type == "Linux" or system_type == "Darwin":
        host_file_path = "/etc/hosts"
    else:
        print("Unsupported operating system.")
        return

    try:
        # Ask the user to enter sites to be unblocked
        sites_to_unblock = entry.get().split()

        # Check if the entry field is empty
        if not sites_to_unblock:
            messagebox.showerror("Empty Field", "Please enter a site to unblock.")
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

        messagebox.showinfo("Unblocked Site", "Selected sites unblocked successfully.")
    except FileNotFoundError:
        print("Hosts file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def list_blocked_sites():
    global blocked_sites_set
    system_type = platform.system()
    if system_type == "Windows":
        host_file_path = r"C:\Windows\System32\drivers\etc\hosts"
    elif system_type == "Linux" or system_type == "Darwin":
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
            messagebox.showinfo("Blocked Sites", f"The following sites are blocked:\n{blocked_sites_str}")
        else:
            messagebox.showinfo("Blocked Sites", "No sites are currently blocked.")
    except FileNotFoundError:
        print("Hosts file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def copy_blocked_sites():
    global blocked_sites_set
    try:
        
        # Call the list_blocked_sites() function to update blocked_sites_set
        list_blocked_sites()

        # Copy blocked sites to the clipboard
        blocked_sites_str = "\n".join(sorted(blocked_sites_set))
        root.clipboard_clear()
        root.clipboard_append(blocked_sites_str)

        messagebox.showinfo("Copy Blocked Sites", "Blocked sites copied to the clipboard.")
    except Exception as e:
        print(f"An error occurred: {e}")



def whitelist_sites():
    system_type = platform.system()
    if system_type == "Windows":
        host_file_path = r"C:\Windows\System32\drivers\etc\hosts"
    elif system_type == "Linux" or system_type == "Darwin":
        host_file_path = "/etc/hosts"
    else:
        print("Unsupported operating system.")
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
            if messagebox.askokcancel("Whitelist Sites", "Are you sure you want to whitelist all blocked sites?"):
                # Remove the lines containing all blocked sites from the host file content
                for site in blocked_sites:
                    line_to_remove = f"0.0.0.0 {site}"
                    if line_to_remove in host_content:
                        host_content = host_content.replace(line_to_remove, "")

                # Write the updated host file content
                with open(host_file_path, "w") as file:
                    file.write(host_content)

                messagebox.showinfo("Whitelisted Sites", "All blocked sites are whitelisted successfully.")
        else:
            messagebox.showinfo("No Blocked Sites", "There are no blocked sites to whitelist.")
    except FileNotFoundError:
        print("Hosts file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

#ping check

def ping_site2(site):  #not imp just for pop notif.
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
    

    
def ping_site(site, num_requests=3):
    try:
        response = subprocess.check_output(["ping", "-n", str(num_requests), site])
        return response.decode()
    except subprocess.CalledProcessError:
        return f"Failed to ping {site}."
    


def confirm_blocking_status():
    sites_to_check = entry.get().split()

    if not sites_to_check:
        messagebox.showerror("Empty Field", "Please enter sites to check.")
        return

    blocking_status = ""
    for site in sites_to_check:
        status = ping_site2(site)
        blocking_status += f"{status}\n"

    
    ping_responses = ""
    for site in sites_to_check:
        response = ping_site(site)
        ping_responses += f"Ping responses for {site}:\n{response}\n\n"


        
    # Clear the output text widget and display the results
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, ping_responses)

    # Show the results in a message box
    messagebox.showinfo("Blocking Status", blocking_status)



# Function to schedule site blocking and unblocking
def schedule_site_blocking(schedule_time, sites, action):
    s = sched.scheduler(time.time, time.sleep)
    for site in sites:
        s.enterabs(schedule_time, 1, perform_blocking_action, argument=(site, action))
    s.run()


# Function to perform the actual blocking or unblocking action
def perform_blocking_action(site, action):
    if action == "block":
        block_sites(site)
    elif action == "unblock":
        unblock_sites(site)


def schedule_blocking():
    #date_str = simpledialog.askstring("Schedule Blocking", "Enter the date and time (YYYY-MM-DD HH:MM:SS) to activate the blocking:")
    date_str=schedule_time_entry.get()
    try:
        # Parse the user input string to a datetime object
        schedule_time = parse_date(date_str)

        # Get the current time
        current_time = datetime.now()

        # Calculate the time difference (in seconds) between the schedule time and current time
        time_difference = (schedule_time - current_time).total_seconds()

        # Schedule the blocking after the time difference
        root.after(int(time_difference * 1000), block_sites)

        # Show a pop-up message confirming the schedule
        messagebox.showinfo("Schedule Set", "The blocking is scheduled successfully.")

    except ValueError:
        messagebox.showerror("Invalid Date Format", "Invalid date format. Please use YYYY-MM-DD HH:MM:SS format.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def schedule_unblocking():
    date_str = schedule_time_entry.get()

    try:
        # Parse the user input string to a datetime object
        schedule_time = parse_date(date_str)

        # Get the current time
        current_time = datetime.now()

        # Calculate the time difference (in seconds) between the schedule time and current time
        time_difference = (schedule_time - current_time).total_seconds()

        # Schedule the unblocking after the time difference
        root.after(int(time_difference * 1000), unblock_sites)

        # Show a pop-up message confirming the schedule
        messagebox.showinfo("Schedule Set", "The unblocking is scheduled successfully.")

    except ValueError:
        messagebox.showerror("Invalid Date Format", "Invalid date format. Please use YYYY-MM-DD HH:MM:SS format.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


#function for file menu
def exit_program():
    if messagebox.askokcancel("Exit", "!!!Do you really want to exit the program ?"):
        root.destroy()


def show_help():
    help_text = """This is a simple website blocker.
Please feel free to ask any queries at www.linkedin.com/in/pemba-sherpa-40a188263"""
    messagebox.showinfo("Help", help_text)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Webite Blocker")
    root.geometry("400x500")

       
# Call the check_password() function at the beginning of the script
    check_password()

    
    # Create a custom font for the title
    title_font = ("Helvetica", 20, "bold")

    # Create a label widget for the title and use the custom font
    title_label = ttk.Label(root, text="Website Blocker", font=title_font)
    title_label.pack(pady=20, padx=10)


    # Create custom styles for our GUI
    style = ttk.Style()

    # Create a color scheme
    bg = "#f0f4f9"  #f0f4f9
    fg = "#303030"

    # Use the color scheme for different elements
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TEntry", background=bg, foreground=fg)
    style.configure("TButton", background="#0078d4", foreground="black") 

    label = ttk.Label(root, text="Enter the sites to block/unblock (separate each site with a space):")
    label.pack(pady=10)

    entry = ttk.Entry(root, width=50)
    entry.pack(pady=10)

    block_button = ttk.Button(root, text="Block Sites", command=block_sites)
    block_button.pack(pady=5)

    unblock_button = ttk.Button(root, text="Unblock Sites", command=unblock_sites)
    unblock_button.pack(pady=5)

    list_button = ttk.Button(root, text="List Blocked Sites", command=list_blocked_sites)
    list_button.pack(pady=5)


    whitelist_button = ttk.Button(root, text="Whitelist All Sites", command=whitelist_sites)
    whitelist_button.pack(pady=5)

    
    check_button = ttk.Button(root, text="Check Blocking Status", command=confirm_blocking_status)
    check_button.pack(pady=5)

    
    # Create a text widget to display the ping responses
    output_text = tk.Text(root, wrap=tk.WORD, height=10)
    output_text.pack(pady=5, padx=20)
    output_text.insert(tk.END, "Results will appear here.")


    # Add entry fields for scheduling time
    schedule_time_label = ttk.Label(root, text="Enter the schedule time (YYYY-MM-DD HH:MM:SS):")
    schedule_time_label.pack(pady=5)
    schedule_time_entry = ttk.Entry(root, width=30)
    schedule_time_entry.pack(pady=5)


    #file menu part
    menu=tk.Menu(root)
    root.config(menu=menu)


    file_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="File", menu=file_menu)

      # Add a "Copy Blocked Sites" option to the File menu
    file_menu.add_command(label="Copy Blocked Sites", command=copy_blocked_sites)

    # Add an "Exit" option to the File menu
    file_menu.add_command(label="Exit", command=exit_program)

    
    # Help menu
    help_menu = tk.Menu(menu, tearoff=False)
    menu.add_cascade(label="Help", menu=help_menu)

    help_menu.add_command(label="About", command=show_help)



    root.mainloop()




