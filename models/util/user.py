#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_user_table(**kwargs):
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "user_id" in kwargs and kwargs["user_id"] is not None:
        conditions_of_where.append("id = {0}".format(kwargs["user_id"]))
    elif "email" in kwargs and kwargs["email"] is not None:
        conditions_of_where.append("email = '{0}'".format(kwargs["email"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some condition, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT * FROM user_ {0} ORDER BY id
        ) AS user_
    """.format(where_clause)

    return subquery_table
