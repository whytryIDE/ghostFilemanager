import os
import shutil
import re
from datetime import datetime
from tkinter import Tk, Label, Entry, Text, Button, Frame, END, messagebox, filedialog

# b.end functions
def write_to_file():
    filename = create_file_name_entry.get()
    content = create_text_entry.get("1.0", END).strip()
    if filename and content:
        with open(filename, "w") as file:
            file.write(content)
        log_operation("Write", f"File: {filename}, Data: {content}")
        messagebox.showinfo("Success", f"Data written to file {filename}")
        create_file_name_entry.delete(0, END)
        create_text_entry.delete("1.0", END)
    else:
        messagebox.showwarning("Error", "Enter file name and text to write")

def read_from_file():
    filename = filedialog.askopenfilename()
    if filename:
        with open(filename, "r") as file:
            content = file.read()
        read_text_display.config(state='normal')
        read_text_display.delete("1.0", END)
        read_text_display.insert("1.0", content)
        read_text_display.config(state='disabled')
        log_operation("Read", f"File: {filename}")
    else:
        messagebox.showwarning("Error", "Select a file to read")

def delete_file():
    filename = delete_file_name_entry.get()
    if filename:
        if os.path.exists(filename):
            backup_filename = f"{filename}_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            shutil.copy(filename, backup_filename)
            os.remove(filename)
            log_operation("Delete", f"File: {filename}, Backup: {backup_filename}")
            messagebox.showinfo("Success", f"File {filename} deleted. Backup saved as {backup_filename}")
            delete_file_name_entry.delete(0, END)
        else:
            messagebox.showwarning("Error", f"File {filename} not found")
    else:
        messagebox.showwarning("Error", "Enter file name to delete")

def rename_file():
    old_filename = old_file_name_entry.get()
    new_filename = new_file_name_entry.get()
    if old_filename and new_filename:
        if os.path.exists(old_filename):
            os.rename(old_filename, new_filename)
            log_operation("Rename", f"Old name: {old_filename}, New name: {new_filename}")
            messagebox.showinfo("Success", f"File {old_filename} renamed to {new_filename}")
            old_file_name_entry.delete(0, END)
            new_file_name_entry.delete(0, END)
        else:
            messagebox.showwarning("Error", f"File {old_filename} not found")
    else:
        messagebox.showwarning("Error", "Enter old and new file names")

def analyze_text():
    filename = filedialog.askopenfilename()
    if filename:
        with open(filename, "r") as file:
            content = file.read()
        words = re.findall(r'\b\w+\b', content.lower())
        word_count = {word: words.count(word) for word in set(words)}
        analysis_result = "\n".join([f"{word}: {count}" for word, count in word_count.items()])
        analyze_text_display.config(state='normal')
        analyze_text_display.delete("1.0", END)
        analyze_text_display.insert("1.0", analysis_result)
        analyze_text_display.config(state='disabled')
        log_operation("Analyze", f"File: {filename}, Unique words: {len(word_count)}")
    else:
        messagebox.showwarning("Error", "Select a file to analyze")

def show_frame(frame):
    frame.tkraise()
    clear_entries(frame)

def clear_entries(frame):
    for widget in frame.winfo_children():
        if isinstance(widget, Entry):
            widget.delete(0, END)
        elif isinstance(widget, Text):
            widget.delete("1.0", END)

def log_operation(operation, details):
    with open("file_operations.log", "a") as log_file:
        log_file.write(f"{datetime.now()} - {operation}: {details}\n")

# Frontend
root = Tk()
root.title("ghostFilemanager")
root.configure(bg='#272727')
root.resizable(False, False)

frames = {}
for F in ("Main", "Create", "Read", "Delete", "Rename", "Analyze"):
    frame = Frame(root, bg='#272727')
    frame.grid(row=0, column=0, sticky='nsew')
    frames[F] = frame

    #color: (#272727 фон,#48494a кнопки, #edc3ca текст, #464241 кнопки2 )


# Main page
main_frame = frames["Main"]
Label(main_frame, text="ghostFilemanager", bg='#272727', fg='#cdcdcd', font=("Helvetica", 8)).pack(pady=10)
Label(main_frame, text="Select an action:", bg='#48494a', fg='#edc3ca', font=("Helvetica", 16)).pack(pady=20)
Button(main_frame, text="Create File", command=lambda: show_frame(frames["Create"]), bg='#48494a', fg='#edc3ca', width=20).pack(pady=5)
Button(main_frame, text="Read File", command=lambda: show_frame(frames["Read"]), bg='#464241', fg='#edc3ca', width=20).pack(pady=5)
Button(main_frame, text="Delete File", command=lambda: show_frame(frames["Delete"]), bg='#48494a', fg='#edc3ca', width=20).pack(pady=5)
Button(main_frame, text="Rename File", command=lambda: show_frame(frames["Rename"]), bg='#464241', fg='#edc3ca', width=20).pack(pady=5)
Button(main_frame, text="Analyze Text in File", command=lambda: show_frame(frames["Analyze"]), bg='#48494a', fg='#edc3ca', width=20).pack(pady=5)

# Create page
create_frame = frames["Create"]
Label(create_frame, text="File name:", bg='#48494a', fg='#edc3ca').grid(row=0, column=0, padx=5, pady=5, sticky='e')
create_file_name_entry = Entry(create_frame, width=50)
create_file_name_entry.grid(row=0, column=1, padx=5, pady=5)
Label(create_frame, text="Text to write:", bg='#48494a', fg='#edc3ca').grid(row=1, column=0, padx=5, pady=5, sticky='ne')
create_text_entry = Text(create_frame, height=10, width=50)
create_text_entry.grid(row=1, column=1, padx=5, pady=5)
Button(create_frame, text="Write", command=write_to_file, bg='#48494a', fg='#edc3ca').grid(row=2, column=0, columnspan=2, pady=5)
Button(create_frame, text="Back", command=lambda: show_frame(frames["Main"]), bg='#464241', fg='#edc3ca').grid(row=3, column=0, columnspan=2, pady=5)

# Read page
read_frame = frames["Read"]
Label(read_frame, text="Content:", bg='#48494a', fg='#edc3ca').grid(row=0, column=0, padx=5, pady=5, sticky='ne')
read_text_display = Text(read_frame, height=10, width=50)
read_text_display.grid(row=0, column=1, padx=5, pady=5)
read_text_display.config(state='disabled')
Button(read_frame, text="Select File", command=read_from_file, bg='#48494a', fg='#edc3ca').grid(row=1, column=0, columnspan=2, pady=5)
Button(read_frame, text="Back", command=lambda: show_frame(frames["Main"]), bg='#48494a', fg='#edc3ca').grid(row=2, column=0, columnspan=2, pady=5)

# Delete page
delete_frame = frames["Delete"]
Label(delete_frame, text="File name:", bg='#48494a', fg='#edc3ca').grid(row=0, column=0, padx=5, pady=5, sticky='e')
delete_file_name_entry = Entry(delete_frame, width=50)
delete_file_name_entry.grid(row=0, column=1, padx=5, pady=5)
Button(delete_frame, text="Delete", command=delete_file, bg='#48494a', fg='#edc3ca').grid(row=1, column=0, columnspan=2, pady=5)
Button(delete_frame, text="Back", command=lambda: show_frame(frames["Main"]), bg='#48494a', fg='#edc3ca').grid(row=2, column=0, columnspan=2, pady=5)

# Rename page
rename_frame = frames["Rename"]
Label(rename_frame, text="Old file name:", bg='#48494a', fg='#edc3ca').grid(row=0, column=0, padx=5, pady=5, sticky='e')
old_file_name_entry = Entry(rename_frame, width=50)
old_file_name_entry.grid(row=0, column=1, padx=5, pady=5)
Label(rename_frame, text="New file name:", bg='#48494a', fg='#edc3ca').grid(row=1, column=0, padx=5, pady=5, sticky='e')
new_file_name_entry = Entry(rename_frame, width=50)
new_file_name_entry.grid(row=1, column=1, padx=5, pady=5)
Button(rename_frame, text="Rename", command=rename_file, bg='#48494a', fg='#edc3ca').grid(row=2, column=0, columnspan=2, pady=5)
Button(rename_frame, text="Back", command=lambda: show_frame(frames["Main"]), bg='#48494a', fg='#edc3ca').grid(row=3, column=0, columnspan=2, pady=5)

# Analyze page
analyze_frame = frames["Analyze"]
Label(analyze_frame, text="Results:", bg='#48494a', fg='#edc3ca').grid(row=0, column=0, padx=5, pady=5, sticky='ne')
analyze_text_display = Text(analyze_frame, height=10, width=50)
analyze_text_display.grid(row=0, column=1, padx=5, pady=5)
analyze_text_display.config(state='disabled')
Button(analyze_frame, text="Select File", command=analyze_text, bg='#48494a', fg='#edc3ca').grid(row=1, column=0, columnspan=2, pady=5)
Button(analyze_frame, text="Back", command=lambda: show_frame(frames["Main"]), bg='#48494a', fg='#edc3ca').grid(row=2, column=0, columnspan=2, pady=5)

show_frame(frames["Main"])

root.mainloop()
