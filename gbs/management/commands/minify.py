from django.core.management.base import BaseCommand, CommandError
from csscompressor import compress

class MinifyCSSCommand(BaseCommand):
    help = 'Minifies CSS'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # TODO
	# self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
