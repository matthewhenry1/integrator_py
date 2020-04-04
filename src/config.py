environment = {
    "url": "https://<instance>.xmatters.com",  # ensure that there's no / at the end
    "username": "username",
    "password": "password"
}

file = {
    "file_name": "user_response.csv",  # absolute path recommended for Windows, Linux can remain as is
    "encoding": "utf-8"
}

response = {
    "form": "Resiliency Testing"
}

role_mapping = {
    "default_role": "Standard User",  # default role to be assigned if all roles are removed from the user's profile
    "enable_web_ui": True,
    "plan_name": "Script Runner",  # only leveraged if enable_web_ui is true
    "library_name": "RoleMapping",  # only leveraged if enable_web_ui is true
    "local_file_name": ""  # only leveraged if enable_web_ui is false
}

thread_count = 15 # maximum concurrent threads that will be used in parallel processing to update xMatters. Do not exceed 30 as that will simulate DoS.

logging = {
    "file_name": "log.log",  # absolute path recommended for Windows, Linux can remain as is
    "max_bytes": 16 * 1024 * 1024,  # 16mb is default
    "back_up_count": 2,
    "level": 20
    # Log Levels Integers
    # Critical: 50
    # Error:	40
    # Warning:	30
    # Info:     20
    # Debug:	10
    # Not Set:	0
}