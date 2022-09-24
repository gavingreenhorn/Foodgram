from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = name.capitalize()

    def post_migration(self, sender, **kwargs):
        """Code to run after migration is completed."""
        verbosity = kwargs['verbosity']
        self.setup_permissions(verbosity=verbosity)

    def setup_permissions(self, **kwargs) -> None:
        """Get and set permissions for the groups that should have them."""
        from django.contrib.contenttypes.models import ContentType
        from django.contrib.auth.models import Group, Permission

        verbosity = kwargs['verbosity']
        if verbosity >= 1:
            print('Setting up admin permissions for user model.')
        user_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(
                get_user_model()))
        admin, created = Group.objects.get_or_create(name='admin')
        # admin_permissions = (
        #     list(filter(
        #         lambda perm: (perm.codename.startswith('view_')
        #                       or perm.codename.startswith('add_')
        #                       or perm.codename.st
        #                       or perm.codename.startswith('delete_')),
        #         user_permissions))
        # )
        admin.permissions.add(*user_permissions)
        if verbosity >= 1:
            print('Admin permissions for user model set.')

    def ready(self) -> None:
        post_migrate.connect(self.post_migration, sender=self)
