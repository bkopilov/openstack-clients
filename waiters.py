import time


def get_value(value, key, client):
    """
    decide how to handle returned data from client commands
    two options: returned dictionary or returned object.
    we change the returned data to a dictionay
    """
    if client is None:
        return value.__dict__[key]
    elif "glance" in str(client):
        return value[key]
    elif "cinder" in str(client):
        return value.__dict__[key]
    elif "nova" in str(client):
        return value.__dict__[key]


class Waiter(object):
    RETRY_COUNT = 15
    SLEEP_BETWEEN_RETRY = 3
    PASS = 1
    FAIL = 0

    @classmethod
    def wait_for_resource_status(cls, function, waiter_id, status, message="",
                                 client=None, retry_count=RETRY_COUNT,
                                 sleep_between_retry=SLEEP_BETWEEN_RETRY,
                                 **function_args):
        """
        :param function: caller function
        :param waiter_id:  the resource id we are waiting for
        :param status:  the resource expected status
        :param function_args:  the args the function sends
        :param message:  print a message
        :param client:  the resource client
        :param retry_count:  how many time to call to function
        :param sleep_between_retry:  sleep time between calls.
        :param **function_args  -> all params that sent to function
        :return pass or fail:
        """
        start_count = 0
        while start_count < retry_count:
            # we assume that we asked for a resource_id -
            # returned the resources
            # example: glance.images.get("image_id") will return the value
            # as a dictionary
            resource = function(**function_args)
            if not function_args:
                # running a list command
                for value in resource:
                    value_id = get_value(value, 'id', client)
                    if value_id == waiter_id:
                        print message + " found waiter id: {0}\n"\
                            .format(waiter_id)
                        if get_value(value, "status", client) == status:
                            print message + " status is: {0}\n".format(status)
                            return cls.PASS
                        elif get_value(value, "status", client) == "error":
                            print message + "status is: {0}\n".format("error")
                            return cls.FAIL
            else:
                # assume user asked for get_command
                if get_value(resource, 'id', client) == waiter_id:
                        print message + " found waiter id: {0} ".\
                            format(waiter_id)
                        if get_value(resource, "status", client) == status:
                            print message + " status is: {0}".format(status)
                            return cls.PASS
                        elif get_value(resource, "status", client) == "error":
                            print message + "status is: {0}\n".format("error")
                            return cls.FAIL
            time.sleep(sleep_between_retry)
            start_count += 1
        raise RuntimeError("Timeout expires")

    @classmethod
    def wait_for_resource_deletion(cls, function, waiter_id, message="",
                                   client=None, retry_count=RETRY_COUNT,
                                   sleep_between_retry=SLEEP_BETWEEN_RETRY,
                                   **function_args):
        """
        :param function: caller function
        :param waiter_id:  the resource id we are waiting for deletion
        :param status:  the resource expected status
        :param function_args:  the args the function sends
        :param message:  print a message
        :param client:  the resource client
        :param retry_count:  how many time to call to function
        :param sleep_between_retry:  sleep time between calls.
        :param **function_args  -> all params that sent to function
        :return pass or fail:
        """
        start_count = 0
        while start_count < retry_count:
            # we assume that we asked for a resource_id -returned the resource
            # example: glance.images.get("image_id") will return the value as
            #  a dictionary
            resource = function(**function_args)
            if not function_args:
                # running a list command
                deleted = True
                for value in resource:
                    value_id = get_value(value, 'id', client)
                    if value_id == waiter_id:
                        deleted = False
                        print message + " found waiter id: {0}\n"\
                            .format(waiter_id)
                if deleted:
                    return cls.PASS
            else:
                # assume user asked for get_command
                if get_value(resource, 'id', client) == waiter_id:
                        print message + " found waiter id: {0} "\
                            .format(waiter_id)

            time.sleep(sleep_between_retry)
            start_count += 1
        raise RuntimeError("Timeout expires")
