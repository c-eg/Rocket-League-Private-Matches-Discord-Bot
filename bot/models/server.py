from bot.models.game import Game


class Server(object):
    def __init__(self, game_size=6):
        self.__game_size = game_size
        self.__queue = []
        self.__games = []

    def add_user(self, user):
        if user not in self.__queue:
            self.__queue.append(user)

            if self.check_queue():
                self.create_game()

    def remove_user(self, user):
        self.__queue.remove(user)

    def check_queue(self):
        if len(self.__queue) >= self.__game_size:
            return True

    def get_users_in_queue(self):
        return self.__queue

    def create_game(self):
        users = []

        for i in range(self.__game_size):
            users.append(self.__queue.pop(i))

        # TODO: Generate way to differentate voting for games

        game = Game(users)
        self.__games.append(game)
