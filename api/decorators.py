from functools import wraps

from api.db_manager import get_session, json_response_error
from api.global_var import NOT_LOGGED_IN


def api_check_login(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        try:
            user_data = get_session(request.headers.get("authorization", None))
        except:
            return json_response_error(NOT_LOGGED_IN)

        return f(request, user_data, *args, **kwargs)

    return wrapper
