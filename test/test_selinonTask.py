#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ####################################################################
# Copyright (C) 2016  Fridolin Pokorny, fpokorny@redhat.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# ####################################################################

import pytest
from flexmock import flexmock
from selinon import SelinonTask
from selinon.retry import Retry
from selinon.storagePool import StoragePool
from selinonTestCase import SelinonTestCase


class _MyTask(SelinonTask):
    def run(self, node_args):
        super().run(node_args)


_MYTASK_PARAMS = {
    'task_name': 'task1',
    'flow_name': 'flow1',
    'parent': {
        'task2': '<task2-id>',
        'flow2': {
            'task3': ['<flow2-task2-id>']
        }
    },
    'dispatcher_id': '<dispatcher-id>'
}


task_test = [
    (_MyTask(**_MYTASK_PARAMS), _MYTASK_PARAMS)
]


@pytest.mark.parametrize("task, params", task_test)
class TestSelinonTask(SelinonTestCase):
    def test_init(self, task, params):
        assert task.task_name == params['task_name']
        assert task.flow_name == params['flow_name']
        assert task.parent == params['parent']
        assert task.dispatcher_id == params['dispatcher_id']

    def test_parent_task_result(self, task, params):
        parent_task_name = 'task2'
        parent_task_id = params['parent'][parent_task_name]
        result = 'foo'

        flexmock(StoragePool)\
            .should_receive('retrieve')\
            .with_args(params['flow_name'], parent_task_name, parent_task_id)\
            .and_return(result)

        assert task.parent_task_result(parent_task_name) == result

    def test_parent_task_result_error(self, task, params):
        with pytest.raises(KeyError):
            task.parent_task_result('some-not-existing-task')

    def test_parent_flow_result(self, task, params):
        parent_flow_name = 'flow2'
        parent_task_name = 'task3'
        index = 0
        parent_task_id = params['parent'][parent_flow_name][parent_task_name][index]
        result = 'foo'

        flexmock(StoragePool)\
            .should_receive('retrieve')\
            .with_args(parent_flow_name, parent_task_name, parent_task_id)\
            .and_return(result)

        assert task.parent_flow_result(parent_flow_name, parent_task_name, index=0) == result

    def test_parent_flow_result_error_no_flow(self, task, params):
        with pytest.raises(KeyError):
            task.parent_flow_result('some-not-existing-flow', 'task2', index=0)

    def test_parent_flow_result_error_no_task(self, task, params):
        with pytest.raises(KeyError):
            task.parent_flow_result('flow2', 'some-not-existing-task', index=0)

    def test_parent_flow_result_error_index(self, task, params):
        with pytest.raises(IndexError):
            task.parent_flow_result('flow2', 'task3', index=42)

    def test_storage(self, task, params):
        storage_instance = 'some-storage'

        flexmock(StoragePool)\
            .should_receive('get_storage_by_task_name')\
            .with_args(params['task_name'])\
            .and_return(storage_instance)

        assert task.storage == storage_instance

    def test_retry(self, task, params):
        with pytest.raises(Retry):
            task.retry()