import os
import struct
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from collections import namedtuple
from tkinter import ttk
import threading

class ZFBimagesTool(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.stop_flag = threading.Event()

        # --- Tamaños de imagen ---
        self.ImageSize = namedtuple('ImageSize', [
            "hyper_width", "hyper_height", 
            "default_width", "default_height", 
            "init_width", "init_height"
        ])
        self.img = self.ImageSize(
            hyper_width="640", hyper_height="480", 
            default_width="144", default_height="208", 
            init_width="144", init_height="208"
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

        # Checkbox ARCADE
        self.arcade_var = tk.BooleanVar(value=False)
        self.arcade_checkbutton = tk.Checkbutton(
            self.master, text="ARCADE", variable=self.arcade_var, command=self.toggle_arcade, font=label_font
        )
        self.arcade_checkbutton.grid(row=3, column=0, columnspan=2, sticky="w", padx=10)

        # Core y Extension
        self.create_core_and_extension(label_font)

        # Tamaño de imagen
        self.create_image_size_widgets(label_font)

        # Botón para crear archivos ZFB
        self.create_zfb_button = tk.Button(
            self.master, text="Create ZFB Files", command=self.execute_create_zfb, font=("Helvetica", 14)
        )
        self.create_zfb_button.grid(row=7, column=0, columnspan=7, pady=10)

        # Botón de STOP
        self.stop_button = tk.Button(
            self.master, text="STOP", command=self.stop_processing, font=("Helvetica", 14), fg="red"
        )
        self.stop_button.grid(row=7, column=4, columnspan=2, pady=10)
        self.stop_button["state"] = "disabled"

        # Mensajes de estado
        self.msg_var = tk.StringVar()
        tk.Label(self.master, textvariable=self.msg_var, fg="green", font=label_font).grid(row=8, column=0, columnspan=7, sticky="w", padx=10)

        # Barra de progreso
        self.progress = ttk.Progressbar(self.master, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=9, column=0, columnspan=7, padx=10, pady=5, sticky="ew")

        # Inicialización de valores predeterminados
        c_dir = os.getcwd()
        self.master.bind("<Return>", self.entry_enter_key)
        self.input_folder_var_entry.focus_set()
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

    def disable_inputs(self):
        # Entradas
        self.input_folder_var_entry.config(state="disabled")
        self.output_folder_var_entry.config(state="disabled")
        self.core_entry.config(state="disabled")
        self.extension_entry.config(state="disabled")
        self.imgwidth_entry.config(state="disabled")
        self.imgheight_entry.config(state="disabled")

        # Botones
        self.input_folder_var_button.config(state="disabled")
        self.output_folder_var_button.config(state="disabled")
        self.arcade_checkbutton.config(state="disabled")
        self.hyperscreen_checkbox.config(state="disabled")

        # Radio buttons
        for child in self.master.grid_slaves():
            if isinstance(child, tk.Radiobutton):
                child.config(state="disabled")

    def enable_inputs(self):
        # Entradas
        self.input_folder_var_entry.config(state="normal")
        self.output_folder_var_entry.config(state="normal")
        self.core_entry.config(state="normal")
        self.extension_entry.config(state="normal")
        self.imgwidth_entry.config(state="normal")
        self.imgheight_entry.config(state="normal")

        # Botones
        self.input_folder_var_button.config(state="normal")
        self.output_folder_var_button.config(state="normal")
        self.arcade_checkbutton.config(state="normal")
        self.hyperscreen_checkbox.config(state="normal")

        # Radio buttons
        for child in self.master.grid_slaves():
            if isinstance(child, tk.Radiobutton):
                child.config(state="normal")

    def stop_processing(self):
        self.stop_flag.set()
        self.msg_var.set("Stopping...")

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
        #self.core_var.trace_add("write", self.core_input_callback)
        self.core_label = tk.Label(self.master, text="CORE:", font=label_font)
        self.core_label.grid(row=4, column=0, sticky="w", padx=10)
        self.core_entry = tk.Entry(self.master, textvariable=self.core_var, width=10)
        self.core_entry.grid(row=4, column=1, sticky="w", padx=6)

        # EXTENSION
        self.extension_frame = tk.Frame(self.master, bd=0, relief="flat")
        self.extension_frame.grid(row=4, column=2, columnspan=3, sticky="w")
        self.extension_var = tk.StringVar()
        self.extension_label = tk.Label(self.extension_frame, text="EXTENSION:", font=label_font)
        self.extension_label.grid(row=0, column=0, sticky="w", padx=5)
        self.extension_entry = tk.Entry(self.extension_frame, textvariable=self.extension_var, width=10)
        self.extension_entry.grid(row=0, column=1, columnspan=2, sticky="w", padx=15)

    def create_image_size_widgets(self, label_font):
        self.img_mode = tk.StringVar(value="auto")
        auto_rb = tk.Radiobutton(
            self.master, text="auto",
            variable=self.img_mode, value="auto", command=self.toggle_img_mode,
            font=label_font
        )
        auto_rb.grid(row=5, column=1, sticky="w", padx=5)
        manual_rb = tk.Radiobutton(
            self.master, text="manual",
            variable=self.img_mode, value="manual", command=self.toggle_img_mode,
            font=label_font
        )
        manual_rb.grid(row=5, column=2, sticky="w")

        self.img_size_var = tk.StringVar()
        tk.Label(self.master, textvariable=self.img_size_var, fg="green", anchor="w").grid(row=5, column=3, columnspan=3, sticky="ew")

        self.img_mode_frame = tk.Frame(self.master)
        self.img_mode_frame.grid(row=6, column=1, columnspan=5, sticky="w", padx=5)

        self.imgwidth_var = tk.StringVar(value=self.img.init_width)
        self.imgheight_var = tk.StringVar(value=self.img.init_height)
        self.img_hyperscreen_var = tk.BooleanVar(value=True)

        tk.Label(self.master, text="Image Size:", font=label_font).grid(row=5, column=0, sticky="w", padx=10)
        self.imgwidth_entry = tk.Entry(self.img_mode_frame, textvariable=self.imgwidth_var, width=10, font=label_font)
        self.imgwidth_entry.grid(row=0, column=0, sticky="w", padx=(2, 0))
        self.imgwidth_var.trace_add("write", self.imgsize_input_callback)
        tk.Label(self.img_mode_frame, text="x", font=label_font).grid(row=0, column=1, sticky="w", padx=3)
        self.imgheight_entry = tk.Entry(self.img_mode_frame, textvariable=self.imgheight_var, width=10, font=label_font)
        self.imgheight_entry.grid(row=0, column=2, sticky="w")
        self.imgheight_var.trace_add("write", self.imgsize_input_callback)

        # Checkbox HyperScreen
        self.hyperscreen_checkbox = tk.Checkbutton(
            self.img_mode_frame, text="HyperScreen", variable=self.img_hyperscreen_var, command=self.toggle_hyperscreen, font=label_font
        )
        self.hyperscreen_checkbox.grid(row=0, column=3, sticky="w", padx=15)
        self.toggle_img_mode()

    def entry_enter_key(self, event):
        if event.keysym == "Return":
            focused_widget = self.master.focus_get()
            if focused_widget["state"] == "disabled":
                return
            if focused_widget == self.input_folder_var_entry:
                self.output_folder_var_entry.focus_set()
            if focused_widget == self.output_folder_var_entry:
                self.arcade_checkbutton.focus_set()
            if focused_widget == self.arcade_checkbutton:
                if self.arcade_var.get():
                    self.create_zfb_button.focus_set()
                else:
                    self.core_entry.focus_set()
            if focused_widget == self.core_entry:
                self.extension_entry.focus_set()
            if focused_widget == self.extension_entry:
                self.create_zfb_button.focus_set()
            if focused_widget == self.imgwidth_entry:
                self.imgheight_entry.focus_set()
            if focused_widget == self.imgheight_entry:
                self.create_zfb_button.focus_set()
            if focused_widget == self.create_zfb_button:
                self.execute_create_zfb()
            if focused_widget == self.stop_button:
                self.stop_processing()

    def core_input_callback(self, *args):
        self.extension_var.set(self.core_var.get())

    def imgsize_input_callback(self, *args):
        self.img_hyperscreen_var.set(self.check_image_size())

    def check_image_size(self, img_size=None):
        arg_provided = (img_size is not None)

        width = 0
        height = 0
        if img_size is None:
            try:
                width = int(self.imgwidth_var.get() or 0)
            except ValueError:
                self.imgwidth_var.set("0")
                return False

            try:
                height = int(self.imgheight_var.get() or 0)
            except ValueError:
                self.imgheight_var.set("0")
                return False

            img_size = (width, height)
        else:
            self.imgwidth_var.set(str(img_size[0]))
            self.imgheight_var.set(str(img_size[1]))

        if img_size[0] == int(self.img.default_width) and img_size[1] == int(self.img.default_height):
            mode = 0
        elif img_size[0] >= 360 or img_size[1] >= 360:
            mode = 1
        else:
            mode = 2

        size_txt = "(" + str(img_size[0]) + " x " + str(img_size[1]) + " ["
        if mode == 1:
            size_txt += "HyperScreen"
        elif mode == 2:
            size_txt += "Custom"
        else:
            size_txt += "Default"
        size_txt += "])"

        if arg_provided or self.img_mode.get() != "auto":
            self.img_size_var.set(size_txt)

        return mode == 1

    def toggle_img_mode(self):
        if self.img_mode.get() == "manual":
            self.img_mode_frame.grid()
            self.check_image_size()
        else:
            self.img_mode_frame.grid_remove()
            self.img_size_var.set("")

    def toggle_hyperscreen(self):
        if self.img_hyperscreen_var.get():
            self.imgwidth_var.set(self.img.hyper_width)
            self.imgheight_var.set(self.img.hyper_height)
        else:
            self.imgwidth_var.set(self.img.default_width)
            self.imgheight_var.set(self.img.default_height)
        self.check_image_size()

    def toggle_arcade(self):
        if self.arcade_var.get():
            # Ocultar los campos CORE y EXTENSION
            self.core_entry.grid_remove()
            self.extension_entry.grid_remove()
            self.core_label.grid_remove()
            self.extension_label.grid_remove()
            self.extension_frame.grid_remove()
        else:
            # Mostrar los campos CORE y EXTENSION
            self.core_entry.grid()
            self.extension_entry.grid()
            self.core_label.grid()
            self.extension_label.grid()
            self.extension_frame.grid()


    def execute_create_zfb(self):
        if self.img_mode.get() == "manual":
            try:
                width = int(self.imgwidth_var.get())
                height = int(self.imgheight_var.get())
                if width < int(self.img.default_width) or height < int(self.img.default_height):
                    messagebox.showerror("Image Size Error", "Image size must be at least " + self.img.default_width + " x " + self.img.default_height + ".")
                    return
                if width > int(self.img.hyper_width) or height > int(self.img.hyper_height):
                    messagebox.showerror("Image Size Error", "Image size must be at most " + self.img.hyper_width + " x " + self.img.hyper_height + ".")
                    return
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numeric values for image size.")
                return

        self.stop_flag.clear()
        thread = threading.Thread(
            target=lambda: self.process_zfb_files(arcade_mode=self.arcade_var.get())
        )
        thread.start()

    def process_zfb_files(self, arcade_mode=False):
        try:
            input_folder = self.input_folder_var.get()
            output_folder = self.output_folder_var.get()
            core = self.core_var.get()
            extension = self.extension_var.get()

            if not input_folder or not output_folder or (not arcade_mode and (not core or not extension)):
                messagebox.showwarning('Warning', 'Please fill in all the fields and select input and output folders.')
                return

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            self.disable_inputs()
            self.create_zfb_button["state"] = "disabled"
            self.stop_button["state"] = "normal"

            files = os.listdir(input_folder)
            total_files = len(files)
            self.progress["maximum"] = total_files
            self.progress["value"] = 0
            self.master.update()

            image_files_found = False

            for idx, file_name in enumerate(files):
                if self.stop_flag.is_set():
                    self.msg_var.set("Process canceled.")
                    break

                file_path = os.path.join(input_folder, file_name)
                zfb_filename = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.zfb')

                try:
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        with Image.open(file_path) as img:
                            # Mostrar nombre del archivo siempre, sin importar el modo
                            self.msg_var.set(f"Processing file: {os.path.splitext(file_name)[0]}")

                            if self.img_mode.get() == "auto":
                                img_w, img_h = img.size
                                if img_w < int(self.img.default_width) or img_h < int(self.img.default_height):
                                    img_w, img_h = int(self.img.default_width), int(self.img.default_height)
                                elif img_w > int(self.img.hyper_width) or img_h > int(self.img.hyper_height):
                                    img_w, img_h = int(self.img.hyper_width), int(self.img.hyper_height)

                                self.img_hyperscreen_var.set(self.check_image_size((img_w, img_h)))
                            else:
                                img_w = int(self.imgwidth_var.get())
                                img_h = int(self.imgheight_var.get())


                            img = img.resize((img_w, img_h)).convert("RGB")

                            raw_data = []
                            for y in range(img_h):
                                for x in range(img_w):
                                    r, g, b = img.getpixel((x, y))
                                    rgb = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
                                    raw_data.append(struct.pack('H', rgb))

                            raw_data_bytes = b''.join(raw_data)

                        with open(zfb_filename, 'wb') as zfb:
                            zfb.write(raw_data_bytes)
                            zfb.write(b'\x00\x00\x00\x00')

                            if arcade_mode:
                                zfb.write(f"{os.path.splitext(file_name)[0]}.zip".encode('utf-8'))
                            else:
                                zfb.write(f"{core};{os.path.splitext(file_name)[0]}.{extension}.gba".encode('utf-8'))

                            zfb.write(b'\x00\x00')

                        image_files_found = True

                    else:
                        with open(zfb_filename, 'wb') as zfb:
                            if arcade_mode:
                                zfb.write(b'\xFF' * 0xEA00)
                            else:
                                zfb.write(b'\x00' * 0xEA00)

                            zfb.write(b'\x00\x00\x00\x00')
                            if arcade_mode:
                                zfb.write(f"{os.path.splitext(file_name)[0]}.zip".encode('utf-8'))
                            else:
                                zfb.write(f"{core};{os.path.splitext(file_name)[0]}.{os.path.splitext(file_name)[1][1:]}.gba".encode('utf-8'))
                            zfb.write(b'\x00\x00')

                except Exception as e:
                    print(f"Error with {file_name}: {e}")

                self.progress["value"] = idx + 1
                self.master.update_idletasks()
                self.master.update()

            self.msg_var.set("")
            if not self.stop_flag.is_set():
                if arcade_mode and not image_files_found:
                    messagebox.showwarning('Warning', 'No image files found. Non-image files are copied to the output folder.')
                else:
                    messagebox.showinfo('Success', 'ZFB files created successfully.')

        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')

        self.enable_inputs()    
        self.create_zfb_button["state"] = "normal"
        self.stop_button["state"] = "disabled"
        self.progress["value"] = 0
        self.msg_var.set("")

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
    root.title("ZFB Generator Hyper")
    app = ZFBimagesTool(master=root)
    root.mainloop()
