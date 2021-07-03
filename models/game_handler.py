from models.game import Game


class GameHandler(object):
    def __init__(self, game_size):
        self.__game_size = game_size
        self.__queue = []
        self.__games = []

    def get_game_size(self):
        return self.__game_size

    def add_user(self, user):
        """
        Adds a user to the server's queue
        :param user: to add
        :return: true if added, false if not
        """
        if user not in self.__queue:
            self.__queue.append(user)

            # check if a game should be created
            if self.check_queue():
                self.create_game()

            return True
        else:
            return False

    def remove_user(self, user):
        """
        Removes a user from the server's queue
        :param user: to remove
        :return: true if removed, false if user not in queue
        """
        self.__queue.remove(user)

    def check_queue(self):
        """
        Checks to see if a game can be created
        :return: true if a game can be created, false if not
        """
        if len(self.__queue) >= self.__game_size:
            return True

    def get_users_in_queue(self):
        """
        Gets a list of users in the queue
        :return: list of users in queue
        """
        return self.__queue

    def create_game(self):
        """
        Creates a game, removing the users from the queue
        :return: void
        """
        users = []

        for i in range(self.__game_size):
            users.append(self.__queue.pop(i))

        # TODO: Generate way to differentiate voting for games

        game = Game(users)
        self.__games.append(game)
