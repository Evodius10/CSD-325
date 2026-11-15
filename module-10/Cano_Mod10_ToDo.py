"""CSD-325 Module 10: modified scrolling Tkinter to-do list.

Based on David Love, Tkinter By Example, Listing 2.2 (Chapter 2).
Enter a task and press Enter to add it. Right-click a task to delete it.
"""

import tkinter as tk
from tkinter import messagebox as msg


class Todo(tk.Tk):
    def __init__(self, tasks=None):
        super().__init__()
        self.tasks = []
        self.title("Cano-ToDo")
        self.geometry("410x500")
        self.minsize(320, 340)

        # Complementary blue and orange task backgrounds.
        self.colour_schemes = [
            {"bg": "#DDECF9", "fg": "#17324D"},
            {"bg": "#FBE5CC", "fg": "#5C3414"},
        ]

        # File -> Exit properly closes the application.
        menu_bar = tk.Frame(self, bg="#E8EEF4", padx=8, pady=3)
        menu_bar.pack(side=tk.TOP, fill=tk.X)
        file_button = tk.Menubutton(
            menu_bar, text="File", bg="#E8EEF4", fg="#17324D", relief=tk.FLAT,
            activebackground="#DDECF9", padx=8, pady=3,
        )
        file_button.pack(side=tk.LEFT)
        file_menu = tk.Menu(file_button, tearoff=0)
        file_menu.add_command(label="Exit", command=self.destroy)
        file_button.configure(menu=file_menu)

        instructions = tk.Label(
            self,
            text="Enter a task below and press Enter. Right-click a task to delete it.",
            wraplength=370,
            justify=tk.CENTER,
            bg="#17324D",
            fg="white",
            padx=12,
            pady=14,
        )
        instructions.pack(side=tk.TOP, fill=tk.X)

        list_container = tk.Frame(self)
        list_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tasks_canvas = tk.Canvas(list_container, bg="#F5F7FA", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(
            list_container, orient="vertical", command=self.tasks_canvas.yview
        )
        self.tasks_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tasks_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tasks_frame = tk.Frame(self.tasks_canvas, bg="#F5F7FA")
        self.canvas_frame = self.tasks_canvas.create_window(
            (0, 0), window=self.tasks_frame, anchor="nw"
        )
        self.tasks_frame.bind("<Configure>", self.on_frame_configure)
        self.tasks_canvas.bind("<Configure>", self.task_width)

        text_frame = tk.Frame(self, bg="#F5F7FA", padx=12, pady=12)
        text_frame.pack(side=tk.BOTTOM, fill=tk.X)
        tk.Label(text_frame, text="New task:", bg="#F5F7FA").pack(anchor="w")
        self.task_create = tk.Text(text_frame, height=2, bg="white", fg="black", wrap="word")
        self.task_create.pack(fill=tk.X)
        tk.Button(text_frame, text="Add Task", command=self.add_task, bg="#17324D", fg="white").pack(
            fill=tk.X, pady=(8, 0)
        )
        self.task_create.bind("<Return>", self.add_task)

        self.tasks_canvas.bind_all("<MouseWheel>", self.mouse_scroll)
        self.tasks_canvas.bind_all("<Button-4>", self.mouse_scroll)
        self.tasks_canvas.bind_all("<Button-5>", self.mouse_scroll)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.task_create.focus_set()

        # Used only when initial tasks are explicitly provided.
        for task in tasks or []:
            self.add_task(task_text=task)

    def add_task(self, event=None, task_text=None):
        text = (task_text if task_text is not None else self.task_create.get("1.0", tk.END)).strip()
        if text:
            task = tk.Label(self.tasks_frame, text=text, padx=12, pady=12, anchor="w", justify="left")
            self.set_task_colour(len(self.tasks), task)
            task.bind("<Button-3>", self.remove_task)
            task.pack(side=tk.TOP, fill=tk.X, pady=(0, 2))
            self.tasks.append(task)
        if task_text is None:
            self.task_create.delete("1.0", tk.END)
        return "break" if event is not None else None

    def remove_task(self, event):
        task = event.widget
        if task not in self.tasks:
            return
        if msg.askyesno("Really Delete?", f"Delete {task.cget('text')}?", parent=self):
            self.tasks.remove(task)
            task.destroy()
            self.recolour_tasks()
            self.on_frame_configure()

    def recolour_tasks(self):
        for position, task in enumerate(self.tasks):
            self.set_task_colour(position, task)

    def set_task_colour(self, position, task):
        colours = self.colour_schemes[position % 2]
        task.configure(bg=colours["bg"], fg=colours["fg"])

    def on_frame_configure(self, event=None):
        self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all"))

    def task_width(self, event):
        self.tasks_canvas.itemconfig(self.canvas_frame, width=event.width)

    def mouse_scroll(self, event):
        if event.delta:
            amount = -int(event.delta / 120) if abs(event.delta) >= 120 else (-1 if event.delta > 0 else 1)
        else:
            amount = 1 if event.num == 5 else -1
        self.tasks_canvas.yview_scroll(amount, "units")


if __name__ == "__main__":
    todo = Todo()
    todo.mainloop()
