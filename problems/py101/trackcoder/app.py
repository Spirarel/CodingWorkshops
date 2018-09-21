from __future__ import unicode_literals
import sys

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from peewee import *
import datetime
import click

command_completer = WordCompleter(['add', 'show'], ignore_case=True)

db = SqliteDatabase('to_do_list.db')


class ToDo(Model):
    task = CharField(max_length=255)
    description = CharField(max_length=255)
    timestamp = DateTimeField(default=datetime.datetime.now)
    mins = IntegerField()
    done = BooleanField(default=True)

    class Meta:
        database = db


def initialize():
    """Connect to database, create tables if they don't exist"""
    db.connect()
    db.create_tables([ToDo], safe=True)

def parse(input):
    """
        a b 10 first blog post
        a c 10 finished cli
        a p 120
    """
    input = input.strip()
    cmd, task, mins, description = ['']*4
    try:
        cmd, task, mins, *description = input.split()
        mins += 0
        description = ' '.join(description)
        return cmd, task, mins, description
    except TypeError:
        pass
        # return input, task, mins, description
    except ValueError:
        return input, task, mins, description


def add(**kwargs):
    ToDo.create(task=kwargs['task'],
                mins=kwargs['mins'],
                description=kwargs['description'])


def show(**kwargs):
    for t in ToDo.select():
        b,c,d,m,r,p = 0,0,0,0,0,0
        if t.task == 'b':
            b += t.mins
        elif t.task == 'c':
            c += t.mins
        elif t.task == 'd':
            d += t.mins
        elif t.task == 'm':
            m += t.mins
        elif t.task == 'r':
            r += t.mins
        elif t.task == 'p':
            p += t.mins

    # print(t.task, t.description, t.mins, t.done)
    print(f"{b} minutes spent blogging")
    print(f"{c} minutes spent in cli")
    print(f"{d} minutes spent in debugging")
    print(f"{m} minutes spent keeping the project in mind")
    print(f"{r} minutes spent reading")
    print(f"{p} minutes spent learning")


def execute(**kwargs):
    cmds = {
        'add': add,
        'show': show
    }

    cmds.get(kwargs['cmd'])(**kwargs)


@click.command()
@click.option('--interactive', '-i', help='needs some help text', is_flag=True, default=False)
@click.option('--show', '-s', help='needs some help text', is_flag=True, default=False)
@click.option('--add', '-a', nargs=3, type=(click.STRING, int, click.STRING), default=(None, None, None))
def main(interactive, add, show):
    initialize()

    if interactive:
        history = InMemoryHistory()
        session = PromptSession()

        while True:
            try:
                text = session.prompt('% ')
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            else:
                try:
                    cmd, task, mins, description = parse(text)
                    execute(cmd=cmd, task=task, mins=mins, description=description)
                except TypeError:
                    print("Please check your input")
    elif show:
        execute(cmd='show')
    else:
        task, mins, description = add
        execute(cmd='add', task=task, mins=mins, description=description)
    print('GoodBye!')


if __name__ == '__main__':
    main()
