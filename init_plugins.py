class Plugin:
    def initialize(self):
        raise NotImplementedError


class LoggingPlugin(Plugin):
    def initialize(self):
        print("Logging plugin initialized")


class DatabasePlugin(Plugin):
    def initialize(self):
        print("Database plugin initialized")


class CachePlugin(Plugin):
    def initialize(self):
        print("Cache plugin initialized")


def initialize_plugins(plugin_classes):
    plugins = []

    for plugin_class in plugin_classes:
        plugin = plugin_class()
        plugin.initialize()
        plugins.append(plugin)

    return plugins


plugin_list = [
    LoggingPlugin,
    DatabasePlugin,
    CachePlugin,
]

initialized_plugins = initialize_plugins(plugin_list)
