from dateutil.parser import parse


def is_date(string):
    try:
        parse(string, fuzzy=False)
        return True
    except ValueError:
        return False