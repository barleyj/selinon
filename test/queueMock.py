#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ######################################################################
# Copyright (C) 2016-2017  Fridolin Pokorny, fridolin.pokorny@gmail.com
# This file is part of Selinon project.
# ######################################################################


class QueueMock(object):
    queue_string = 'queue_%s'

    def __getitem__(self, item):
        return self.queue_string % item
