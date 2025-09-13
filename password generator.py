import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

# Background color
BG_COLOR = "#f0f4f8"  # Light bluish-gray

# Helper function to generate password
def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            raise ValueError("Password length must be at least 4.")

        use_upper = upper_var.get()
        use_lower = lower_var.get()
        use_digits = digits_var.get()
        use_symbols = symbols_var.get()
        exclude_similar = exclude_var.get()

        character_sets = []
        password_chars = []

        if use_lower:
            chars = string.ascii_lowercase
            if exclude_similar:
                chars = chars.replace('l', '')
            character_sets.append(chars)
        if use_upper:
            chars = string.ascii_uppercase
            if exclude_similar:
                chars = chars.replace('I', '').replace('O', '')
            character_sets.append(chars)
        if use_digits:
            chars = string.digits
            if exclude_similar:
                chars = chars.replace('0', '').replace('1', '')
            character_sets.append(chars)
        if use_symbols:
            chars = string.punctuation
            character_sets.append(chars)

        if not character_sets:
            messagebox.showerror("Error", "Select at least one character type.")
            return

        for chars in character_sets:
            password_chars.append(random.choice(chars))

        all_chars = ''.join(character_sets)
        while len(password_chars) < length:
            password_chars.append(random.choice(all_chars))

        random.shuffle(password_chars)
        final_password = ''.join(password_chars)
        password_var.set(final_password)
        update_strength(length, len(character_sets))

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def copy_to_clipboard():
    password = password_var.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def update_strength(length, char_types):
    score = length + (char_types * 2)
    if score < 10:
        strength = "Weak"
        color = "red"
    elif score < 16:
        strength = "Medium"
        color = "orange"
    else:
        strength = "Strong"
        color = "green"

    strength_label.config(text=f"Strength: {strength}", fg=color)

# --- GUI Setup ---
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x450")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# Password output
password_var = tk.StringVar()
tk.Label(root, text="Generated Password:", bg=BG_COLOR).pack(pady=5)
tk.Entry(root, textvariable=password_var, font=("Courier", 12), width=30, justify="center").pack(pady=5)
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=5)

# Length input
tk.Label(root, text="Password Length:", bg=BG_COLOR).pack(pady=5)
length_entry = tk.Entry(root)
length_entry.insert(0, "12")
length_entry.pack(pady=5)

# Character set options
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
exclude_var = tk.BooleanVar()

# Create checkbuttons with background
options_frame = tk.Frame(root, bg=BG_COLOR)
options_frame.pack(pady=10)

tk.Checkbutton(options_frame, text="Include Uppercase Letters", variable=upper_var, bg=BG_COLOR).pack(anchor='w')
tk.Checkbutton(options_frame, text="Include Lowercase Letters", variable=lower_var, bg=BG_COLOR).pack(anchor='w')
tk.Checkbutton(options_frame, text="Include Numbers", variable=digits_var, bg=BG_COLOR).pack(anchor='w')
tk.Checkbutton(options_frame, text="Include Symbols", variable=symbols_var, bg=BG_COLOR).pack(anchor='w')
tk.Checkbutton(options_frame, text="Exclude Similar Characters (1, l, O, 0)", variable=exclude_var, bg=BG_COLOR).pack(anchor='w')

# Generate button
tk.Button(root, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white").pack(pady=10)

# Strength label
strength_label = tk.Label(root, text="Strength: ", font=("Arial", 10, "bold"), bg=BG_COLOR)
strength_label.pack()

# Run the GUI
root.mainloop()
