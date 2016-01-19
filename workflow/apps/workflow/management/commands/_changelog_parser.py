#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


class Block(object):
    """
    Represent an section of CHANGELOG equivalent at one version.
    This contains any items of her section.

    Attributes:
        line_number -- line number of block start
        title       -- title of CHANGELOG section
        _items      -- lines content in the block
    """

    __slots__ = ['line_number', 'title', '_items']

    class Item(object):
        """
        Represent one line of current section of CHANGELOG. 

        Attributes:
            line_number -- number of line in CHANGELOG
            text        -- text of line
        """
        __slots__ = ['text', 'line_number', '_bad_char']

        def __init__(self, line_number, text):
            self.text = text
            self.line_number = line_number

        def __repr__(self):
            return self.text

    def __init__(self, line_number, title):
        self.line_number = line_number
        self.title = title
        self._items = []

    def __repr__(self):
        return self.title

    def add_item(self, item):
        """ 'add_item' append item in self._items
        """
        self._items.append(item)

    def items(self):
        for item in self._items:
            yield item


class ChangelogParser(object):
    """
    CHANGELOG Parser.
    Parse file define in 'changelog_path' attribute, and define Block by
    section of this and Item by lines content in this one.

    Attributes:
        changelog_path -- path of CHANGELOG file
        block_title    -- title of CHANGELOG section or just parts of this
        block_start    -- symbol representing the beginning of section
        block_stop     -- symbol representing the end of section
        _tmp_block     -- temp instance of 'Block' object
        _blocks        -- all instance of 'Block' representing CHANGELOG parts
    """

    __slots__ = ['changelog_path', 'block_title', 'block_start', 
                 'block_stop', '_tmp_block', '_blocks']

    def __init__(self, changelog_path, block_title, block_start, block_stop):
        self.changelog_path = changelog_path
        self.block_title = block_title
        self.block_start = block_start
        self.block_stop = block_stop
        self._tmp_block = None
        self._blocks = []
        try:
            with open(changelog_path) as f:
                self.process_file(f)
        except IOError:
            print("The file '%s' does not exist" % changelog_path)

    def process_file(self, f):
        """ 'process_file' iter on lines content in f file 
            and call 'process_line' on each of them.
        """
        for line_number, text in enumerate(f):
            self.process_line(line_number, text)
        if not self._blocks:
            print('No blocks found with the currents arguments')

    def process_line(self, line_number, text):
        """ 'process_line' check line representation.
            If text start with 'self.block_title', function call 'open_block'
            to define new temp Block in 'self._tmp_block'.

            Alternatively if 'self._tmp_block' is already defined, and text not
            start with 'self.block_start', 'self.block_stop' and not empty, 
            function call 'new_item' function to define new Item and append 
            it to the current temp Block.

            If text start with 'self.block_stop', function call 'close_block' 
            to add 'self._tmp_block' at 'self._blocks'
        """
        if text.startswith(self.block_title):
            self.open_block(line_number, text)
            return
        if self._tmp_block:
            if not text.startswith(self.block_start)\
                and not text.startswith(self.block_stop)\
                and text.strip():
                    self.new_item(line_number, text)
            if text.startswith(self.block_stop):
                self.close_block()

    def open_block(self, line_number, text):
        """ 'open_block' define a new block in 'self._tmp_block'
        """
        self._tmp_block = Block(line_number, text) 

    def close_block(self):
        """ 'close_block' append block defined in 'self._tmp_block' to 'self._blocks'
        """
        self._blocks.append(self._tmp_block)
        self._tmp_block = None

    def new_item(self, line_number, text):
        """ 'new_item' define a new Item instance and append it to block defined in
            'self._tmp_block'
        """
        item = Block.Item(line_number, text)
        self._tmp_block.add_item(item)

    def blocks(self):
        for block in self._blocks:
            yield block
    

if __name__ == '__main__':
    # Exemple of Parser use
    parser = ChangelogParser(
        changelog_path=os.path.join(os.path.dirname(__file__), '..', 'CHANGELOG'),
        block_title='Update',
        block_start='--',
        block_stop='=='
    )
    for block in parser.blocks():
        print(block.title)
        for item in block.items():
            print(item)
