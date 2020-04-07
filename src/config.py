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
    "property_name": "Emp Status",
    "property_value": ["P", "L"],
    "logging": {
        "file_name": "log_people.log",  # absolute path recommended for Windows, Linux can remain as is
        "max_bytes": 16 * 1024 * 1024,  # 16mb is default
        "back_up_count": 2,
        "level": 20
    }
}