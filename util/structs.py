#
# Copyright 2026 Krypton Yousuke.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from pydantic import BaseModel, ConfigDict
class Triang3lObject(BaseModel):
    '''
    The base for all the Triang3l safe and private structs.
    '''
    
    model_config = ConfigDict(validate_assignment=True)
    
    def all_valid(self) -> dict | bool:
        self_dict = self.__dict__
        values = self_dict.values()
        for value in values:
            if value is None:
                return False
        return self.__dict__

# Simple structs
class colors:
    '''
    Triang3l private colors.
    '''
    blue   = 0x1177fc
    white  = 0xc4c4c4
    purple = 0xbb00ff
    green  = 0x07d400
    red    = 0xc41e0c


class Group(Triang3lObject):
    '''
    Represents a group.
    '''
    group_hash: str | None = None
    group_id: int | None = None
    server_owner_id: int | None = None
    server_owner_name: str | None = None
    group_name: str | None = None

class BannedUser(Triang3lObject):
    '''
    Represents a user who was banned.
    '''
    username: str | None = None
    display_name: str | None = None
    user_id: int | None = None
    reason: str | None = None
    in_server_id: int | None = None

