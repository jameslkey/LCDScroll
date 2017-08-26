# -*- coding: utf-8 -*-
"""
Comments go here!!!

:program: LcdScroll
:file: steps
:platform: Cross-Platform
:synopsis: Change this text.

.. moduleauthor:: James L. Key <james@bluepenguinslutions.com>

"""

from behave import given, when, then, step


@given('we have behave installed')
def step_impl(context):
    """

    Args:
        context:
    """
    pass


@when('we implement {number:d} tests')
def step_impl(context, number):  # -- NOTE: number is converted into integer
    assert number > 1 or number == 0
    context.tests_count = number


@then('behave will test them for us!')
def step_impl(context):
    """

    Args:
        context:
    """
    assert context.failed is False
    assert context.tests_count >= 0
