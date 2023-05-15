import requests

class File(object):
    def __init__(self, args, nargs):
        #ссылка на репозиторий с заданиями, параметр1 = занятие, параметр2 = задача
        repository = lambda lesson, task: f'https://raw.githubusercontent.com/AngryBro/inf_ege_files/main/{lesson}/{task}.txt'
        #имя тестового файла по умолчанию
        default_test_file_name = 'test'
        self.test_data = None
        if default_test_file_name in nargs:
            self.test_data = nargs[default_test_file_name]
        lesson = None
        task = None
        self.file = None
        self.fetched = None
        open_test_error = lambda path: print(f'Файл "{path}"\nне удалось открыть')
        load_error = lambda path: print(f'Файл "{path}"\n  не удалось ни открыть ни загрузить')
        load_success = lambda: print(f'Файл загружен')
        load_begin = lambda url: print(f'Загрузка файла "{url}"')

        def try_open_or_fetch(path, url = None):
            if url == None:
                url = path
            try:
                file = open(path)
            except IOError:
                fetch_data(url)
            else:
                self.file = file
                self.fetched = False
        
        def fetch_data(url):
            load_begin(url)
            try:
                response = requests.get(url)
            except IOError:
                load_error(url)
            else:
                if response.status_code == 200:
                    self.fetched = True
                    load_success()
                    self.file = response
                else:
                    load_error(url)

        def try_open_file(path):
            try:
                f = open(path)
            except IOError:
                open_test_error(path)
            else:
                self.file = f
                self.fetched = False

        if len(args) == 1:
            path = args[0]
            if path == "":
                if self.test_data == None:
                    try_open_file(default_test_file_name)
                else:
                    self.file = self.test_data
            else:
                try_open_or_fetch(path)
                # try:
                #     file = open(path)
                # except IOError:
                #     url = path
                #     fetch_data(url)
                # else:
                #     self.file = file
                #     self.fetched = False
        else:
            task = args[1]
            lesson = args[0]
            if task == "":
                if self.test_data == None:
                    try_open_file(default_test_file_name)
                else:
                    self.file = self.test_data
            else:
                try_open_or_fetch(task, repository(lesson, task))
                # try:
                #     file = open(task)
                # except IOError:
                #     url = repository(lesson, task)
                #     fetch_data(url)
                # else:
                #     self.file = file
                #     self.fetched = False       

    def read(self):
        if self.fetched == None:
            if self.test_data == None:
                return None
            return self.file
        if self.fetched:
            return self.file.text
        return self.file.read()

open_file = lambda *args, **kwargs: File(args, kwargs)
