from enum import Enum

class Status(Enum):
    Draft = "Drafting"
    Awaiting_approval = "Awaiting Approvel"
    Approved = "Approved"
    Failed = "Failed"
    Waiting_User_Input = "Waiting User Input"