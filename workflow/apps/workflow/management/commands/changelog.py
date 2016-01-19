# -*- coding: utf-8 -*-
import os
from django.core.management.base import BaseCommand, CommandError
from workflow.apps.workflow.models import Changelog
from _changelog_parser import ChangelogParser


class Command(BaseCommand):
    help = 'Update CHANGELOG posts'

    def handle(self, *args, **options):
        from django.conf import settings
        self.CHANGELOG_POST = Changelog.objects.all()

        changelog_parser = ChangelogParser(
            changelog_path=os.path.join(settings.BASE_DIR, 'CHANGELOG'),
            block_title='Update',
            block_start='--',
            block_stop='=='
        )
        for block in changelog_parser.blocks():
            if self.block_exist(block):
                post = Changelog.objects.get(title=block.title)
                text = ''.join([item.text for item in block.items()])
                if post.text != text:
                    post.text = text
                    post.save()
                    print('\033[94m[UPDATE]\033[0m %s' % block.title)
            else:
                post = Changelog(
                    title=block.title,
                    text=''.join([item.text for item in block.items()])
                )
                post.save()
                print('\033[92m[WRITE]\033[0m %s' % block.title)

    def block_exist(self, block):
        """ 'block_exist' check if block already exist in database
        """
        if [post.title for post in self.CHANGELOG_POST if post.title == block.title]:
            return True
        return False