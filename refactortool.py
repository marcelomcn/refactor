import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os
import autopep8
import pylint.lint
from io import StringIO
import sys
import webbrowser


class RefactorTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window until the unlock code is entered
        self.unlock_code = "R3FACTORV2"  # Set the correct unlock code
        self.warning_window()

    def warning_window(self):
        warning = tk.Toplevel(self.root)
        warning.geometry("450x450")
        warning.title("Warning")

        message = ("Do NOT be fooled! I am a very powerful tool "
                   "for refactoring Python code automatically. "
                   "Proceed with caution! - Developed by Mirko Secchi - www.malagadigital.space")
        label = tk.Label(warning, text=message,
                         wraplength=400, justify="center")
        label.pack(expand=True)

        # Entry field for unlock code
        self.code_entry = tk.Entry(warning, show="*", justify="center")
        self.code_entry.pack(pady=10)

        # Proceed button
        button = tk.Button(warning, text="* UNLOCK *",
                           command=lambda: self.verify_code(warning))
        button.pack(pady=10)

        # Pay button
        pay_button = tk.Button(warning, text="Go to Payment",
                               command=self.open_payment_link)
        pay_button.pack(pady=10)

        # Disable the "X" button to prevent closing the window
        warning.protocol("WM_DELETE_WINDOW", lambda: None)
        warning.mainloop()

    def verify_code(self, warning):
        entered_code = self.code_entry.get()
        if entered_code == self.unlock_code:
            self.open_main_window(warning)
        else:
            messagebox.showerror(
                "Error", "Invalid code. Please enter the correct unlock code.")

    def open_payment_link(self):
        webbrowser.open("https://www.aurawave.eu//_paylink/AZF6KmPZ")

    def open_main_window(self, warning):
        warning.destroy()  # Close the warning window
        self.root.deiconify()  # Show the main window

        # Main Window Setup
        self.root.geometry("500x300")
        self.root.title("Refactoring Tool")

        label = tk.Label(
            self.root, text="Select the folder containing Python code:")
        label.pack(pady=10)

        button = tk.Button(self.root, text="Browse",
                           command=self.select_folder)
        button.pack(pady=10)

        self.folder_path_label = tk.Label(self.root, text="")
        self.folder_path_label.pack(pady=10)

        analyze_button = tk.Button(
            self.root, text="Analyze and Refactor", command=self.refactor_code)
        analyze_button.pack(pady=20)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path
            self.folder_path_label.config(
                text=f"Selected Folder: {folder_path}")

    def refactor_code(self):
        if not hasattr(self, 'folder_path'):
            messagebox.showerror("Error", "Please select a folder first!")
            return

        # Live Log Window
        self.log_window = tk.Toplevel(self.root)
        self.log_window.geometry("600x400")
        self.log_window.title("Live Log")

        self.log_text = scrolledtext.ScrolledText(
            self.log_window, state='disabled', wrap=tk.WORD)
        self.log_text.pack(expand=True, fill=tk.BOTH)

        self.log_message("Starting code refactoring...\n")

        for subdir, _, files in os.walk(self.folder_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(subdir, file)
                    self.log_message(f"Processing {file_path}\n")

                    # Run autopep8 to fix the code
                    fixed_code = autopep8.fix_file(file_path)
                    with open(file_path, 'w') as f:
                        f.write(fixed_code)
                    self.log_message(f"Fixed formatting for {file_path}\n")

                    # Run pylint and capture the output
                    pylint_output = self.run_pylint(file_path)
                    self.log_message(
                        f"Pylint analysis for {file_path}:\n{pylint_output}\n")

        self.log_message("Code refactoring completed!\n")

    def run_pylint(self, file_path):
        """Runs pylint on the given file and captures its output."""
        pylint_output = StringIO()
        sys.stdout = pylint_output  # Redirect stdout to capture pylint's output
        sys.stderr = pylint_output  # Capture stderr as well

        try:
            pylint_opts = [file_path, '--errors-only']
            pylint.lint.Run(pylint_opts)
        except SystemExit:
            pass  # Prevent pylint from calling sys.exit()
        finally:
            sys.stdout = sys.__stdout__  # Reset stdout
            sys.stderr = sys.__stderr__  # Reset stderr

        return pylint_output.getvalue()

    def log_message(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message)
        self.log_text.yview(tk.END)
        self.log_text.config(state='disabled')


if __name__ == "__main__":
    RefactorTool()
