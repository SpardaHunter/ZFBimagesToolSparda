import os
import struct
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from collections import namedtuple


class ZFBimagesTool(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # --- Tamaños de imagen ---
        self.ImageSize = namedtuple('ImageSize', [
            "full_width", "full_height", 
            "default_width", "default_height", 
            "init_width", "init_height"
        ])
        self.img = self.ImageSize(
            full_width="640", full_height="480", 
            default_width="144", default_height="208", 
            init_width="640", init_height="480"
        )

        # Crear la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Fuentes
        bold_font = ("Helvetica", 10, "bold")
        label_font = ("Helvetica", 10, "normal")

        # Input Folder
        self.create_label_entry(
            row=1, label_text="Input Folder:", var_name="input_folder_var", 
            button_text="Browse", button_command=self.select_input_folder, label_font=label_font
        )

        # Output Folder
        self.create_label_entry(
            row=2, label_text="Output Folder:", var_name="output_folder_var", 
            button_text="Browse", button_command=self.select_output_folder, label_font=label_font
        )

        # Core y Extension
        self.create_core_and_extension(label_font)

        # Checkbox ARCADE
        self.arcade_var = tk.BooleanVar(value=False)
        self.arcade_checkbutton = tk.Checkbutton(
            self.master, text="ARCADE", variable=self.arcade_var, command=self.toggle_arcade
        )
        self.arcade_checkbutton.grid(row=4, column=0, columnspan=2, sticky="w", padx=10)

        # Tamaño de imagen
        self.create_image_size_widgets(label_font)

        # Botón para crear archivos ZFB
        self.create_zfb_button = tk.Button(
            self.master, text="Create ZFB Files", command=self.execute_create_zfb, font=("Helvetica", 14)
        )
        self.create_zfb_button.grid(row=6, column=0, columnspan=7, pady=10)

        # Mensajes de estado
        self.msg_var = tk.StringVar()
        tk.Label(self.master, textvariable=self.msg_var, font=label_font).grid(row=7, column=0, columnspan=7, sticky="w", padx=10)

        # Inicialización de valores predeterminados
        c_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_folder_var.set(c_dir)
        self.output_folder_var.set(os.path.join(c_dir, "output"))
        self.imgwidth_var.set(self.img.init_width)
        self.imgheight_var.set(self.img.init_height)

        # Configuración del grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def create_label_entry(self, row, label_text, var_name, button_text, button_command, label_font):
        tk.Label(self.master, text=label_text, font=label_font).grid(row=row, column=0, sticky="w", padx=10)
        
        var = tk.StringVar()
        setattr(self, var_name, var)

        entry = tk.Entry(self.master, textvariable=var, width=70)
        setattr(self, f"{var_name}_entry", entry)
        entry.grid(row=row, column=1, columnspan=5, sticky="w", padx=5)

        button = tk.Button(self.master, text=button_text, command=button_command)
        setattr(self, f"{var_name}_button", button)
        button.grid(row=row, column=6, sticky="w")

    def create_core_and_extension(self, label_font):
        # CORE
        self.core_var = tk.StringVar()
        self.core_label = tk.Label(self.master, text="CORE:", font=label_font)
        self.core_label.grid(row=3, column=0, sticky="w", padx=10)
        self.core_entry = tk.Entry(self.master, textvariable=self.core_var, width=10)
        self.core_entry.grid(row=3, column=1, sticky="w", padx=5)
    
        # EXTENSION
        self.extension_var = tk.StringVar()
        self.extension_label = tk.Label(self.master, text="EXTENSION:", font=label_font)
        self.extension_label.grid(row=3, column=2, sticky="w", padx=5)
        self.extension_entry = tk.Entry(self.master, textvariable=self.extension_var, width=10)
        self.extension_entry.grid(row=3, column=3, sticky="w", padx=5)


    def create_image_size_widgets(self, label_font):
        self.imgwidth_var = tk.StringVar(value=self.img.init_width)
        self.imgheight_var = tk.StringVar(value=self.img.init_height)
        self.img_fullscreen_var = tk.BooleanVar(value=True)
    
        tk.Label(self.master, text="Image Size:", font=label_font).grid(row=5, column=0, sticky="w", padx=10)
        self.imgwidth_entry = tk.Entry(self.master, textvariable=self.imgwidth_var, width=10)
        self.imgwidth_entry.grid(row=5, column=1, sticky="w", padx=5)
        tk.Label(self.master, text="x", font=label_font).grid(row=5, column=2, sticky="w")
        self.imgheight_entry = tk.Entry(self.master, textvariable=self.imgheight_var, width=10)
        self.imgheight_entry.grid(row=5, column=3, sticky="w", padx=5)
    
        # Checkbox Fullscreen
        self.fullscreen_checkbox = tk.Checkbutton(
            self.master, text="Fullscreen", variable=self.img_fullscreen_var, command=self.toggle_fullscreen
        )
        self.fullscreen_checkbox.grid(row=5, column=4, sticky="w", padx=10)


    def toggle_fullscreen(self):
        if self.img_fullscreen_var.get():
            self.imgwidth_var.set(self.img.full_width)
            self.imgheight_var.set(self.img.full_height)
        else:
            self.imgwidth_var.set(self.img.default_width)
            self.imgheight_var.set(self.img.default_height)

    def toggle_arcade(self):
        if self.arcade_var.get():
            # Ocultar los campos CORE y EXTENSION
            self.core_entry.grid_remove()
            self.extension_entry.grid_remove()
            self.core_label.grid_remove()
            self.extension_label.grid_remove()
        else:
            # Mostrar los campos CORE y EXTENSION
            self.core_entry.grid()
            self.extension_entry.grid()
            self.core_label.grid()
            self.extension_label.grid()


    def execute_create_zfb(self):
        if self.arcade_var.get():
            self.create_zfb_files_ARCADE()
        else:
            self.create_zfb_files()

    def create_zfb_files(self):
        try:
            input_folder = self.input_folder_var.get()
            output_folder = self.output_folder_var.get()
            core = self.core_var.get()
            extension = self.extension_var.get()
        #--- Q_ta mod ------------------------------------------------------------------
            img_w = self.imgwidth_var.get()
            img_h = self.imgheight_var.get()
        #-------------------------------------------------------------------------------

            # Check if folders are selected
            #if not input_folder or not output_folder or not core or not extension:
            if not input_folder or not output_folder or not core or not extension or not img_w or not img_h:
                messagebox.showwarning('Warning', 'Please fill in all the fields and select input and output folders.')
                return

        #--- Q_ta mod ------------------------------------------------------------------
            #thumb_size = (640, 480)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            thumb_size = (int(img_w), int(img_h))
            self.msg_var.set("processing ... ")
            self.create_zfb_button["state"] = "disabled"
            root.update()
        #-------------------------------------------------------------------------------

            # Iterate over all files in the input folder
            for file_name in os.listdir(input_folder):
                file_path = os.path.join(input_folder, file_name)

                try:
                    # Attempt to open the file as an image
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
                            # Fill with 00 bytes until offset 0xEA00
                            zfb.write(raw_data_bytes)
                            zfb.write(b'\x00\x00\x00\x00')  # Write four 00 bytes
                            zfb.write(f"{core};{os.path.splitext(file_name)[0]}.{extension}.gba".encode('utf-8'))  # Write the modified filename
                            zfb.write(b'\x00\x00')  # Write two 00 bytes

                except Exception as img_error:
                    # Create a placeholder .zfb file if the file is not a recognized image
                    placeholder_data = b'\x00' * 0xEA00 + b'\x00\x00\x00\x00' + f"{core};{os.path.splitext(file_name)[0]}.{os.path.splitext(file_name)[1][1:]}.gba".encode('utf-8') + b'\x00\x00'
                    zfb_filename = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.zfb')
                    with open(zfb_filename, 'wb') as zfb:
                        zfb.write(placeholder_data)

        #--- Q_ta mod ------------------------------------------------------------------
            self.msg_var.set("")
        #-------------------------------------------------------------------------------
            messagebox.showinfo('Success', 'ZFB files created successfully.')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred while creating the ZFB files: {str(e)}')

        #--- Q_ta mod ------------------------------------------------------------------
        self.create_zfb_button["state"] = "normal"
        self.msg_var.set("")
        #-------------------------------------------------------------------------------
        pass

    def create_zfb_files_ARCADE(self):
        try:
            input_folder = self.input_folder_var.get()
            output_folder = self.output_folder_var.get()
        #--- Q_ta mod ------------------------------------------------------------------
            img_w = self.imgwidth_var.get()
            img_h = self.imgheight_var.get()
        #-------------------------------------------------------------------------------

    
            # Check if folders are selected
            #if not input_folder or not output_folder:
            if not input_folder or not output_folder or not img_w or not img_h:
                messagebox.showwarning('Warning', 'Please fill in all the fields and select input and output folders.')
                return

        #--- Q_ta mod ------------------------------------------------------------------
            #thumb_size = (640, 480)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            thumb_size = (int(img_w), int(img_h))
            self.msg_var.set("processing ... ")
            self.create_zfb_button["state"] = "disabled"
            root.update()
        #-------------------------------------------------------------------------------

            # Keep track of whether any image files were found
            image_files_found = False

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
                        zfb.write(f"{os.path.splitext(file_name)[0]}.zip".encode('utf-8'))  # Write the modified filename
                        zfb.write(b'\x00\x00')  # Write two 00 bytes

                    image_files_found = True

                else:
                    # This block should be inside the loop
                    # Create .zfb filename
                    zfb_filename = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.zfb')

                    # Write the image data to the .zfb file
                    with open(zfb_filename, 'wb') as zfb:
                        zfb.write(b'\xFF' * 0xEA00)
                        zfb.write(b'\x00\x00\x00\x00')  # Write four 00 bytes
                        zfb.write(f"{os.path.splitext(file_name)[0]}.zip".encode('utf-8'))  # Write the modified filename
                        zfb.write(b'\x00\x00')  # Write two 00 bytes

        #--- Q_ta mod ------------------------------------------------------------------
            self.msg_var.set("")
        #-------------------------------------------------------------------------------
            if image_files_found:
                messagebox.showinfo('Success', 'ZFB files created successfully.')
            else:
                messagebox.showwarning('Warning', 'No image files found. Non-image files are copied to the output folder.')

        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')

        #--- Q_ta mod ------------------------------------------------------------------
        self.create_zfb_button["state"] = "normal"
        self.msg_var.set("")
        #-------------------------------------------------------------------------------
        pass

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder_var.set(folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder_var.set(folder)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x300")
    root.resizable(False, False)
    root.title("ZFB Generator")
    app = ZFBimagesTool(master=root)
    root.mainloop()
