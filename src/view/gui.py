import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import ttkbootstrap as ttk
from ..utils.aux_functions import fila_log
import queue


class GUI(ttk.Window):
    def __init__(self, themename):
        super().__init__(themename=themename)

        self.title("Arquiveiro ClickUp")

        self.root_frame = ttk.Frame(self, padding=20)
        self.root_frame.pack(fill=tk.BOTH, expand=True)

        self.parameters = {
            'user': {
                'label': 'Usuário:',
                'entry': None,
                'tk_var': tk.StringVar(),
                'row': 0
            },
            'password': {
                'label': 'Senha:',
                'entry': None,
                'tk_var': tk.StringVar(),
                'row': 1
            },
            'list_name': {
                'label': 'Lista Alvo:',
                'entry': None,
                'tk_var': tk.StringVar(),
                'row': 2
            },
            'driver_path': {
                'label': 'Driver Path: ',
                'entry': None,
                'tk_var': tk.StringVar(),
                'row': 3
            }}

        self.create_parameters_frame()
        self.create_parameters_widgets()
        self.create_ctrl_btn()
        self.create_log_box()
        self.update_log()

    def show_info(self, info_message):
        messagebox.showinfo(info_message[0], info_message[1])

    def create_parameters_frame(self):
        self.parameters_frame = ttk.LabelFrame(
            self.root_frame,
            text='Parâmetros',
            padding=10
        )
        self.parameters_frame.pack(fill=tk.X, expand=True)
        self.parameters_frame.grid_columnconfigure(0, weight=0)
        self.parameters_frame.grid_columnconfigure(1, weight=1)

    def create_parameters_widgets(self):
        parameter_types = ['user', 'password', 'list_name', 'driver_path']
        for type in parameter_types:
            ttk.Label(
                self.parameters_frame,
                text=self.parameters[type]['label'],
                anchor='w'
            ).grid(
                row=self.parameters[type]['row'],
                column=0,
                sticky='w',
                padx=5,
                pady=2
            )
            self.parameters[type]['entry'] = ttk.Entry(
                self.parameters_frame,
                textvariable=self.parameters[type]['tk_var'],
                justify='left',
            )
            self.parameters[type]['entry'].grid(
                row=self.parameters[type]['row'],
                column=1,
                sticky='ew',
                padx=5,
                pady=2
            )
        self.parameters['password']['entry'].config(show='*')

    def get_parameter(self, parameter_type):
        parameter_str = self.parameters[parameter_type]['tk_var'].get()
        return parameter_str

    def create_ctrl_btn(self):
        ctrl_btn_frame = ttk.Frame(
            self.root_frame,
            padding=10
        )
        ctrl_btn_frame.pack(fill=tk.X, expand=True)

        self.start_extraction_btn = ttk.Button(
            ctrl_btn_frame,
            text='Iniciar Extração',
        )
        self.stop_extraction_btn = ttk.Button(
            ctrl_btn_frame,
            text='Parar Extração',
            state='disabled'
        )
        self.export_database_btn = ttk.Button(
            ctrl_btn_frame,
            text='Exportar Dados',
            state='enabled'
        )
        self.start_extraction_btn.pack(side=tk.LEFT, padx=5, pady=2)
        self.stop_extraction_btn.pack(side=tk.LEFT, padx=5, pady=2)
        self.export_database_btn.pack(side=tk.LEFT, padx=5, pady=2)

    def create_log_box(self):
        log_frame = ttk.LabelFrame(
            self.root_frame,
            text='Log',
            padding=10
        )
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_box = scrolledtext.ScrolledText(
            log_frame, wrap=tk.WORD, state='disabled'
        )
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

    def update_log(self):
        while not fila_log.empty():
            try:
                message = fila_log.get_nowait()
                self.log_box.config(state='normal')
                self.log_box.insert(tk.END, message+'\n')
                self.log_box.see(tk.END)
                self.log_box.config(state='disabled')
            except queue.Empty:
                pass
        self.after(100, self.update_log)
