# -*- coding: utf-8 -*-
#
#
# TheVirtualBrain-Scientific Package. This package holds all simulators, and
# analysers necessary to run brain-simulations. You can use it stand alone or
# in conjunction with TheVirtualBrain-Framework Package. See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2020, Baycrest Centre for Geriatric Care ("Baycrest") and others
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

import pytest
from tvb.interfaces.rest.server.resources.exceptions import InvalidIdentifierException
from tvb.interfaces.rest.server.resources.user.user_resource import GetUsersResource, GetProjectsListResource
from tvb.tests.framework.core.base_testcase import TransactionalTestCase
from tvb.tests.framework.core.factory import TestFactory


class TestUserResource(TransactionalTestCase):

    def transactional_setup_method(self):
        self.users_resource = GetUsersResource()
        self.projects_list_resource = GetProjectsListResource()

    def test_get_users_default(self):
        result = self.users_resource.get()
        assert type(result) is list
        assert len(result) == 1

    def test_get_users(self):
        TestFactory.create_user('Rest_User')
        result = self.users_resource.get()
        assert type(result) is list
        assert len(result) == 2

    def test_get_project_invalid_username(self):
        invalid_username = 'invalid-username'
        with pytest.raises(InvalidIdentifierException): self.projects_list_resource.get(invalid_username)

    def test_get_projects_empty(self):
        username = 'Rest_User'
        TestFactory.create_user(username)
        result = self.projects_list_resource.get(username)
        assert type(result) is list
        assert len(result) == 0

    def test_get_projects(self):
        username = 'Rest_User'
        user = TestFactory.create_user(username)
        TestFactory.create_project(user, 'Rest Project')
        result = self.projects_list_resource.get(username)
        assert type(result) is list
        assert len(result) == 1
