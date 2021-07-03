class Player:
    def __init__(self, discord_id, mmr):
        self.__id = discord_id
        self.__mmr = mmr

    def get_id(self):
        return self.__id

    def get_mmr(self):
        return self.__mmr

    def set_mmr(self, mmr):
        self.__mmr = mmr

    def __eq__(self, other):
        if not isinstance(other, Player):
            return NotImplemented

        return self.__id == other.__id