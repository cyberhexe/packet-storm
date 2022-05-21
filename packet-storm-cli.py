#!/usr/bin/env python3
import nest_asyncio

nest_asyncio.apply()
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
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.shortcuts import radiolist_dialog

from prompt_toolkit.shortcuts import message_dialog

console = Console()

history_file = "~/.packet-storm-history"

docs_extension_list = ['mkd', 'md', 'txt']

current_note = None

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

box_style = Style.from_dict({
    'dialog': 'bg:#88ff88',
    'dialog frame.label': 'bg:#ffffff #000000',
    'dialog.body': 'bg:#000000 #00ff00',
    'dialog shadow': 'bg:#00aa00',
})


class TxtNode:
    def __init__(self, root_dir: str, abs_path: str):
        if not os.path.exists(abs_path):
            raise Exception(f"{abs_path} does not exist")
        self.root_dir = root_dir
        self.abs_path = abs_path
        self.title = os.path.basename(self.abs_path).rstrip(".md")
        with open(abs_path, 'r') as f:
            self.content = f.read()
        self.normalized_name = self.abs_path.split('.')[0].split(self.root_dir)[1].lstrip(os.sep)
        self.folder = self.normalized_name.split(self.title)[0].rstrip(os.sep)

    def print_md(self):
        print("\033c", end='')
        console.print(Markdown(self.content))


def get_bottom_toolbar():
    global toolbar_text
    return [
        ('class:toolbar', ' [F2] List notes'),
        ('class:toolbar', ' [F3] Create note'),
        ('class:toolbar', ' [F4] Edit note')
    ]


def create_radiolist_dialog(text: str, elements: list):
    return radiolist_dialog(
        # title=HTML('<style bg="blue" fg="white">Note</style> '
        #            '<style fg="ansired">creation</style> window'),
        text=text,
        values=elements,
        style=box_style)


def get_notes_folders(export_dir: str):
    folders = []
    notes = load_notes(export_dir=export_dir)
    for folder in list(set(entry.folder for entry in notes)):
        folders.append((folder, folder))
    folders.sort()
    return folders


def find_note(export_dir: str, note_normalized_name: str):
    for note in load_notes(export_dir=export_dir):
        if note_normalized_name == note.normalized_name or note.normalized_name in note_normalized_name:
            return note


class CommandPrompt:
    def __init__(self, prompt_str: str,
                 completer: Completer = None,
                 style: Style = None,
                 server_url: str = None,
                 auth_token: str = None,
                 export_dir: str = None):
        self.export_dir = export_dir
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

        @self.bindings.add("f2")
        def _(event):
            notes = load_notes(export_dir=export_dir)
            dialog_elements = []
            for note in notes:
                dialog_elements.append((note.abs_path, note.normalized_name))

            path = create_radiolist_dialog(text=f"Select a note to open\n",
                                           elements=dialog_elements).run()
            if not path:
                return
            note = find_note(export_dir=export_dir, note_normalized_name=path)
            global current_note
            current_note = note
            note.print_md()
            print_delimiter()

        @self.bindings.add("f3")
        def _(event):
            note_name = input_dialog(
                title='Create a new note',
                text="Please type the name of your new note:").run()
            if not note_name:
                return

            folders = get_notes_folders(export_dir=export_dir)

            path = create_radiolist_dialog(text=f"Please specify the folder for your new note '{note_name}' \n",
                                           elements=folders).run()
            if not path:
                return

            new_note_path = f"{export_dir}{os.sep}{path}{os.sep}{note_name}.md"
            os.system(f"vim \"{new_note_path}\"")
            if os.path.exists(new_note_path):
                message_dialog(
                    title='Note created successfully',
                    text=f'Your note has been saved at {new_note_path}',
                    style=box_style).run()
            else:
                message_dialog(
                    title='Note has not been created',
                    text=f'Your note has not been saved').run()

        @self.bindings.add("f4")
        def _(event):
            global current_note
            if not current_note:
                return
            file_hash = md5(current_note.abs_path)
            os.system(f"vim '{current_note.abs_path}'")
            new_file_hash = md5(current_note.abs_path)
            if file_hash == new_file_hash:
                # the file has not been changed
                return
            else:
                # push the changes to the trilium server
                with open(current_note.abs_path, 'r') as f:
                    updated_content = f.read()
                    current_note.content = updated_content
                if self.sync_thread:
                    response = self.sync_thread.ea.search_note(search=current_note.title)

                    if 'results' in response:
                        for note in response['results']:
                            remote_note_title = note['title']

                            if remote_note_title != current_note.title:
                                continue
                            else:
                                self.sync_thread.ea.update_note_content(noteId=note['noteId'], content=updated_content)
                current_note.print_md()
                print_delimiter()


    def input(self, prompt_str: str = None):
        if prompt_str:
            _prompt_str = prompt_str
        else:
            _prompt_str = self.prompt_str
        toolbar = get_bottom_toolbar()
        return self.session.prompt(_prompt_str, completer=self.completer,
                                   key_bindings=self.bindings,
                                   complete_while_typing=True,
                                   bottom_toolbar=toolbar,
                                   style=self.style)


class SearchCompleter(Completer):
    def __init__(self, nodes: list):
        Completer.__init__(self)
        self.nodes = nodes

    def get_completions(self, document, complete_event):
        for node in self.nodes:
            if document.text.lower() in node.content.lower() or \
                    document.text.lower() in node.title.lower():
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


def start_interactive_prompt(export_dir: str,
                             server_url: str = None,
                             token: str = None):
    nodes = load_notes(export_dir=export_dir)
    word_completer = SearchCompleter(nodes)
    command_prompt = CommandPrompt('>> ', completer=word_completer,
                                   style=style,
                                   server_url=server_url,
                                   auth_token=token,
                                   export_dir=export_dir)
    docs_name = command_prompt.input()
    for node in load_notes(export_dir=export_dir):
        if docs_name == node.normalized_name:
            global current_note
            current_note = node
            node.print_md()
            print_delimiter()


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
        while True:
            try:
                start_interactive_prompt(export_dir=export_dir,
                                         server_url=options.server_url,
                                         token=options.token)
            except KeyboardInterrupt:
                exit()
            except Exception:
                pass


if __name__ == '__main__':
    main()
