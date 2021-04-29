from oauth.models import *
from api.models import *


def get_session(token):
    try:
        data = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )
        return data
    except Exception as e:
        raise Exception(str(e))
        return None