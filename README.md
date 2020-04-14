# xMatters ETL and Integration Tools with Python3

## Overview
From within `/integrator_py/src` exists the following scripts available for execution:
* `/integrator_py/src/add_members.py`: Creates groups and add members to created groups
* `/integrator_py/src/dynamic_teams.py`: Creates dynamic teams
* `/integrator_py/src/roles.py`: This script is responsible synchronizing roles based on group membership
* `/integrator_py/src/people.py`: This script is responsible for querying users based on a property name and value to then set the users as inactive
* `/integrator_py/src/response.py`: This script is responsible for querying xmatters events based on a form name and then outputting to a file the user delivery detail
* `/integrator_py/src/modify_lanugage.py`: This script is responsible for querying xmatters based on user's site affiliation and then setting the profile to a different language such as portuguese


## Installation & Required Dependencies
1. This package was developed for Python3 only, install the latest Python3 stable version here: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Python3 will install with a package manager called pip. A required dependency to leverage `integrator_py` is requests, which is documented here: [https://pypi.org/project/requests/](https://pypi.org/project/requests/)
3. To install requests, navigate to the command line and execute `pip3 install requests`
4. Next, it is required to download the pyxmatters package from [https://github.com/matthewhenry1/pyxmatters](https://github.com/matthewhenry1/pyxmatters)
5. Once pyxmatters has been downloaded, place the xmatters package in the following directory: `/integrator_py/src/`
5. Once requests and pyxmatters is installed, the `integrator_py` is ready for use!

## How To Use
1. It is suggested to use `integrator_py` with PyCharm CE. PyCharm CE can be downloaded from here: [https://www.jetbrains.com/pycharm/download](https://www.jetbrains.com/pycharm/download). Ensure the community edition is installed. If you're already satisfied with your existing editor, use that.
2. Before executing any of the scripts identified in the overview section, first open the `/integrator_py/src/config.py` and modify the `environment` object. If the process being leveraged, be sure to update the `file` object as well and map to the associated file as needed.
3. To execute the script, use the terminal at the very bottom of PyCharm CE or open the Terminal on your machine and navigate to `<your_path/integrator_py/src/`, from within this directory execute `python3` followed by one of the scripts desired to be executed. For example `python3 on_call.py`

## Pro Tips
* If you feel like your `integrator_py/src/` is becoming crowded, you can move your logs and config to a dedicated folder, i.e. `/integrator_py/src/log/log.log` & `/integrator_py/src/config/config.py`
* You can also move your core scripts to their own folder as well, i.e. `add_members.py`, `dynamic_teams.py`, and `on_call.py` could exist in a directory like: `/integrator_py/src/scripts/<they_exist_here_now>`. _**HOWEVER**_ this is the sibling directory concept in Python, so if you decide to do this or pursue this approach, it is required to execute scripts from `/integrator_py/src/` and must be executed from the root directory as: `python3 -m subpackage1.script1`. So using the example provided it would be `python3 -m scripts.on_call.py`
* The `integrator_py/src/xmatters/` package isn't actually needed, like `requests`, the `xmatters` package is available to install via `pip3 install pyxmatters`. It's available here: [https://pypi.org/project/pyxmatters/](https://pypi.org/project/pyxmatters/). _**HOWEVER**_ if this package is going to reside for Production usage, the `xmatters` directory must be provided locally as changes, updates, and or even improvements could break the design of whatever script/package is leveraging it.
* See [https://github.com/matthewhenry1/pyxmatters/blob/master/samples/test_script.py](https://github.com/matthewhenry1/pyxmatters/blob/master/samples/test_script.py) for additional examples interfacing with `pyxmatters`

## Specific notes for roles.py

### Overview
The role synchronization is designed to take a JSON format like below and based on group membership assign/remove roles. So using the example below, if a member is included in the _xMatters Developers_ group, the user would receive the _Developer_ and _Full Access User_ roles. To remove roles, the GET users by Roles query is leveraged, if the user contains one of the roles in the role mapping JSON object and does not exist in one of the groups, that user will lose that role.
```
  {
    "data": [{
      "group": "xMatters Developers",
      "roles": ["Developer", "Full Access User"]
    }, {
      "group": "xMatters Company Supervisor",
      "roles": ["Company Supervisor"]
    }, {
      "group": "xMatters Full Access User",
      "roles": ["Full Access User"]
    }]
  }
```

### Configuration
To configure the role sync, open the `config.py`. 

### Automation
To automate this process, it is recommended to leverage a Windows Task Scheduler. If this solution is not viable, an alternative option is to leverage the xMatters Agent and utilize `xm-shell`, which is documented here: https://help.xmatters.com/ondemand/xmodwelcome/xmattersagent/writing-xmatters-agent-scripts.htm

To successfully initiate the command via the xMatters Agent and `xm-shell`, be sure to execute the command like so:

**Windows:**
```
 py C:\xMatters\integrator_py\roles.py
```

**Linux:**
```
 python3 /Users/matthenry/integrator_py/roles.py
```

## Miscellaneous Notes
* For MacOS users: Recursively remove compiled files prior to uploading to GitHub
    * From within src directory (i.e. `/integrator_/src`) execute the following: `find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf`
