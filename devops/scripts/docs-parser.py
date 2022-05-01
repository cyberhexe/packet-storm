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

# sudo apt install python3-magic
# shell token : rO24cXxgfQwJ_oSPOBGE/QTzTWYTIN+mzxay9pSu3jNOIj/WGoawK5mc=


docs_extension_list = ['mkd', 'md', 'txt']

def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Packet Storm Docs Parser Script")
    parser.add_argument('-ed',
                        '--export-dir',
                        dest='export_dir',
                        required=False,
                        type=str,
                        help="Specify the directory path with .md or .txt files to parse. "
                             "The script will recursively walk through the directories and parse the markdown "
                             "or text files into the compatible structure the script understands.")
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

def get_random_hacker_phrase():
    from random import choice

    return choice([
        "We're in.",
        "Hello.",
        "I don't play well with others.",
        "I couldn't think as slow as you if I tried.",
        "I invented it.",
        "Now the hunted becomes the hunter.",
        "Let the hacking begin.",
        "Come on, baby!",
        "It's beautiful.",
        "Now, we wait.",
        "Hack the Planet!",
        "Are you stoned or stupid?",
        "We have no names, man. No names!",
        "Too easy.",
        "By the time they realise the truth, we'll be long gone.",
        "I got an idea.",
        "A minor glitch with you seems to turn into a major catastrophe.",
        f"- It's too much machine for you.{os.linesep}- Yeah?",
        "Name your stakes.",
        "What the hell are you doing?",
        "You know anything about computers?",
        "That's why hackers always win.",
        "In English, please!",
    ])

class CommandPrompt:
    def __init__(self, prompt_str: str, completer: Completer = None,
                 style: Style = None):
        self.prompt_str = prompt_str
        self.completer = completer
        self.style = style
        if os.path.exists(history_file):
            self.session = PromptSession(history=FileHistory(history_file))
        else:
            self.session = PromptSession()

    def input(self, bottom_toolbar_tokens: list = None, prompt_str: str = None):
        if prompt_str:
            _prompt_str = prompt_str
        else:
            _prompt_str = self.prompt_str
        return self.session.prompt(_prompt_str, completer=self.completer,
                      complete_while_typing=True,
                      bottom_toolbar=bottom_toolbar_tokens,
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
    def __init__(self, root_dir: str, abs_path: str):
        if not os.path.exists(abs_path):
            raise Exception(f"{abs_path} does not exist")
        self.root_dir = root_dir
        self.file_path = abs_path
        self.file_name = os.path.basename(self.file_path)
        with open(abs_path, 'r') as f:
            self.content = f.read()
        self.normalized_name = self.file_path.split('.')[0].split(self.root_dir)[1].lstrip(os.sep)

    def print_md(self):
        print("\033c", end='')
        console.print(Markdown(self.content))


def main():
    options = get_arguments()

    nodes = []

    export_dir = options.export_dir
    if export_dir:
        if export_dir.endswith('/'):
            export_dir = export_dir[0:-1]

        # traverse root directory, and list directories as dirs and files as files
        for root, dirs, files in os.walk(export_dir):
            path = root.split(os.sep)
            # print((len(path) - 1) * '---', os.path.basename(root))
            for file in files:
                abs_path = f"{os.sep.join(path)}{os.sep}{file}"

                if any(abs_path.endswith(ext) for ext in docs_extension_list):
                    node = TxtNode(root_dir=export_dir, abs_path=abs_path)
                    nodes.append(node)


    if nodes:
        print("What are you looking for?")
        word_completer = SearchCompleter(nodes)
        command_prompt = CommandPrompt('>> ', completer=word_completer,
                                       style=style)
        while True:
            docs_name = command_prompt.input(bottom_toolbar_tokens=get_random_hacker_phrase())
            for node in nodes:
                if docs_name == node.normalized_name:
                    node.print_md()
                    print_delimeter()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
