<<<<<<< HEAD
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext, ttk
import os
import subprocess
import threading
import queue
import configparser
import shutil

# Save settings to config.ini
def save_settings():
    config['Settings']['base_dir'] = base_dir_var.get()
    config['Settings']['gcsim_path'] = gcsim_path_var.get()
    config['Settings']['project_name'] = project_combobox.get()
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Update file list in sidebar
def update_file_list():
    project_name = project_combobox.get()
    file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
    file_listbox.delete(0, tk.END)
    if os.path.exists(file_dir):
        files = [f for f in os.listdir(file_dir) if f.endswith(".txt")]
        for file in files:
            file_listbox.insert(tk.END, file)

# Update project dropdown
def update_project_list():
    base_dir = base_dir_var.get()
    project_dir = os.path.join(base_dir, "projects")
    if os.path.exists(project_dir):
        projects = [d for d in os.listdir(project_dir) if os.path.isdir(os.path.join(project_dir, d))]
        project_combobox['values'] = projects
        if projects:
            project_combobox.set(projects[0])  # Default to first project
        else:
            project_combobox.set('')
    else:
        project_combobox['values'] = []
        project_combobox.set('')

# Handle variable changes
def on_var_change(*args):
    save_settings()
    update_file_list()

# Browse for base directory
def browse_base_dir():
    path = filedialog.askdirectory(title="Select Base Directory")
    if path:
        base_dir_var.set(path)
        update_project_list()  # Update projects when base dir changes

# Browse for gcsim.exe
def browse_gcsim():
    path = filedialog.askopenfilename(title="Select gcsim.exe", filetypes=[("Executable files", "*.exe")])
    if path:
        gcsim_path_var.set(path)

# Create project folder structure
def create_project():
    base_dir = base_dir_var.get()
    project_name = project_combobox.get()
    if not base_dir or not project_name:
        status_var.set("Need base dir and project")
        return
    project_dir = os.path.join(base_dir, "projects", project_name)
    os.makedirs(os.path.join(project_dir, "configs"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "outputs"), exist_ok=True)
    status_var.set(f"Created at {project_dir}")
    messagebox.showinfo("Info", f"Ready! Add .txt files to:\n{os.path.join(project_dir, 'configs')}")
    update_project_list()  # Update project list after creation
    update_file_list()

# Load selected file on double-click
def load_selected_file(event):
    selection = file_listbox.curselection()
    if selection:
        file_name = file_listbox.get(selection[0])
        project_name = project_combobox.get()
        file_path = os.path.join(base_dir_var.get(), "projects", project_name, "configs", file_name)
        with open(file_path, "r") as f:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, f.read())
        current_file_var.set(file_path)
        status_var.set(f"Loaded: {file_name}")
        file_indicator.config(text=f"File: {file_name}")

# Create new file
def new_file():
    project_name = project_combobox.get()
    if not project_name:
        status_var.set("Select a project first")
        return
    file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
    if not os.path.exists(file_dir):
        status_var.set("Project not found. Click 'Create'.")
        return
    file_name = simpledialog.askstring("New File", "Enter file name (e.g., test):")
    if file_name:
        if not file_name.endswith(".txt"):
            file_name += ".txt"
        file_path = os.path.join(file_dir, file_name)
        with open(file_path, "w") as f:
            f.write("")
        current_file_var.set(file_path)
        text_area.delete(1.0, tk.END)
        status_var.set(f"New file: {file_name}")
        file_indicator.config(text=f"File: {file_name}")
        update_file_list()

# Load existing file
def load_file():
    project_name = project_combobox.get()
    if not project_name:
        status_var.set("Select a project first")
        return
    file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
    file_path = filedialog.askopenfilename(initialdir=file_dir, title="Pick a File", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as f:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, f.read())
        current_file_var.set(file_path)
        status_var.set(f"Loaded: {os.path.basename(file_path)}")
        file_indicator.config(text=f"File: {os.path.basename(file_path)}")

# Save file
def save_file():
    file_path = current_file_var.get()
    if not file_path:
        status_var.set("No file loaded")
        return
    with open(file_path, "w") as f:
        f.write(text_area.get(1.0, tk.END))
    status_var.set(f"Saved: {os.path.basename(file_path)}")
    file_indicator.config(text=f"File: {os.path.basename(file_path)} (Saved)")

# Rename selected file
def rename_file():
    selection = file_listbox.curselection()
    if not selection:
        messagebox.showwarning("No Selection", "Select a file to rename")
        return
    old_name = file_listbox.get(selection[0])
    new_name = simpledialog.askstring("Rename", f"New name for {old_name}:", initialvalue=old_name)
    if new_name:
        if not new_name.endswith(".txt"):
            new_name += ".txt"
        project_name = project_combobox.get()
        file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
        old_path = os.path.join(file_dir, old_name)
        new_path = os.path.join(file_dir, new_name)
        if os.path.exists(new_path):
            messagebox.showerror("Error", f"{new_name} already exists")
            return
        os.rename(old_path, new_path)
        update_file_list()
        if current_file_var.get() == old_path:
            current_file_var.set(new_path)
            status_var.set(f"Renamed to: {new_name}")
            file_indicator.config(text=f"File: {new_name}")

# Delete selected file
def delete_file():
    selection = file_listbox.curselection()
    if not selection:
        messagebox.showwarning("No Selection", "Select a file to delete")
        return
    file_name = file_listbox.get(selection[0])
    project_name = project_combobox.get()
    file_path = os.path.join(base_dir_var.get(), "projects", project_name, "configs", file_name)
    if messagebox.askyesno("Confirm", f"Delete {file_name}?"):
        os.remove(file_path)
        update_file_list()
        if current_file_var.get() == file_path:
            current_file_var.set("")
            text_area.delete(1.0, tk.END)
            status_var.set("Deleted file")
            file_indicator.config(text="No file loaded")

# Duplicate selected file
def duplicate_file():
    selection = file_listbox.curselection()
    if not selection:
        messagebox.showwarning("No Selection", "Select a file to duplicate")
        return
    original_name = file_listbox.get(selection[0])
    project_name = project_combobox.get()
    file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
    original_path = os.path.join(file_dir, original_name)
    base, ext = os.path.splitext(original_name)
    copy_name = f"{base}_copy{ext}"
    copy_path = os.path.join(file_dir, copy_name)
    counter = 1
    while os.path.exists(copy_path):
        copy_name = f"{base}_copy_{counter}{ext}"
        copy_path = os.path.join(file_dir, copy_name)
        counter += 1
    shutil.copyfile(original_path, copy_path)
    update_file_list()
    status_var.set(f"Duplicated to {copy_name}")

# Process log queue
def process_log_queue():
    try:
        while True:
            log_area.insert(tk.END, log_queue.get_nowait())
            log_area.see(tk.END)
    except queue.Empty:
        pass
    root.after(100, process_log_queue)

# Global list to track running processes
running_processes = []

# Run a single simulation
def run_single_simulation(file_path):
    gcsim_path = gcsim_path_var.get()
    project_name = project_combobox.get()
    base_dir = base_dir_var.get()
    if not all([gcsim_path, project_name, base_dir]):
        log_queue.put("Set base dir, gcsim, and project\n")
        return
    output_dir = os.path.join(base_dir, "projects", project_name, "outputs")
    file_name = os.path.basename(file_path)
    log_queue.put(f"Starting simulation for {file_name}...\n")
    
    # Optimization step
    optimized_path = os.path.join(output_dir, file_name.replace(".txt", "_opt.txt"))
    process = subprocess.Popen([gcsim_path, "-c", file_path, "-substatOptim", "-out", optimized_path],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    running_processes.append(process)
    stdout, stderr = process.communicate()
    if process in running_processes:
        running_processes.remove(process)
    log_queue.put(stdout + "\n")
    if process.returncode != 0:
        log_queue.put(f"Optimization error for {file_name}: {stderr}\n")
        status_var.set(f"Optimization failed for {file_name}")
        return
    
    # Simulation step
    output_path = os.path.join(output_dir, file_name.replace(".txt", "_out.txt"))
    process = subprocess.Popen([gcsim_path, "-c", optimized_path, "-out", output_path, "-s"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    running_processes.append(process)
    stdout, stderr = process.communicate()
    if process in running_processes:
        running_processes.remove(process)
    log_queue.put(stdout + "\n")
    if process.returncode != 0:
        log_queue.put(f"Run error for {file_name}: {stderr}\n")
        status_var.set(f"Run failed for {file_name}")
    else:
        log_queue.put(f"Completed simulation for {file_name}\n")

# Threaded simulation (for single file runs)
def run_single_simulation_thread(file_path):
    threading.Thread(target=run_single_simulation, args=(file_path,), daemon=True).start()

# Run all simulations sequentially in a background thread
running_all = False  # Debounce flag
def run_all_simulations():
    global running_all
    if running_all:
        log_queue.put("Already running all simulations, please wait...\n")
        return
    project_name = project_combobox.get()
    file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
    if not os.path.exists(file_dir):
        status_var.set("No project folder found")
        return
    files = [os.path.join(file_dir, f) for f in os.listdir(file_dir) if f.endswith(".txt")]
    if not files:
        status_var.set("No .txt files found")
        return
    unique_files = set(files)  # Ensure no duplicates
    log_queue.put(f"Starting {len(unique_files)} simulations sequentially...\n")
    running_all = True
    
    def run_sequential():
        for file_path in unique_files:
            log_queue.put(f"Processing: {os.path.basename(file_path)}\n")
            run_single_simulation(file_path)  # Run sequentially in this thread
        status_var.set(f"Completed {len(unique_files)} simulations")
        global running_all
        running_all = False
    
    threading.Thread(target=run_sequential, daemon=True).start()

# Run selected simulation
def run_selected_simulation():
    file_path = current_file_var.get()
    if not file_path:
        status_var.set("No file loaded")
        return
    run_single_simulation_thread(file_path)

# Terminate running processes
def terminate_processes():
    global running_processes
    if not running_processes:
        log_queue.put("No running processes to terminate\n")
        return
    for process in running_processes[:]:  # Copy list to avoid modification issues
        process.terminate()
        running_processes.remove(process)
    log_queue.put("Terminated all running processes\n")
    status_var.set("Processes terminated")
    global running_all
    running_all = False  # Allow restarting after termination

# GUI setup
root = tk.Tk()
root.title("gcsim manager")
root.configure(bg="#2e2e2e")

# Variables
base_dir_var = tk.StringVar()
gcsim_path_var = tk.StringVar()
status_var = tk.StringVar()
current_file_var = tk.StringVar()
log_queue = queue.Queue()

# Sidebar
sidebar_frame = tk.Frame(root, bg="#2e2e2e")
sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="ns")
file_listbox = tk.Listbox(sidebar_frame, bg="#3e3e3e", fg="white", selectbackground="#4e4e4e", width=20)
scrollbar = tk.Scrollbar(sidebar_frame, orient="vertical", command=file_listbox.yview)
file_listbox.config(yscrollcommand=scrollbar.set)
file_listbox.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
file_listbox.bind("<Double-Button-1>", load_selected_file)

# Input frame (only essential items)
input_frame = tk.Frame(root, bg="#2e2e2e")
input_frame.grid(row=0, column=1, sticky="ew")

tk.Label(input_frame, text="Base Dir:", bg="#2e2e2e", fg="white").grid(row=0, column=0, padx=5, pady=2)
tk.Entry(input_frame, textvariable=base_dir_var, width=25, bg="#3e3e3e", fg="white").grid(row=0, column=1, padx=5, pady=2)
tk.Button(input_frame, text="Browse", command=browse_base_dir, bg="#4e4e4e", fg="white", width=8).grid(row=0, column=2, padx=5, pady=2)

tk.Label(input_frame, text="gcsim Path:", bg="#2e2e2e", fg="white").grid(row=1, column=0, padx=5, pady=2)
tk.Entry(input_frame, textvariable=gcsim_path_var, width=25, bg="#3e3e3e", fg="white").grid(row=1, column=1, padx=5, pady=2)
tk.Button(input_frame, text="Browse", command=browse_gcsim, bg="#4e4e4e", fg="white", width=8).grid(row=1, column=2, padx=5, pady=2)

tk.Label(input_frame, text="Project:", bg="#2e2e2e", fg="white").grid(row=2, column=0, padx=5, pady=2)
project_combobox = ttk.Combobox(input_frame, width=23)
project_combobox.grid(row=2, column=1, padx=5, pady=2)
tk.Button(input_frame, text="Create", command=create_project, bg="#4e4e4e", fg="white", width=8).grid(row=2, column=2, padx=5, pady=2)

# Editor
text_area = tk.Text(root, height=20, width=40, bg="#3e3e3e", fg="white", insertbackground="white")
text_area.grid(row=1, column=1, sticky="nsew")

# File indicator
file_indicator = tk.Label(root, text="No file loaded", bg="#2e2e2e", fg="white")
file_indicator.grid(row=1, column=1, sticky="sw", padx=5, pady=5)

# Log area (smaller)
log_area = scrolledtext.ScrolledText(root, height=10, width=60, bg="#3e3e3e", fg="white")
log_area.grid(row=2, column=1, sticky="nsew")

# Buttons frame (right side)
buttons_frame = tk.Frame(root, bg="#2e2e2e")
buttons_frame.grid(row=1, column=2, sticky="ns")

# Add buttons to buttons_frame
tk.Button(buttons_frame, text="New", command=new_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Load", command=load_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Save", command=save_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Run All", command=run_all_simulations, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Run", command=run_selected_simulation, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Rename", command=rename_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Delete", command=delete_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Duplicate", command=duplicate_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Terminate", command=terminate_processes, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)

# Grid weights
root.grid_columnconfigure(0, weight=0)  # Sidebar
root.grid_columnconfigure(1, weight=1)  # Text editor and log
root.grid_columnconfigure(2, weight=0)  # Buttons frame
root.grid_rowconfigure(0, weight=0)     # Input frame
root.grid_rowconfigure(1, weight=1)     # Text editor and buttons
root.grid_rowconfigure(2, weight=0)     # Log

# Load or create config
config = configparser.ConfigParser()
if os.path.exists('config.ini'):
    config.read('config.ini')
else:
    config['Settings'] = {'base_dir': '', 'gcsim_path': '', 'project_name': ''}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Set variables from config
base_dir_var.set(config['Settings'].get('base_dir', ''))
gcsim_path_var.set(config['Settings'].get('gcsim_path', ''))
project_combobox.set(config['Settings'].get('project_name', ''))

# Add traces
base_dir_var.trace('w', on_var_change)
gcsim_path_var.trace('w', save_settings)
project_combobox.bind('<<ComboboxSelected>>', lambda event: on_var_change())

# Update project list and file list on startup
update_project_list()
update_file_list()

# Start log queue
root.after(100, process_log_queue)

# Run GUI
=======
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, scrolledtext, ttk
import os
import subprocess
import threading
import queue
import configparser
import shutil

# Save settings to config.ini
def save_settings():
    config['Settings']['base_dir'] = base_dir_var.get()
    config['Settings']['gcsim_path'] = gcsim_path_var.get()
    config['Settings']['project_name'] = project_combobox.get()
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Update file list in sidebar
def update_file_list():
    project_name = project_combobox.get()
    file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
    file_listbox.delete(0, tk.END)
    if os.path.exists(file_dir):
        files = [f for f in os.listdir(file_dir) if f.endswith(".txt")]
        for file in files:
            file_listbox.insert(tk.END, file)

# Update project dropdown
def update_project_list():
    base_dir = base_dir_var.get()
    project_dir = os.path.join(base_dir, "projects")
    if os.path.exists(project_dir):
        projects = [d for d in os.listdir(project_dir) if os.path.isdir(os.path.join(project_dir, d))]
        project_combobox['values'] = projects
        if projects:
            project_combobox.set(projects[0])  # Default to first project
        else:
            project_combobox.set('')
    else:
        project_combobox['values'] = []
        project_combobox.set('')

# Handle variable changes
def on_var_change(*args):
    save_settings()
    update_file_list()

# Browse for base directory
def browse_base_dir():
    path = filedialog.askdirectory(title="Select Base Directory")
    if path:
        base_dir_var.set(path)
        update_project_list()  # Update projects when base dir changes

# Browse for gcsim.exe
def browse_gcsim():
    path = filedialog.askopenfilename(title="Select gcsim.exe", filetypes=[("Executable files", "*.exe")])
    if path:
        gcsim_path_var.set(path)

# Create project folder structure
def create_project():
    base_dir = base_dir_var.get()
    project_name = project_combobox.get()
    if not base_dir or not project_name:
        status_var.set("Need base dir and project")
        return
    project_dir = os.path.join(base_dir, "projects", project_name)
    os.makedirs(os.path.join(project_dir, "configs"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "outputs"), exist_ok=True)
    status_var.set(f"Created at {project_dir}")
    messagebox.showinfo("Info", f"Ready! Add .txt files to:\n{os.path.join(project_dir, 'configs')}")
    update_project_list()  # Update project list after creation
    update_file_list()

# Load selected file on double-click
def load_selected_file(event):
    selection = file_listbox.curselection()
    if selection:
        file_name = file_listbox.get(selection[0])
        project_name = project_combobox.get()
        file_path = os.path.join(base_dir_var.get(), "projects", project_name, "configs", file_name)
        with open(file_path, "r") as f:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, f.read())
        current_file_var.set(file_path)
        status_var.set(f"Loaded: {file_name}")
        file_indicator.config(text=f"File: {file_name}")

# Create new file
def new_file():
    project_name = project_combobox.get()
    if not project_name:
        status_var.set("Select a project first")
        return
    file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
    if not os.path.exists(file_dir):
        status_var.set("Project not found. Click 'Create'.")
        return
    file_name = simpledialog.askstring("New File", "Enter file name (e.g., test):")
    if file_name:
        if not file_name.endswith(".txt"):
            file_name += ".txt"
        file_path = os.path.join(file_dir, file_name)
        with open(file_path, "w") as f:
            f.write("")
        current_file_var.set(file_path)
        text_area.delete(1.0, tk.END)
        status_var.set(f"New file: {file_name}")
        file_indicator.config(text=f"File: {file_name}")
        update_file_list()

# Load existing file
def load_file():
    project_name = project_combobox.get()
    if not project_name:
        status_var.set("Select a project first")
        return
    file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
    file_path = filedialog.askopenfilename(initialdir=file_dir, title="Pick a File", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r") as f:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, f.read())
        current_file_var.set(file_path)
        status_var.set(f"Loaded: {os.path.basename(file_path)}")
        file_indicator.config(text=f"File: {os.path.basename(file_path)}")

# Save file
def save_file():
    file_path = current_file_var.get()
    if not file_path:
        status_var.set("No file loaded")
        return
    with open(file_path, "w") as f:
        f.write(text_area.get(1.0, tk.END))
    status_var.set(f"Saved: {os.path.basename(file_path)}")
    file_indicator.config(text=f"File: {os.path.basename(file_path)} (Saved)")

# Rename selected file
def rename_file():
    selection = file_listbox.curselection()
    if not selection:
        messagebox.showwarning("No Selection", "Select a file to rename")
        return
    old_name = file_listbox.get(selection[0])
    new_name = simpledialog.askstring("Rename", f"New name for {old_name}:", initialvalue=old_name)
    if new_name:
        if not new_name.endswith(".txt"):
            new_name += ".txt"
        project_name = project_combobox.get()
        file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
        old_path = os.path.join(file_dir, old_name)
        new_path = os.path.join(file_dir, new_name)
        if os.path.exists(new_path):
            messagebox.showerror("Error", f"{new_name} already exists")
            return
        os.rename(old_path, new_path)
        update_file_list()
        if current_file_var.get() == old_path:
            current_file_var.set(new_path)
            status_var.set(f"Renamed to: {new_name}")
            file_indicator.config(text=f"File: {new_name}")

# Delete selected file
def delete_file():
    selection = file_listbox.curselection()
    if not selection:
        messagebox.showwarning("No Selection", "Select a file to delete")
        return
    file_name = file_listbox.get(selection[0])
    project_name = project_combobox.get()
    file_path = os.path.join(base_dir_var.get(), "projects", project_name, "configs", file_name)
    if messagebox.askyesno("Confirm", f"Delete {file_name}?"):
        os.remove(file_path)
        update_file_list()
        if current_file_var.get() == file_path:
            current_file_var.set("")
            text_area.delete(1.0, tk.END)
            status_var.set("Deleted file")
            file_indicator.config(text="No file loaded")

# Duplicate selected file
def duplicate_file():
    selection = file_listbox.curselection()
    if not selection:
        messagebox.showwarning("No Selection", "Select a file to duplicate")
        return
    original_name = file_listbox.get(selection[0])
    project_name = project_combobox.get()
    file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
    original_path = os.path.join(file_dir, original_name)
    base, ext = os.path.splitext(original_name)
    copy_name = f"{base}_copy{ext}"
    copy_path = os.path.join(file_dir, copy_name)
    counter = 1
    while os.path.exists(copy_path):
        copy_name = f"{base}_copy_{counter}{ext}"
        copy_path = os.path.join(file_dir, copy_name)
        counter += 1
    shutil.copyfile(original_path, copy_path)
    update_file_list()
    status_var.set(f"Duplicated to {copy_name}")

# Process log queue
def process_log_queue():
    try:
        while True:
            log_area.insert(tk.END, log_queue.get_nowait())
            log_area.see(tk.END)
    except queue.Empty:
        pass
    root.after(100, process_log_queue)

# Global list to track running processes
running_processes = []

# Run a single simulation
def run_single_simulation(file_path):
    gcsim_path = gcsim_path_var.get()
    project_name = project_combobox.get()
    base_dir = base_dir_var.get()
    if not all([gcsim_path, project_name, base_dir]):
        log_queue.put("Set base dir, gcsim, and project\n")
        return
    output_dir = os.path.join(base_dir, "projects", project_name, "outputs")
    file_name = os.path.basename(file_path)
    log_queue.put(f"Starting simulation for {file_name}...\n")
    
    # Optimization step
    optimized_path = os.path.join(output_dir, file_name.replace(".txt", "_opt.txt"))
    process = subprocess.Popen([gcsim_path, "-c", file_path, "-substatOptim", "-out", optimized_path],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    running_processes.append(process)
    stdout, stderr = process.communicate()
    if process in running_processes:
        running_processes.remove(process)
    log_queue.put(stdout + "\n")
    if process.returncode != 0:
        log_queue.put(f"Optimization error for {file_name}: {stderr}\n")
        status_var.set(f"Optimization failed for {file_name}")
        return
    
    # Simulation step
    output_path = os.path.join(output_dir, file_name.replace(".txt", "_out.txt"))
    process = subprocess.Popen([gcsim_path, "-c", optimized_path, "-out", output_path, "-s"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    running_processes.append(process)
    stdout, stderr = process.communicate()
    if process in running_processes:
        running_processes.remove(process)
    log_queue.put(stdout + "\n")
    if process.returncode != 0:
        log_queue.put(f"Run error for {file_name}: {stderr}\n")
        status_var.set(f"Run failed for {file_name}")
    else:
        log_queue.put(f"Completed simulation for {file_name}\n")

# Threaded simulation (for single file runs)
def run_single_simulation_thread(file_path):
    threading.Thread(target=run_single_simulation, args=(file_path,), daemon=True).start()

# Run all simulations sequentially in a background thread
running_all = False  # Debounce flag
def run_all_simulations():
    global running_all
    if running_all:
        log_queue.put("Already running all simulations, please wait...\n")
        return
    project_name = project_combobox.get()
    file_dir = os.path.join(base_dir_var.get(), "projects", project_name, "configs")
    if not os.path.exists(file_dir):
        status_var.set("No project folder found")
        return
    files = [os.path.join(file_dir, f) for f in os.listdir(file_dir) if f.endswith(".txt")]
    if not files:
        status_var.set("No .txt files found")
        return
    unique_files = set(files)  # Ensure no duplicates
    log_queue.put(f"Starting {len(unique_files)} simulations sequentially...\n")
    running_all = True
    
    def run_sequential():
        for file_path in unique_files:
            log_queue.put(f"Processing: {os.path.basename(file_path)}\n")
            run_single_simulation(file_path)  # Run sequentially in this thread
        status_var.set(f"Completed {len(unique_files)} simulations")
        global running_all
        running_all = False
    
    threading.Thread(target=run_sequential, daemon=True).start()

# Run selected simulation
def run_selected_simulation():
    file_path = current_file_var.get()
    if not file_path:
        status_var.set("No file loaded")
        return
    run_single_simulation_thread(file_path)

# Terminate running processes
def terminate_processes():
    global running_processes
    if not running_processes:
        log_queue.put("No running processes to terminate\n")
        return
    for process in running_processes[:]:  # Copy list to avoid modification issues
        process.terminate()
        running_processes.remove(process)
    log_queue.put("Terminated all running processes\n")
    status_var.set("Processes terminated")
    global running_all
    running_all = False  # Allow restarting after termination

# GUI setup
root = tk.Tk()
root.title("gcsim manager")
root.configure(bg="#2e2e2e")

# Variables
base_dir_var = tk.StringVar()
gcsim_path_var = tk.StringVar()
status_var = tk.StringVar()
current_file_var = tk.StringVar()
log_queue = queue.Queue()

# Sidebar
sidebar_frame = tk.Frame(root, bg="#2e2e2e")
sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="ns")
file_listbox = tk.Listbox(sidebar_frame, bg="#3e3e3e", fg="white", selectbackground="#4e4e4e", width=20)
scrollbar = tk.Scrollbar(sidebar_frame, orient="vertical", command=file_listbox.yview)
file_listbox.config(yscrollcommand=scrollbar.set)
file_listbox.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
file_listbox.bind("<Double-Button-1>", load_selected_file)

# Input frame (only essential items)
input_frame = tk.Frame(root, bg="#2e2e2e")
input_frame.grid(row=0, column=1, sticky="ew")

tk.Label(input_frame, text="Base Dir:", bg="#2e2e2e", fg="white").grid(row=0, column=0, padx=5, pady=2)
tk.Entry(input_frame, textvariable=base_dir_var, width=25, bg="#3e3e3e", fg="white").grid(row=0, column=1, padx=5, pady=2)
tk.Button(input_frame, text="Browse", command=browse_base_dir, bg="#4e4e4e", fg="white", width=8).grid(row=0, column=2, padx=5, pady=2)

tk.Label(input_frame, text="gcsim Path:", bg="#2e2e2e", fg="white").grid(row=1, column=0, padx=5, pady=2)
tk.Entry(input_frame, textvariable=gcsim_path_var, width=25, bg="#3e3e3e", fg="white").grid(row=1, column=1, padx=5, pady=2)
tk.Button(input_frame, text="Browse", command=browse_gcsim, bg="#4e4e4e", fg="white", width=8).grid(row=1, column=2, padx=5, pady=2)

tk.Label(input_frame, text="Project:", bg="#2e2e2e", fg="white").grid(row=2, column=0, padx=5, pady=2)
project_combobox = ttk.Combobox(input_frame, width=23)
project_combobox.grid(row=2, column=1, padx=5, pady=2)
tk.Button(input_frame, text="Create", command=create_project, bg="#4e4e4e", fg="white", width=8).grid(row=2, column=2, padx=5, pady=2)

# Editor
text_area = tk.Text(root, height=20, width=40, bg="#3e3e3e", fg="white", insertbackground="white")
text_area.grid(row=1, column=1, sticky="nsew")

# File indicator
file_indicator = tk.Label(root, text="No file loaded", bg="#2e2e2e", fg="white")
file_indicator.grid(row=1, column=1, sticky="sw", padx=5, pady=5)

# Log area (smaller)
log_area = scrolledtext.ScrolledText(root, height=10, width=60, bg="#3e3e3e", fg="white")
log_area.grid(row=2, column=1, sticky="nsew")

# Buttons frame (right side)
buttons_frame = tk.Frame(root, bg="#2e2e2e")
buttons_frame.grid(row=1, column=2, sticky="ns")

# Add buttons to buttons_frame
tk.Button(buttons_frame, text="New", command=new_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Load", command=load_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Save", command=save_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Run All", command=run_all_simulations, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Run", command=run_selected_simulation, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Rename", command=rename_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Delete", command=delete_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Duplicate", command=duplicate_file, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)
tk.Button(buttons_frame, text="Terminate", command=terminate_processes, bg="#4e4e4e", fg="white").pack(side="top", fill="x", padx=5, pady=2)

# Grid weights
root.grid_columnconfigure(0, weight=0)  # Sidebar
root.grid_columnconfigure(1, weight=1)  # Text editor and log
root.grid_columnconfigure(2, weight=0)  # Buttons frame
root.grid_rowconfigure(0, weight=0)     # Input frame
root.grid_rowconfigure(1, weight=1)     # Text editor and buttons
root.grid_rowconfigure(2, weight=0)     # Log

# Load or create config
config = configparser.ConfigParser()
if os.path.exists('config.ini'):
    config.read('config.ini')
else:
    config['Settings'] = {'base_dir': '', 'gcsim_path': '', 'project_name': ''}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Set variables from config
base_dir_var.set(config['Settings'].get('base_dir', ''))
gcsim_path_var.set(config['Settings'].get('gcsim_path', ''))
project_combobox.set(config['Settings'].get('project_name', ''))

# Add traces
base_dir_var.trace('w', on_var_change)
gcsim_path_var.trace('w', save_settings)
project_combobox.bind('<<ComboboxSelected>>', lambda event: on_var_change())

# Update project list and file list on startup
update_project_list()
update_file_list()

# Start log queue
root.after(100, process_log_queue)

# Run GUI
>>>>>>> 5208b6bc2755f177b1dd6a905eab7065faeb91ae
root.mainloop()