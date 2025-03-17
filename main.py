from tkinter import *

window = Tk()
window.title("TODO List")
window.minsize(500, 500)

folders = {}
selected_folder = StringVar()
selected_folder.set("None")  # Default value
highest_folder = 0

def delete_task(task):
    if selected_folder.get() == "None":
        return
    # Deleting the object of the task and the task
    folders[selected_folder.get()][0][task].destroy()
    folders[selected_folder.get()][1][task].destroy()
    del folders[selected_folder.get()][0][task]
    del folders[selected_folder.get()][1][task]

def add_task():
    if selected_folder.get() == "None" or inp.get().strip() == "":
        return
    task_name = inp.get()
    if task_name in folders[selected_folder.get()][0]:
        inp.delete(0, END)
        return
    row_pos = len(folders[selected_folder.get()][0]) + 3
    folders[selected_folder.get()][0][task_name] = Label(task_frame, text=task_name)
    folders[selected_folder.get()][0][task_name].grid(row=row_pos, column=0, padx=10, pady=5, sticky="w")

    folders[selected_folder.get()][1][task_name] = Button(task_frame, text="Delete", command=lambda: delete_task(task_name))
    folders[selected_folder.get()][1][task_name].grid(row=row_pos, column=1, padx=10, pady=5)

    inp.delete(0, END)

def delete_folder(folder_name):
    global highest_folder
    if folder_name == "None":
        return
    for widget in folders[folder_name][0].values():
        widget.destroy()
    for widget in folders[folder_name][1].values():
        widget.destroy()
    folders[folder_name][2].destroy()
    del folders[folder_name]
    selected_folder.set("None")

    update_folder_buttons()

def add_folder():
    global highest_folder
    highest_folder += 1
    folder_name = f"Folder {highest_folder}"
    folders[folder_name] = [{}, {}, Button(folder_frame, text=folder_name, command=lambda: select_folder(folder_name))]
    folders[folder_name][2].pack(fill="x", pady=2)
    # Autoselect the new folder
    select_folder(folder_name)
    update_folder_buttons()

def select_folder(folder_name):
    selected_folder.set(folder_name)
    update_tasks()

def update_folder_buttons():
    # Gets rid of all the displayed folders
    for widget in folder_frame.winfo_children():
        widget.destroy()
    # Redisplays all the folders
    for folder_name in folders:
        Button(folder_frame, text=folder_name, command=lambda f=folder_name: select_folder(f)).pack(fill="x", pady=2)
    Button(folder_frame, text="Delete Folder", command=lambda: delete_folder(selected_folder.get())).pack(fill="x", pady=10)

def update_tasks():
    # Gets rid of all the displayed tasks
    for widget in task_frame.winfo_children():
        widget.destroy()
    # Updates the text saying the selected folder
    Label(task_frame, text=f"Tasks for {selected_folder.get()}:", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, pady=5)
    # Goes through all the tasks in folder and displays them
    if selected_folder.get() in folders:
        for idx, task_name in enumerate(folders[selected_folder.get()][0].keys(), start=1):
            Label(task_frame, text=task_name).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            Button(task_frame, text="Delete", command=lambda t=task_name: delete_task(t)).grid(row=idx, column=1, padx=10, pady=5)

# UI Layout
Label(window, text="TODO List", font=("Helvetica", 16)).pack(pady=10)

main_frame = Frame(window)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

folder_frame = Frame(main_frame, relief="solid", borderwidth=1)
folder_frame.pack(side="left", fill="y", padx=10, pady=10)

# Make frame for better categorising
task_frame = Frame(main_frame)
task_frame.pack(side="right", fill="both", expand=True)

inp = Entry(window)
inp.pack(pady=10)

# Buttons for adding tasks/folders
Button(window, text="Add Task", command=add_task).pack(pady=5)
Button(window, text="Add Folder", command=add_folder).pack(pady=5)

# Start with one folder
add_folder()

window.mainloop()
