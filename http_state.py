from enum import Enum

class States(Enum):
    OK = "OK"
    Not_Found = "Not Found"
    Forbidden = "Forbidden"
    Moved_Permanently = "Moved Permanently"
    Bad_Request = "Bad Request"
    Unauthorized = "Unauthorized"

# def get_states_number(state: States) -> int:
#     states_number = {
#         States.OK.name: "200",
#         States.Not_Found.name: "404",
#         States.Forbidden.name: "403",
#         States.Moved_Permanently.name: "301",
#         States.Bad_Request.name: "400",
#         States.Unauthorized.name: "401",
#     }
#     return states_number[state]

def get_states_number(state: States) -> int:
    states_number = {
        States.OK: "200",
        States.Not_Found: "404",
        States.Forbidden: "403",
        States.Moved_Permanently: "301",
        States.Bad_Request: "400",
        States.Unauthorized: "401",
    }
    return states_number[state]
