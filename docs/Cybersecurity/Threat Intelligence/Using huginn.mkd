Huginn is a system for building agents that perform automated tasks for you online. 

They can read the web, watch for events, and take actions on your behalf. 
Huginn's Agents create and consume events, propagating them along a directed graph. Think of it as a hackable version of IFTTT or Zapier on your own server.

- https://github.com/huginn/huginn

## Usage

Simple stand-alone usage (use only for testing/evaluation as it can not be updated without losing data):

```bash
docker run -it -p 3000:3000 huginn/huginn
```

Use a volume to export the data of the internal mysql server:

```bash
docker run -it -p 3000:3000 -v /home/huginn/mysql-data:/var/lib/mysql huginn/huginn
```

