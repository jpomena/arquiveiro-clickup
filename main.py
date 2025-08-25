from src import Database
from src import Sasori
from src import HTMLParser
from src import PuppetBrowser
from src import RegexEngine
from src import GUI
from src.models.data_exporter import DataExporter


def main():
    puppet_browser = PuppetBrowser()
    html_parser = HTMLParser()
    regex_engine = RegexEngine()
    database = Database()
    database.create_table()
    data_exporter = DataExporter()

    themename = 'cosmo'
    gui = GUI(themename)

    controller = Sasori(  # noqa: F841
        puppet_browser, html_parser, regex_engine, database, data_exporter, gui
    )

    gui.mainloop()


if __name__ == '__main__':
    main()
