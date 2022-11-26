import pickle


def save_to_file(data):
    with open('/Users/alexgirardello/PycharmProjects/ihc/data/data.pkl', 'wb') as output:
        pickle.dump(data, output, pickle.HIGHEST_PROTOCOL)
    return True


def open_file():
    try:
        with open('/Users/alexgirardello/PycharmProjects/ihc/data/data.pkl', 'rb') as input:
            return pickle.load(input)
    except:
        return False
