import argparse
import sys

from decouple import config as conf
from google.cloud.firestore import Client, CollectionReference

db = Client.from_service_account_json(conf('GOOGLE_APPLICATION_CREDENTIALS'))
col = db.collection('notes')  # type: CollectionReference


class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    @staticmethod
    def from_dict(src):
        return Note(src['title'], src['content'])

    def to_dict(self):
        return {'title': self.title, 'content': self.content}

    def __str__(self):
        return 'title={},content={}'.format(self.title, self.content)


def read(title):
    for s in col.where(u'title', u'==', title).stream():
        return s.to_dict()


def read_all():
    return [s.to_dict() for s in col.stream()]


def write(note: Note):
    col.add(note.to_dict())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', metavar='TITLE', dest='write')
    parser.add_argument('-r', metavar='TITLE', dest='read')
    parser.add_argument('-l', dest='list', action='store_true')

    opt = parser.parse_args()
    if opt.list:
        for doc in read_all():
            nt = Note.from_dict(doc)
            print(nt.title)
        sys.exit()

    if opt.read:
        doc = read(opt.read)
        nt = Note.from_dict(doc)
        print(nt)
        sys.exit()

    if opt.write:
        ipt = input('Content:')
        nt = Note(opt.write, ipt)
        write(nt)
        sys.exit()
