from ..utils.aux_functions import log
import threading
from queue import Queue


class Sasori:
    def __init__(
        self,
        puppet_browser,
        html_parser,
        regex_engine,
        database,
        data_exporter,
        gui
    ):
        self.pb = puppet_browser
        self.html_parser = html_parser
        self.re = regex_engine
        self.db = database
        self.de = data_exporter
        self.gui = gui

        self.db_queue = Queue()

        self.db_listener_thread = threading.Thread(
            target=self._process_db_queue
        )
        self.db_listener_thread.daemon = True
        self.db_listener_thread.start()

        self.gui.start_extraction_btn.config(command=self.start_extraction)
        self.gui.stop_extraction_btn.config(command=self.stop_extraction)
        self.gui.export_database_btn.config(command=self.export_to_excel)

        self.extracting_data = False

    def login_to_clickup(self):
        user = self.gui.get_parameter('user')
        password = self.gui.get_parameter('password')
        list_name = self.gui.get_parameter('list_name')

        if not user or not password or not list_name:
            log('Insira todos os dados obrigatórios!')
            self.extracting_data = False
            self.gui.stop_extraction_btn.config(state='disabled')
            self.gui.start_extraction_btn.config(state='normal')
            return

        if not self.extracting_data:
            return
        self.extracting_data = True
        driver_path = self.gui.get_parameter('driver_path')

        self.pb.open_browser(driver_path)
        self.driver = self.pb.get_driver()
        self.pb.access_site()
        self.pb.login(user, password)

    def locate_column(self):
        if not self.extracting_data:
            return
        list_name = self.gui.get_parameter('list_name')

        self.pb.open_list(list_name)
        self.pb.open_list_kanban()
        self.pb.config_columns()
        self.target_column = self.pb.select_column()

    def iterate_card(self):
        try:
            if not self.extracting_data:
                return
            self.pb.open_card(self.target_column)
            if not self.extracting_data:
                return
            task_html_elements = self.get_task_html_elements()
            if not self.extracting_data:
                return
            task_soups = self.get_task_soups(task_html_elements)
            task_data = self.get_task_data(task_soups)
            self.db_queue.put(task_data)
            log('Dados da atividade armazenados no banco de dados.')
            if not self.extracting_data:
                return
            self.pb.archive_card()
            log(f'{task_data}')
        except Exception as e:
            log(
                f'''Não há mais cards ou ocorreu
                um erro na extração: {e}'''
            )

    def get_task_html_elements(self):
        task_html_elements = {}
        task_html_elements[
            'task_name'
        ] = self.pb.get_task_name_html_element()
        task_html_elements[
            'task_tag'
        ] = self.pb.get_task_tag_html_element()
        task_html_elements[
            'task_assignee'
        ] = self.pb.get_task_assignee_html_element()
        task_html_elements[
            'task_history'
        ] = self.pb.get_task_history_html_element()
        return task_html_elements

    def get_task_soups(self, task_html_elements):
        task_soups = {}
        task_soups['task_name'] = self.html_parser.soupfy_html_element(
            task_html_elements['task_name']
        )
        task_soups['task_tag'] = self.html_parser.soupfy_html_element(
            task_html_elements['task_tag']
        )
        task_soups['task_assignee'] = self.html_parser.soupfy_html_element(
            task_html_elements['task_assignee']
        )
        task_soups['task_history'] = self.html_parser.soupfy_html_element(
            task_html_elements['task_history']
        )

        return task_soups

    def get_task_data(self, task_soups):
        task_data = {}
        task_data['task_name'] = self.re.get_task_name(
            task_soups['task_name']
        )
        task_data['task_tag'] = self.re.get_task_tag(
            task_soups['task_tag']
        )
        task_data['task_assignee'] = self.re.get_task_assignee(
            task_soups['task_assignee']
        )
        task_data['backlog_date'] = self.re.get_task_backlog(
            task_soups['task_history']
        )
        task_data['start_date'] = self.re.get_task_start(  # FIXME
            task_soups['task_history']
        )
        task_data['done_date'] = self.re.get_task_done(  # FIXME
            task_soups['task_history']
        )
        task_data['delivery_date'] = self.re.get_task_delivery(
            task_soups['task_history']
        )
        if task_data['done_date'] is None:
            task_data['done_date'] = task_data['delivery_date']
        return task_data

    def extraction_loop(self):
        self.extracting_data = True
        try:
            self.login_to_clickup()
            self.locate_column()
            while self.extracting_data:
                try:
                    self.iterate_card()
                except Exception as e:
                    log(f'Erro: {e}')
        finally:
            if self.driver:
                self.pb.close_browser()
            log('Processo encerrado.')
            self.extracting_data = False

    def start_extraction(self):
        self.gui.stop_extraction_btn.config(state='normal')
        self.gui.start_extraction_btn.config(state='disabled')
        self.automation_thread = threading.Thread(target=self.extraction_loop)
        self.automation_thread.daemon = True
        self.automation_thread.start()

    def stop_extraction(self):
        self.extracting_data = False
        log('Comando para interromper a extração recebido.')
        self.gui.stop_extraction_btn.config(state='disabled')
        self.gui.start_extraction_btn.config(state='normal')

    def _process_db_queue(self):
        while True:
            task_data = self.db_queue.get()
            self.db.save_task_data(task_data)
            self.db_queue.task_done()

    def export_to_excel(self):
        db_tasks_data = self.db.get_db_tasks_data()
        self.de.export_to_excel(db_tasks_data)
