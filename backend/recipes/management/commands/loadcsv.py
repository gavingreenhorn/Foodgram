from os.path import basename, dirname, abspath

from django.core.management.base import BaseCommand, CommandError

from ._utils import load_model_data


APP_NAME = basename(dirname(
    dirname(dirname(abspath(__file__)))))
FILES = {
    'ingredients': (APP_NAME, ('name', 'measurement_unit')),
    'tags': (APP_NAME, ('name', 'color', 'slug')),
    'users': ('users', (
        'username', 'first_name', 'last_name',
        'email', 'password', 'is_staff'))
}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('source', type=str)
        parser.add_argument('modelname', type=str)
        parser.add_argument('related-field', nargs='?', default=None, type=str)

    def handle(self, *args, **options):
        app_label, headers = FILES[options['source']]
        try:
            load_model_data(
                app_label,
                headers,
                source=options['source'],
                modelname=options['modelname'],
                related_field=options['related-field']
                )
        except Exception as ex:
            raise CommandError(ex)
        else:
            self.stdout.write(self.style.SUCCESS(
                'Successfully loaded "%s" data' % options['modelname']))
