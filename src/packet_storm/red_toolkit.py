#!/usr/bin/env python3
import asyncio
import logging
import os
import platform
from enum import Enum
from pathlib import Path
from time import time

from git.repo.base import Repo
from rich.console import Console
from rich.markdown import Markdown
logging.basicConfig(format='[%(asctime)s %(levelname)s]: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    level='INFO')

console = Console()

class SynchronizationMode(Enum):
    DOWNLOAD = "DOWNLOAD",
    UPDATE = "UPDATE"


git_sources = [
    'github.com',
    'bitbucket.com'
]


class BatchAsyncDownloader:
    def __init__(self):
        pass

    """
       Updates a list of tools
    """

    def update_tools(self, tools: list):
        self.generate_and_run_commands(
            [t for t in tools if t.is_downloaded() and t.is_git_repository()],
            SynchronizationMode.UPDATE)

    """
       Clones a list of tools
    """

    def download_tools(self, tools: list):
        self.generate_and_run_commands(
            [t for t in tools if not t.is_downloaded() and any(host in t.url for host in git_sources)],
            SynchronizationMode.DOWNLOAD)

    """
       Spawn a process to download/update a tool
    """

    @staticmethod
    async def sync_tool(mode: SynchronizationMode, tool):
        """
           Run tool synchronization in subprocess
        """

        if mode == SynchronizationMode.DOWNLOAD:
            tool.path.mkdir(parents=True, exist_ok=True)
            command = ['git', 'clone', tool.url, str(tool.path)]
        elif mode == SynchronizationMode.UPDATE:
            command = ['git', '-C', f"{tool.path}", 'pull']
        else:
            raise Exception(f"Unsupported synchronization mode: {mode}")

        logging.debug(f'Executing {mode} command: {command}')
        process = await asyncio.create_subprocess_exec(
            *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        tool_name = tool.name

        if mode == SynchronizationMode.DOWNLOAD:
            logging.info(f'Downloading {tool_name}')
        if mode == SynchronizationMode.UPDATE:
            logging.info(f'Updating {tool_name}')

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            if mode == SynchronizationMode.DOWNLOAD:
                logging.info('{} has been downloaded'.format(tool_name))
            if mode == SynchronizationMode.UPDATE:
                logging.info('{} has been updated'.format(tool_name))

        else:
            if mode == SynchronizationMode.DOWNLOAD:
                logging.error("{} failed to download".format(tool_name))
                logging.debug('{}: {} / {}'.format(tool_name, stdout, stderr))
            if mode == SynchronizationMode.UPDATE:
                logging.error("{} failed to update".format(tool_name))
                logging.debug('{}: {} / {}'.format(tool_name, stdout, stderr))
        result = stdout.decode().strip()

        return result

    def generate_and_run_commands(self, tools: list, mode: SynchronizationMode):
        start_time = time()
        logging.debug(f'{len(tools)} tool(s) received for {mode}')
        tasks = []
        for tool in tools:
            result = self.sync_tool(mode, tool)
            tasks.append(result)

        def run_asyncio_commands(async_tasks, max_concurrent_tasks=0):
            def make_chunks(length, number):
                """Yield successive n-sized chunks from l.

                Note:
                    Taken from https://stackoverflow.com/a/312464
                """
                for index in range(0, len(length), number):
                    yield length[index: index + number]

            """Run tasks asynchronously using asyncio and return results.

            If max_concurrent_tasks are set to 0, no limit is applied.

            Note:
                By default, Windows uses SelectorEventLoop, which does not support
                subprocesses. Therefore ProactorEventLoop is used on Windows.
                https://docs.python.org/3/library/asyncio-eventloops.html#windows
            """
            all_results = []

            if max_concurrent_tasks == 0:
                chunks = [async_tasks]
                num_chunks = len(chunks)
            else:
                chunks = make_chunks(length=async_tasks, number=max_concurrent_tasks)
                num_chunks = len(list(make_chunks(length=async_tasks, number=max_concurrent_tasks)))

            if asyncio.get_event_loop().is_closed():
                asyncio.set_event_loop(asyncio.new_event_loop())
            if platform.system() == "Windows":
                asyncio.set_event_loop(asyncio.ProactorEventLoop())
            loop = asyncio.get_event_loop()

            for i, tasks_in_chunk in enumerate(chunks):
                chunk = i + 1
                logging.debug(f"Beginning work on chunk {chunk}/{num_chunks}")
                commands = asyncio.gather(*tasks_in_chunk)
                # TODO queueing instead of chunking?
                tasks_results = loop.run_until_complete(commands)
                all_results += tasks_results
                logging.debug(f"Completed work on chunk {chunk}/{num_chunks}")

            loop.close()
            return all_results

        results = run_asyncio_commands(tasks, max_concurrent_tasks=20)  # At most 20 parallel tasks
        logging.debug(f"Results: {os.linesep.join(results)}")

        if len(results) > 0:
            end = time()
            rounded_end = "{0:.4f}".format(round(end - start_time, 4))
            logging.info(
                f"Async tools {'downloader' if mode == SynchronizationMode.DOWNLOAD else 'updater'} ran in "
                f"about {rounded_end} seconds")


class Tool:
    @staticmethod
    def find_category(url, readme_file):
        with open(readme_file, 'r', encoding='utf-8') as file:
            sections = file.read().split('## ')
            for sec in sections:
                if url in sec:
                    category = sec.split(os.linesep)[0]
                    return {
                        'name': category,
                        'alias': category.lower().replace(' ', '-')
                    }

    def get_readme(self):
        readme_files_candidates = ['README.md', 'README', 'README.MD', 'readme', 'readme.md']
        for readme in readme_files_candidates:
            readme_path = f"{self.path}/{readme}"
            if os.path.exists(readme_path):
                return open(readme_path, 'r', encoding='utf-8').read()

    def __init__(self, line, file_content_as_string):
        assert line and line.strip() != ''
        self.name = line.split('**')[1].split('**')[0]
        self.description = line.split('**')[2].split('http')[0].strip()
        self.url = line.split(' ')[-1]
        self.category = self.find_category(self.url, file_content_as_string)
        self.path = Path(f"{os.getcwd()}/{self.category['alias']}/{self.name}")
        self.readme = self.get_readme() if self.is_downloaded() else None

    def download(self):
        download_tool(self)

    def is_downloaded(self):
        return os.path.exists(self.path) and os.listdir(self.path)

    def is_git_repository(self):
        try:
            return Repo(self.path)
        except Exception as e:
            logging.debug(e)
            return False

    def update(self):
        if not self.is_downloaded():
            logging.debug('{} is not downloaded'.format(self.name))
            return
        try:
            Repo(self.path).remote().pull()
            logging.info(f"{self.name} has been updated")
        except Exception as e:
            logging.error(f"Update failed: {e}")

    def print_md(self):
        print("\033c", end='')
        console.print(Markdown(self.get_readme()))


def download_tool(tool: Tool = None, tools: list = None):
    asyncgit = BatchAsyncDownloader()
    if tool and not tools:
        asyncgit.download_tools([tool])
    elif not tool and tools:
        asyncgit.download_tools(tools)
    elif not tool and not tools:
        raise Exception("At least one tool must be given for update")
    elif tool and tools:
        raise Exception("Either a tool name or a list of them must be given")


def update_tool(tool_name, tools):
    tools_to_update_list = []
    for tool in tools:
        if tool.name == tool_name or tool_name == 'UPDATE_ALL':
            tools_to_update_list.append(tool)
    asyncgit = BatchAsyncDownloader()
    asyncgit.update_tools(tools_to_update_list)


def get_tools_from_readme(readme_file: str):
    tools = []
    with open(readme_file, 'r', encoding='utf-8') as file:
        lines = [line.replace(os.linesep, '') for line in file.readlines()]
        for line in lines:
            if line.startswith('* **'):
                tool = Tool(line, readme_file)
                tools.append(tool)
    return tools


def get_scripts_from_readme(readme_file: str):
    scripts_url = []
    with open(readme_file, 'r', encoding='utf-8') as file:
        file_content_as_string = [line.replace(os.linesep, '') for line in file.readlines()]
        for line in file_content_as_string:
            if line.startswith('  * '):
                scripts_url.append(line.replace('  * ', ''))
    return scripts_url


def drop_deprecated_tools(deprecated_tools: list):
    import shutil

    for tool_name in deprecated_tools:
        for directory in [d[0] for d in os.walk(Path(os.getcwd()))]:
            if tool_name in directory:
                shutil.rmtree(Path(str(directory).split(tool_name)[0] + tool_name))
                logging.info('{} tool has been deleted'.format(tool_name))
                break


def search_in_tools(search_query: str, tools: list):
    logging.info(f'Searching for {search_query}')
    matched_tools = []
    for tool in tools:
        pattern = search_query.lower()
        if pattern in tool.name.lower() \
                or pattern in tool.description.lower() \
                or pattern in tool.category['name'].lower():
            matched_tools.append(tool)
    matched_tools_count = len(matched_tools)
    logging.info("%s tools available", matched_tools_count)
