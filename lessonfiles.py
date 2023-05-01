import requests

class File(object):
    def __init__(self, *args):
        #ссылка на репозиторий с заданиями, параметр1 = занятие, параметр2 = задача
        repository = lambda lesson, task: f''
        #имя тестового файла по умолчанию
        default_test_file_name = 'test'
        
        lesson = None
        task = None
        self.file = None
        self.fetched = None
        open_test_error = lambda path: print(f'Файл "{path}"\nне удалось открыть')
        load_error = lambda path: print(f'Файл "{path}"\n  не удалось ни открыть ни загрузить')
        load_success = lambda: print(f'Файл загружен')
        load_begin = lambda url: print(f'Загрузка файла "{url}"')
        
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
            try:
                file = open(path)
            except IOError:
                url = path
                fetch_data(url)
            else:
                self.file = file
                self.fetched = False
        else:
            task = args[1]
            lesson = args[0]
            if task == "":
                if len(args) > 2:
                    try_open_file(args[2])
                else:
                    try_open_file(default_test_file_name)
            else:        
                fetch_data(repository(lesson, task))

    def read(self):
        if self.fetched == None:
            return None
        return self.file.text if self.fetched else self.file.read()

open_file = lambda *args: File(*args)
