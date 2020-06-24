# the cookie used to access canvas
COOKIE = {
    "log_session_id": "xxx",
    "_normandy_session": "yyy",
    "_csrf_token": "zzz"
}

# the meaning of CLASS_INFO["VE203"]:
# the course has ID of 1599, whose homepage is:
# https://umjicanvas.com/courses/1599
# there are 3 courses per week:
# the 1st class on Tuesday, any weeks
# the 1st class on Thursday, any weeks
# the 1st class on Friday, only odd weeks
CLASS_INFO = {
    "VE203": {
        "id": 1599,
        "time": [(2, 1, False), (4, 1, False), (5, 1, True)]
    },
    "VE280": {
        "id": 1604,
        "time": [(2, 2, False), (4, 2, False), (5, 2, True)]
    },
    "VE401": {
        "id": 1611,
        "time": [(1, 3, False), (3, 3, False), (5, 3, True)]
    },
    "VE216": {
        "id": 1601,
        "time": [(2, 5, False), (4, 5, False), (5, 5, True)]
    },
}