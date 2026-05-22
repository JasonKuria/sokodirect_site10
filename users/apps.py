from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # this method is called when the app is ready,
    # we will use it to import the signals and connect them
    # the apps knows about the signals(users.signals) and will connect them when the app is ready
    def ready(self):
        import users.signals # import the signals to connect them when the app is ready
