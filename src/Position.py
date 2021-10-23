from enum import Enum


class Position(Enum):
    RB = 'RB'
    QB = 'QB'
    WR = 'WR'

    @staticmethod
    def str_to_enum(str_val: str):
        if not str:
            return None
        str_val = str_val.strip().upper()
        if str_val == Position.RB.value:
            return Position.RB
        if str_val == Position.WR.value:
            return Position.WR
        if str_val == Position.QB.value:
            return Position.QB
        return None
