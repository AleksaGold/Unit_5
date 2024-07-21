from configparser import ConfigParser

HH_URL_VACANCIES = 'https://api.hh.ru/vacancies'
HH_URL_EMPLOYERS = 'https://hh.ru/employer'

EMPLOYERS = {'65': 'Московский аэропорт Домодедово',
             '43140': 'Международный Аэропорт Внуково',
             '229': 'АО Международный аэропорт Шереметьево',
             '1648021': 'Международный аэропорт Жуковский',
             '80': 'Альфа-Банк',
             '78638': 'Т-Банк',
             '1122462': 'Skyeng',
             '2863076': 'Skillbox',
             '920692': 'Фонд Сколково',
             '895945': 'Правительство Москвы'
             }
AREA = 1
VACANCY_ONLY_WITH_SALARY = True


def config(filename='database.ini', section='postgresql'):
    """
    Функция для создания словаря с данными для подключения к БД
    :param filename: имя файла, в котором хранятся данные для подключения
    :param section: данные для подключения
    :return: словарь с данными для подключения к БД
    """
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
