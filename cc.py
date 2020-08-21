import os
import pymysql

root = os.path.dirname(os.path.abspath(__file__))

ssl_options = {
    'ca': os.path.join(root, 'rds-combined-ca-bundle.pem'),
    'check_hostname': False
}


def change_database(target):
    return change_password(
        host=target["endpoint"],
        user=target["user"],
        old_password=target["old_password"],
        new_password=target["new_password"]
    )


# Generate new password with minimum 26 character length (Reference link)
#
def change_password(host, user, old_password, new_password):
    try:

        print('Tring to connect to database with user: {}'.format(user))
        conn = None
        conn = pymysql.connect(
            host=host, user=user, password=old_password, ssl=ssl_options
        )
        with conn.cursor() as cursor:

            sql = "SET PASSWORD FOR '{}'@'{}' = PASSWORD('{}');".format(
                user, '%', new_password
            )
            print(
                'Tring to update the password for user: {} with sql below:'.
                format(user)
            )
            print("     {}".format(sql))

            cursor.execute(sql)

            print('Update the password for user: {}     ===> OK'.format(user))
            conn.commit()

    except Exception as ex:
        print('Update the password for user: {}     ===> FAILED'.format(user))
        print(ex)

    finally:
        if conn:
            conn.close()


def get_connection(host, user, password):
    try:
        conn = None
        conn = pymysql.connect(
            host=host, user=user, password=password, ssl=ssl_options
        )
        print('Connecting to host: {}   ===> OK'.format(host))
        return conn

    except Exception as ex:
        print('Connecting to host: {}   ===> FAILED'.format(host))
        print(ex)
    finally:
        if conn:
            conn.close()


target = {
    'endpoint': 'database-1.cluster-cda3xpvusvd0.us-west-2.rds.amazonaws.com',
    'user': 'admin',
    'new_password': '',
    'old_password': '',
}

get_connection(
    host=target["endpoint"],
    user=target["user"],
    password=target['old_password']
)

change_database(target)

get_connection(
    host=target["endpoint"],
    user=target["user"],
    password=target['new_password']
)
