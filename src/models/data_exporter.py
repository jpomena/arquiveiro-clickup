import pandas


class DataExporter:
    def __init__(self):
        pass

    def export_to_excel(self, db_tasks_data):
        tasks_dataframe = pandas.DataFrame(
            columns=[
                'Atividade',
                'Etiqueta',
                'Responsável',
                'Data de criação',
                'Data de início',
                'Data de conclusão',
                'Data de entrega'
            ])
        date_keys = [
            'task_backlog_date',
            'task_start_date',
            'task_done_date',
            'task_delivery_date'
        ]
        task_data_types = [
            'task_name',
            'task_tag',
            'task_assignee',
            'task_backlog_date',
            'task_start_date',
            'task_done_date',
            'task_delivery_date'
        ]

        for task in db_tasks_data:
            task_data = []
            for key in date_keys:
                if task[key]:
                    try:
                        task[key] = self._format_date(task[key])
                    except ValueError:
                        pass

            for type in task_data_types:
                task_data.append(task[type])

            pandas_task_data = pandas.Series(
                task_data, index=tasks_dataframe.columns
            )
            tasks_dataframe.loc[len(tasks_dataframe)] = pandas_task_data

        tasks_dataframe.to_excel('atividades.xlsx', index=False)

    def _format_date(self, value):
        return pandas.to_datetime(value, format='%d/%m/%Y')
