from functools import wraps

from api.db_manager import get_session, json_response_error
from api.global_var import NOT_LOGGED_IN, NOT_OWNER


def api_check_login(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        try:
            session = get_session(request.headers.get("authorization", None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        return f(request, session, *args, **kwargs)

    return wrapper


def api_check_owner(f):
    @wraps(f)
    def wrapper(request, user_data, *args, **kwargs):
        if not user_data["is_owner"]:
            return json_response_error(NOT_OWNER)
        return f(request, *args, **kwargs)

    return wrapper
