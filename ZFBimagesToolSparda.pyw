import os
import struct
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class Application(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master: tk.Tk = master
        self.pack(anchor="w")
        self.create_widgets()

        # Create frame for header
        self.header_frame = tk.Frame(self.master)
        self.header_frame.pack(anchor="w")

        # Create frame for ZFB File creation
        self.frame = tk.Frame(self.master)
        self.frame.pack(anchor="w")

        # Create bold font for label
        bold_font = ("Helvetica", 10, "bold")
        label_font = ("Helvetica", 10, "normal")

        instructions_text = "Select folder containing image files for bulk ZFB creation"

        # Instructions
        self.header_label = tk.Label(self.header_frame, text=instructions_text, font=bold_font)
        self.header_label.pack()

        # Input Folder - Label
        self.input_folder_label = tk.Label(self.frame, text="Input Folder: ", font=label_font)
        self.input_folder_label.grid(row=1, column=0, sticky="w")

        # Input Folder - Input box
        self.input_folder_var = tk.StringVar()
        self.input_folder_entry = tk.Entry(self.frame, textvariable=self.input_folder_var, width=70)
        self.input_folder_entry.grid(row=1, column=1, sticky="w")

        # Input Folder - Browse button
        self.input_folder_button = tk.Button(self.frame, text="Browse", command=self.select_input_folder)
        self.input_folder_button.grid(row=1, column=2, sticky="w")

        # Output Folder - Label
        self.output_folder_label = tk.Label(self.frame, text="Output Folder: ", font=label_font)
        self.output_folder_label.grid(row=2, column=0, sticky="w")

        # Output Folder - Input box
        self.output_folder_var = tk.StringVar()
        self.output_folder_entry = tk.Entry(self.frame, textvariable=self.output_folder_var, width=70)
        self.output_folder_entry.grid(row=2, column=1, sticky="w")

        # Output Folder - Browse button
        self.output_folder_button = tk.Button(self.frame, text="Browse", command=self.select_output_folder)
        self.output_folder_button.grid(row=2, column=2, sticky="w")

        # Core Label
        self.core_label = tk.Label(self.frame, text="CORE: ", font=label_font)
        self.core_label.grid(row=3, column=0, sticky="w")

        # Core Input box
        self.core_var = tk.StringVar()
        self.core_entry = tk.Entry(self.frame, textvariable=self.core_var, width=70)
        self.core_entry.grid(row=3, column=1, sticky="w")

        # Extension Label
        self.extension_label = tk.Label(self.frame, text="EXTENSION: ", font=label_font)
        self.extension_label.grid(row=4, column=0, sticky="w")

        # Extension Input box
        self.extension_var = tk.StringVar()
        self.extension_entry = tk.Entry(self.frame, textvariable=self.extension_var, width=70)
        self.extension_entry.grid(row=4, column=1, sticky="w")

        # Create ZFB Files button
        self.create_zfb_button = tk.Button(self.frame, text="Create ZFB Files", command=self.create_zfb_files,
                                           font=("Helvetica", 14))
        self.create_zfb_button.grid(row=5, column=0, sticky="w", columnspan=3)

    def create_widgets(self):
        # Menu bar creation
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.exit_handler)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.master.config(menu=self.menubar)

    def exit_handler(self):
        os._exit(0)

    def select_input_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.input_folder_var.set(folder_path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder_var.set(folder_path)

    def create_zfb_files(self):
        try:
            input_folder = self.input_folder_var.get()
            output_folder = self.output_folder_var.get()
            core = self.core_var.get()
            extension = self.extension_var.get()

            # Check if folders are selected
            if not input_folder or not output_folder or not core or not extension:
                messagebox.showwarning('Warning', 'Please fill in all the fields and select input and output folders.')
                return

            thumb_size = (144, 208)

            # Iterate over all files in the input folder
            for file_name in os.listdir(input_folder):
                file_path = os.path.join(input_folder, file_name)

                if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    # Process the image file and create the .zfb file
                    with Image.open(file_path) as img:
                        img = img.resize(thumb_size)
                        img = img.convert("RGB")

                        raw_data = []

                        # Convert image to RGB565
                        for y in range(thumb_size[1]):
                            for x in range(thumb_size[0]):
                                r, g, b = img.getpixel((x, y))
                                rgb = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
                                raw_data.append(struct.pack('H', rgb))

                        raw_data_bytes = b''.join(raw_data)

                        # Create .zfb filename
                        zfb_filename = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.zfb')

                        # Write the image data to the .zfb file
                        with open(zfb_filename, 'wb') as zfb:
                            zfb.write(raw_data_bytes)
                            zfb.write(b'\x00\x00\x00\x00')  # Write four 00 bytes
                            zfb.write(f"{core};{os.path.splitext(file_name)[0]}.{extension}.gba".encode('utf-8'))  # Write the modified filename
                            zfb.write(b'\x00\x00')  # Write two 00 bytes

            messagebox.showinfo('Success', 'ZFB files created successfully.')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while creating the ZFB files: {str(e)}')


# Create the application window
root = tk.Tk()
root.geometry("630x260")
root.resizable(False, False)
root.title("ZFBSpardaTool")

app = Application(master=root)

# Redefine the window's close button to trigger the custom exit handler
root.protocol("WM_DELETE_WINDOW", app.exit_handler)

# Start the application
app.mainloop()