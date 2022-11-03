#
# Copyright 2013 Metamarkets Group Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


LEFT = "LEFT"
INNER = "INNER"


class Join:
    """ A base class for building a join operation """

    def __init__(self, left, right, right_prefix, condition, join_type=INNER):
        """ A class for building a right join """
        self.left = left
        self.right = right
        self.right_prefix = right_prefix
        self.condition = condition
        self.join_type = join_type

    @property
    def join(self):
        """ Gets the join as a dictionary """
        return {
            "left": self.left,
            "right": self.right,
            "rightPrefix": self.right_prefix,
            "condition": self.condition,
            "joinType": self.join_type,
            "type": "join",
        }

    @staticmethod
    def build_join(join):
        """ Builds the join dictionary """
        return join.join


class LeftJoin(Join):
    """ A class for building a left join operation """

    def __init__(self, left, right, right_prefix, condition):
        super(LeftJoin, self).__init__(left, right, right_prefix, condition, LEFT)


class InnerJoin(Join):
    """ A class for building a left join operation """

    def __init__(self, left, right, right_prefix, condition):
        super(InnerJoin, self).__init__(left, right, right_prefix, condition, INNER)


class CrossJoin(Join):
    """ A class for building a cross join operation """

    def __init__(self, left, right, right_prefix):
        super(CrossJoin, self).__init__(left, right, right_prefix, "1 = 1", INNER)
