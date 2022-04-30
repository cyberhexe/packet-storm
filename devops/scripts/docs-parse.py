#!/usr/bin/env python3
import os
from rich.console import Console
from rich.markdown import Markdown
from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.history import FileHistory

console = Console()

history_file = "~/.packet-storm-history"

def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Packet Storm Docs Parser Script")
    parser.add_argument('-ed',
                        '--export-dir',
                        dest='export_dir',
                        required=True,
                        type=str,
                        help="Specify the export directory path from the cherrytree converter script")
    options = parser.parse_args()
    return options

def print_delimeter():
    print()
    print("[ ::::::::::::::::::::::::::::::::::::::::::::::::::::::::: ]")
    print()

def bottom_toolbar(toolbar_text: str):
    return [('class:bottom-toolbar', toolbar_text)]


style = Style.from_dict({
    'bottom-toolbar': '#ffffff bg:#333333',
})


class CommandPrompt:
    def __init__(self, prompt_str: str, completer: Completer = None,
                 bottom_toolbar_tokens: list = None,
                 style: Style = None):
        self.prompt_str = prompt_str
        self.completer = completer
        self.bottom_toolbar_tokens = bottom_toolbar_tokens
        self.style = style
        if os.path.exists(history_file):
            self.session = PromptSession(history=FileHistory(history_file))
        else:
            self.session = PromptSession()

    def input(self):
        return self.session.prompt(self.prompt_str, completer=self.completer,
                      complete_while_typing=True,
                      bottom_toolbar=self.bottom_toolbar_tokens,
                      style=self.style)


class SearchCompleter(Completer):
    def __init__(self, nodes: list):
        Completer.__init__(self)
        self.nodes = nodes

    def get_completions(self, document, complete_event):
        for node in self.nodes:
            if document.text.lower() in node.normalized_name.lower():
                yield Completion(node.normalized_name, start_position=-1000)


class TxtNode:
    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise Exception(f"{file_path} does not exist")
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
        with open(file_path, 'r') as f:
            self.content = f.read()
        self.normalized_name = self.file_name.replace('--', '/').replace('_', ' ').replace('.txt', '')

    def print_md(self):
        print("\033c", end='')
        console.print(Markdown(self.content))


def main():
    options = get_arguments()
    export_dir = options.export_dir

    if export_dir.endswith('/'):
        export_dir = export_dir[0:-1]

    nodes = []
    for entry in os.scandir(export_dir):
        if entry.is_file() and 'txt' in entry.name:
            node = TxtNode(file_path=f"{export_dir}/{entry.name}")
            nodes.append(node)

    if nodes:
        print('What are we looking for?')
        word_completer = SearchCompleter(nodes)
        command_prompt = CommandPrompt('>> ', completer=word_completer,
                                       bottom_toolbar_tokens=bottom_toolbar(f"{len(nodes)} pages imported"),
                                       style=style)
        while True:
            docs_name = command_prompt.input()
            for node in nodes:
                if docs_name == node.normalized_name:
                    node.print_md()
                    print_delimeter()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
