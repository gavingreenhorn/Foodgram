from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


class RecipesConfig(AppConfig):
    default_auto_field = settings.DEFAULT_AUTO_FIELD
    name = 'recipes'
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
            print('Setting up admin permissions.')
        tag_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(
                self.get_model('Tag')))
        ingredient_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(
                self.get_model('ingredient')))
        recipe_permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(
                self.get_model('Recipe')))
        admin, created = Group.objects.get_or_create(name='admin')
        admin_permissions = (
            list(filter(
                lambda perm: perm.codename in (
                    'add_tag', 'delete_tag',
                    'change_tag'),
                tag_permissions))
            + list(filter(
                lambda perm: perm.codename in (
                    'add_ingredient', 'delete_ingredient',
                    'change_ingredient'),
                ingredient_permissions))
            + list(filter(
                lambda perm: perm.codename in (
                    'delete_recipe',
                    'change_recipe'),
                recipe_permissions))
        )
        admin.permissions.add(*admin_permissions)
        if verbosity >= 1:
            print('Admin permissions set.')

    def ready(self) -> None:
        post_migrate.connect(self.post_migration, sender=self)
