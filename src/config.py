environment = {
    "url": "https://<instance>.xmatters.com",  # ensure that there's no / at the end
    "username": "username",
    "password": "password"
}

# Log Levels Integers
# Critical: 50
# Error:	40
# Warning:	30
# Info:     20
# Debug:	10
# Not Set:	0

responses = {
    "form": "Form Name",
    "thread_count": 10,
    "page_size": 100,
    "file_name": "user_response.csv",  # absolute path recommended for Windows, Linux can remain as is
    "encoding": "utf-8",
    "logging": {
        "file_name": "log_responses.log",  # absolute path recommended for Windows, Linux can remain as is
        "max_bytes": 16 * 1024 * 1024,  # 16mb is default
        "back_up_count": 2,
        "level": 20
    }
}

people = {
    "thread_count": 3,
    "page_size": 1000,
    "properties": {
        # below are key/value property pairs that will be used for the search that exist on user record
        # values must be stored in lists to support multiple values if single needed, only add one value in lists
        "Emp Status": ["On Holiday", "On Medical Leave"]
    },
    "logging": {
        "file_name": "log_people.log",  # absolute path recommended for Windows, Linux can remain as is
        "max_bytes": 16 * 1024 * 1024,  # 16mb is default
        "back_up_count": 2,
        "level": 20
    }
}

modify_language = {
    "thread_count": 3,
    "page_size": 1000,
    "properties": {
        # values must be stored in lists to support multiple values if single needed, only add one value in lists
        "site": ["Site 1", "Site 2"]
    },
    "logging": {
        "file_name": "log_modify_language.log",  # absolute path recommended for Windows, Linux can remain as is
        "max_bytes": 16 * 1024 * 1024,  # 16mb is default
        "back_up_count": 2,
        "level": 20
    }
}

add_members = {
    "file": {
        "file_name": "data/add_members.csv",  # absolute path recommended for Windows, Linux can remain as is
        "encoding": "utf-8"
    },
    "thread_count": 5,
    "logging": {
        "file_name": "log_add_members.log",  # absolute path recommended for Windows, Linux can remain as is
        "max_bytes": 16 * 1024 * 1024,  # 16mb is default
        "back_up_count": 2,
        "level": 10
    }
}

dynamic_teams = {
    "file": {
        "file_name": "data/dynamic_teams.csv",  # absolute path recommended for Windows, Linux can remain as is
        "encoding": "utf-8"
    },
    "logging": {
        "file_name": "log_dynamic_teams.log",  # absolute path recommended for Windows, Linux can remain as is
        "max_bytes": 16 * 1024 * 1024,  # 16mb is default
        "back_up_count": 2,
        "level": 10
    }
}

roles = {
    "thread_count": 5,
    "role_mapping": {
        "default_role": "Standard User",  # default role to be assigned if all roles are removed from the user's profile
        "enable_web_ui": True,
        "plan_name": "Script Runner",  # only leveraged if enable_web_ui is true
        "library_name": "RoleMapping",  # only leveraged if enable_web_ui is true
        "local_file_name": "",  # only leveraged if enable_web_ui is false
    },
    "logging": {
        "file_name": "log_roles.log",  # absolute path recommended for Windows, Linux can remain as is
        "max_bytes": 16 * 1024 * 1024,  # 16mb is default
        "back_up_count": 2,
        "level": 10
    }
}
