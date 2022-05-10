#!/usr/bin/env python3
import hashlib
import os
from threading import Thread

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.markdown import Markdown
from trilium_py.client import ETAPI

console = Console()

history_file = "~/.packet-storm-history"

docs_extension_list = ['mkd', 'md', 'txt']


def get_arguments():
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Packet Storm CLI")
    parser.add_argument('-ed',
                        '--export-dir',
                        dest='export_dir',
                        required=False,
                        type=str,
                        help="Specify the directory path with .md or .txt files to parse. "
                             "The script will recursively walk through the directories and parse the markdown "
                             "or text files into the compatible structure the script understands.")
    parser.add_argument('--server-url',
                        dest='server_url',
                        required=False,
                        type=str,
                        help="Specify the base URL of the Trilium server to sync with")
    parser.add_argument('--token',
                        dest='token',
                        required=False,
                        type=str,
                        help="Specify the ETAPI token of your Trilium user")
    options = parser.parse_args()
    if options.server_url and not options.token:
        parser.error("--token must be provided if --server-url has been given")
    if not options.server_url and options.token:
        parser.error("--server-url must be provided if --token has been given")
    return options


def md5(fname: str):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def print_delimiter():
    print()
    print("[ ::::::::::::::::::::::::::::::::::::::::::::::::::::::::: ]")
    print()


def bottom_toolbar(toolbar_text: str):
    return [('class:bottom-toolbar', toolbar_text)]


style = Style.from_dict({
    'bottom-toolbar': '#ffffff bg:#333333',
})


class TxtNode:
    def __init__(self, root_dir: str, abs_path: str):
        if not os.path.exists(abs_path):
            raise Exception(f"{abs_path} does not exist")
        self.root_dir = root_dir
        self.abs_path = abs_path
        self.title = os.path.basename(self.abs_path).rstrip(".mkd")
        with open(abs_path, 'r') as f:
            self.content = f.read()
        self.normalized_name = self.abs_path.split('.')[0].split(self.root_dir)[1].lstrip(os.sep)

    def print_md(self):
        print("\033c", end='')
        console.print(Markdown(self.content))


class CommandPrompt:
    def __init__(self, prompt_str: str,
                 completer: Completer = None,
                 style: Style = None,
                 server_url: str = None,
                 auth_token: str = None,
                 export_dir: str = None):
        self.prompt_str = prompt_str
        self.completer = completer
        self.style = style
        if os.path.exists(history_file):
            self.session = PromptSession(history=FileHistory(history_file))
        else:
            self.session = PromptSession()

        self.sync_thread = None
        if server_url and auth_token:
            self.sync_thread = TriliumNotesSyncThread(server_url=server_url,
                                                      auth_token=auth_token,
                                                      export_dir=export_dir)
            self.sync_thread.start()

        # Create a set of key bindings
        self.bindings = KeyBindings()

        @self.bindings.add("f4")
        def _(event):
            if not self.current_node:
                print_delimiter()
                print("There's nothing to edit yet")
                return
            file_hash = md5(self.current_node.abs_path)
            os.system(f"vim '{self.current_node.abs_path}'")
            new_file_hash = md5(self.current_node.abs_path)
            if file_hash == new_file_hash:
                # the file has not been changed
                return
            else:
                # push the changes to the trilium server
                with open(self.current_node.abs_path, 'r') as f:
                    updated_content = f.read()
                    self.current_node.content = updated_content
                if self.sync_thread:
                    response = self.sync_thread.ea.search_note(search=self.current_node.title)

                    if 'results' in response:
                        for note in response['results']:
                            remote_note_title = note['title']

                            if remote_note_title != self.current_node.title:
                                continue
                            else:
                                self.sync_thread.ea.update_note_content(noteId=note['noteId'], content=updated_content)
                self.current_node.print_md()
                print_delimiter()

        def bottom_toolbar():
            return [
                ('class:toolbar', ' [F4] Edit ')
            ]

        self.bottom_toolbar = bottom_toolbar()
        self.current_node = None

    def input(self, prompt_str: str = None):
        if prompt_str:
            _prompt_str = prompt_str
        else:
            _prompt_str = self.prompt_str
        return self.session.prompt(_prompt_str, completer=self.completer,
                                   key_bindings=self.bindings,
                                   complete_while_typing=True,
                                   bottom_toolbar=self.bottom_toolbar,
                                   style=self.style)

    def set_current_node(self, node: TxtNode):
        self.current_node = node


class SearchCompleter(Completer):
    def __init__(self, nodes: list):
        Completer.__init__(self)
        self.nodes = nodes

    def get_completions(self, document, complete_event):
        for node in self.nodes:
            if document.text.lower() in node.normalized_name.lower():
                yield Completion(node.normalized_name, start_position=-1000)


class TriliumNotesSyncThread:
    def __init__(self, server_url: str, auth_token: str, export_dir: str):
        self.thread = Thread(target=self.run)
        self.ea = ETAPI(server_url, auth_token)
        self.local_export_dir = export_dir

    def run(self):
        while True:
            for node in load_notes(self.local_export_dir):
                response = self.ea.search_note(search=node.title)

                if 'results' in response:
                    for note in response['results']:
                        remote_content = self.ea.get_note_content(noteId=note['noteId']).strip()

                        remote_note_title = note['title']

                        if remote_note_title != node.title:
                            continue
                        if remote_content == node.content.strip():
                            continue
                        else:
                            with open(node.abs_path, 'w') as f:
                                f.write(remote_content)
                            node.content = remote_content

    def start(self):
        self.thread.start()


def traverse_dir(export_dir: str):
    files_list = []
    for root, dirs, files in os.walk(export_dir):
        path = root.split(os.sep)
        for file in files:
            abs_path = f"{os.sep.join(path)}{os.sep}{file}"

            if any(abs_path.endswith(ext) for ext in docs_extension_list):
                files_list.append(abs_path)
    return files_list


def load_notes(export_dir: str):
    # traverse root directory, and list directories as dirs and files as files
    nodes = []
    for abs_path in traverse_dir(export_dir):
        node = TxtNode(root_dir=export_dir, abs_path=abs_path)
        nodes.append(node)
    return nodes


def main():
    options = get_arguments()

    nodes = []

    export_dir = options.export_dir
    if export_dir:
        if export_dir.endswith('/'):
            export_dir = export_dir[0:-1]

        nodes = load_notes(export_dir=export_dir)

    if nodes:
        print_delimiter()
        print("What are you looking for?")
        word_completer = SearchCompleter(nodes)
        command_prompt = CommandPrompt('>> ', completer=word_completer,
                                       style=style,
                                       server_url=options.server_url,
                                       auth_token=options.token,
                                       export_dir=export_dir)
        while True:
            docs_name = command_prompt.input()
            for node in load_notes(export_dir=export_dir):
                if docs_name == node.normalized_name:
                    command_prompt.set_current_node(node)
                    node.print_md()
                    print_delimiter()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
