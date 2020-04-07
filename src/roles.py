# local imports
import xmatters
import config

# python3 package imports
import logging
import base64
import json
from logging.handlers import RotatingFileHandler


# main process
def main() -> object:

    """
        1. Query for all users that currently have an elevated role.
        2. Query for all membership for all groups.
        3. Normalize the user data and prepare for an upload.
        4. Determine if there are any new users that should receive an elevated role.
        5. Loop through people and do the adding/removal procedures based on membership. Add to the request queue if an update is required.
        6. Process the requests.
    """

    # 1. query for all users by roles, using a set data type to capture roles to ensure no duplicates in query
    roles = set()
    for item in group_roles:
        for role in item["roles"]:
            roles.add(role)
    role_filter = ",".join(roles)
    people = xm_person.get_people_collection("&embed=roles&roles=" + role_filter) # execute search on users, people returns a list of the full xMatters person object record
    log.debug("people: " + str(people))

    # 2. query for all membership and build a list that contains dictionary with group name, set of unique users, and list of roles
    # Example: [{"users": {"user_1","user_2","user_3",},"roles": ["Role_1", "Role_2"]}, {"users": {"user_4","user_5","user_6",},"roles": ["Role_2", "Role_3"]}]
    unstructured_role_users_mapping = []
    for item in group_roles:
        users = xm_roster.get_roster_collection(item["group"])
        if users:
            unstructured_role_users_mapping.append({
                "users": users,
                "roles": item["roles"]
            })
    log.debug("unstructured_role_users_mapping: " + str(unstructured_role_users_mapping))

    # 3. Now it"s time to normalize the above data to make it useful later in the process,
    # Manipulating Example above: [{"role": "Role_1", "users": {"user_2", "user_3", "user_1"}}, {"role": "Role_2", "users": {"user_2", "user_3", "user_1", "user_6", "user_4", "user_5"}}, {"role": "Role_3", "users": {"user_6", "user_4", "user_5"}}]
    role_users_mapping = []
    for unstructured in unstructured_role_users_mapping:
        for role in unstructured["roles"]:
            if len(role_users_mapping) == 0:
                role_users_mapping.append({
                    "users": unstructured["users"],
                    "role": role
                })
            else:
                match = False
                for structured in role_users_mapping:
                    if structured["role"] == role:
                        match = True
                        structured["users"] = unstructured["users"].union(structured["users"])
                if not match:
                    role_users_mapping.append({
                        "users": unstructured["users"],
                        "role": role
                    })

    log.debug("role_users_mapping: " + str(role_users_mapping))

    # 4. We must find the users that need an elevated role but do not have an elevated role already
    role_users = set()
    for item in role_users_mapping:
        for user in item['users']:
            role_users.add(user)

    people_users = set()
    for person in people:
        people_users.add(person["targetName"])

    diff_users = role_users.difference(people_users)
    for user_name in diff_users:
        person = xm_person.get_person(user_name)
        if person:
            people.append(person)

    log.debug('Adding additional users to process that do not have an elevated role already: ' + str(people))

    # 5. Loop through people, normalize data, add/remove roles, and if update required queue update
    request_queue = []
    for person in people:
        update_required = False
        request = {"data": {
            "targetName": person["targetName"],
            "id": person["id"],
            "roles": []
            }
        }

        # build role object to assist with comparisons
        for role in person["roles"]["data"]:
            request["data"]["roles"].append(role["name"])

        # do add/remove
        for role_user in role_users_mapping:
            if request["data"]["targetName"] in role_user["users"] and role_user["role"] not in request["data"]["roles"]:
                update_required = True
                log.info("Adding " + role_user["role"] + " from user: " + request["data"]["targetName"])
                request["data"]["roles"].append(role_user["role"])

            elif request["data"]["targetName"] not in role_user["users"] and role_user["role"] in request["data"]["roles"]:
                update_required = True
                log.info("Removing " + role_user["role"] + " from user: " + request["data"]["targetName"])
                request["data"]["roles"].remove(role_user["role"])

        # set a default role if all roles are removed or just add the Standard User role by default if the user doesn't have it already
        if (len(request["data"]["roles"]) == 0 and update_required) or config.roles['role_mapping']["default_role"] not in request["data"]["roles"]:
            update_required = True
            log.info("Adding Default Role to Standard User for user: " + request["data"]["targetName"])
            request["data"]["roles"].append(config.roles['role_mapping']["default_role"])

        if update_required:
            log.info('Adding to the request_queue: ' + str(request))
            request_queue.append(request)

    # 6. Process the updates
    if len(request_queue) > 0:
        log.info("Executing updates with request_queue: " + str(request_queue))
        process_collection = xm_collection.create_collection(xm_person.modify_person, request_queue, config.roles['thread_count'])

        log.info("User update success: " + str(process_collection["response"]))
        log.info("User update failures: " + str(process_collection["errors"]))
    else:
        log.info("No updates required")

# entry point when file initiated
if __name__ == "__main__":

    # configure the logging
    logging.basicConfig(level=config.roles['logging']["level"], datefmt="%m-%d-%Y %H:%M:%Srm ",
                        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
                        handlers=[RotatingFileHandler(config.roles['logging']["file_name"], maxBytes=config.roles['logging']["max_bytes"], backupCount=config.roles['logging']['back_up_count'])])
    log = logging.getLogger(__name__)

    # time start
    time_util = xmatters.TimeCalc()
    start = time_util.get_time_now()
    log.info("Starting Process: " + time_util.format_date_time_now(start))

    # instantiate classes
    environment = xmatters.xMattersAPI(config.environment["url"], config.environment["username"], config.environment["password"])

    xm_roster = xmatters.xMattersRoster(environment)
    xm_person = xmatters.xMattersPerson(environment)
    xm_libraries = xmatters.xMattersLibraries(environment)
    xm_collection = xmatters.xMattersCollection(environment)

    # retrieve the group-roles mapping
    group_roles = None
    if config.roles['role_mapping']["enable_web_ui"]:
        libraries = xm_libraries.get_libraries(config.roles['role_mapping']["plan_name"])
        for script in libraries["data"]:
            if script["name"] == config.roles['role_mapping']["library_name"]:
                group_roles = json.loads(base64.b64decode(script["script"]))["data"]
                break
    else:
        with open(config.roles['role_mapping']["local_file_name"]) as f:  # read the json file
            group_roles = json.load(f)["data"]

    if group_roles:
        main()  # execute the main process

    # end the duration
    end = time_util.get_time_now()
    log.info("Process Duration: " + time_util.get_diff(end, start))
