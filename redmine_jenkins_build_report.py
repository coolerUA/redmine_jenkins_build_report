import sys
import os
import psycopg2
import time

psql_server = '192.168.0.1'
psql_user = 'redmine'
psql_database = 'redmine'
psql_password = 'redmine'
psql_port = '15434'
project_id = '2'  #
tracker = '1'  # 1 - Error
status_id = '1'  # 1 - New
assigned_to_id = '5'  #
priority_id = '5'  # 5 - Immidiate
author_id = '17'  #
lock_version = '2'  # ?
root_id = '1'  #


def print_usage():
    print("Using: \n"
          + os.path.dirname(__file__)+"/" + os.path.basename(__file__) + " ${JOB_NAME} ${BUILD_NUMBER} ${BUILD_URL} "
          "STATUS\n"
          "where:\n"
          "${JOB_NAME} - Name of the project of this build, such as \"foo\" or \"foo/bar\"\n"
          "${BUILD_NUMBER} - The current build number, such as \"153\"\n"
          "${BUILD_URL} - Full URL of this build, like http://jenkins_server:port/job/foo/15/ \n"
          "STATUS - status of build. Any keyword you want.")


try:
    subject = 'Build # ' + sys.argv[2] + 'status ' + sys.argv[4] + ' for ' + sys.argv[1]
    description = 'Task ' + sys.argv[1] + ' ' + sys.argv[4] + ' to build. Job #' + sys.argv[2] + \
                  '. See full build log on "' + sys.argv[3] + '":' + sys.argv[3]

    due_date = time.strftime("%Y-%m-%d")
    created_on = time.strftime("%Y-%m-%d %H:%M:%S.000000")
    updated_on = created_on
    start_date = due_date

    dsn = "host={} dbname={} user={} password={} port={}".format(psql_server, psql_database, psql_user, psql_password,
                                                                 psql_port)

    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    query = ("INSERT INTO public.issues( tracker_id, project_id, subject, description, due_date, "
             "status_id, assigned_to_id, priority_id, author_id, lock_version, "
             "created_on, updated_on, start_date, root_id, lft, rgt) "
             "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'"
             ");").format(
             tracker, project_id, subject, description, due_date, status_id, assigned_to_id, priority_id,
             author_id, lock_version, created_on, updated_on, start_date, root_id, 1, 1)
    print(query)
    cur.execute(query)
    conn.commit()

except IndexError:
    print_usage()
