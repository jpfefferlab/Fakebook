from django.apps import AppConfig

class ConfigurationConfig(AppConfig):
    name = 'configuration'

    # THIS WOULD CAUSE THE configuration to be loaded even on database migration, making the db migration causing the table to exist fail
    # django is beautiful thing
    # def ready(self):
    #     print("Ensuring configuration exists...")
    #     from configuration.models import ensure_config_exists
    #     ensure_config_exists()
