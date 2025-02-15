# Attendance Manager

[![attendance-manager.png](https://i.postimg.cc/Y2fnMLDw/attendance-manager.png)](https://postimg.cc/Hjn4tnCS)

Developed as protoype application for my bachelor thesis on the topic of testability of hexagonal architecture.
Deployed on a virtual machine of the universite and accessible from the university network
on https://attend-man.f4.htw-berlin.de/ <br>

### Main Features

An attendance management system to log student attendance at university lectures.

- Attendance logging for students
- Attendance overview of course for professors
- User account management for admins

### Architecture Overview

Built utilizing hexagonal architecture (also knowns as ports and adapters architecture)

[![simple-architecture-uml.png](https://i.postimg.cc/X7qwmrTL/simple-architecture-uml.png)](https://postimg.cc/crqg8L1t)

### Local Development

- install dependencies: `pip install`
- required environments variables: DB_URI (SQLite URL) and SECRET_KEY
- start application `flask --app src.adapters.primary.app --debug run`
- add new dependencies to requiremnts.txt: `pip3 freeze > requirements.txt`
- run all tests `python -m pytest -s --headed .\tests` or individual
  `python -m pytest -s --headed  .\tests\[e2e|integration|unit] -k "[test name]"`