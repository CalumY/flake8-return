import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_return.errors import (
    ImplicitReturn,
    ImplicitReturnValue,
    UnnecessaryAssign,
    UnnecessaryReturnNone,
)
from flake8_return.visitors import ReturnVisitor


def _ids(values):
    return ['' for _ in values]


error_not_exists = (
    # without return value
    """
    def x(y):
        if not y:
            return
        return
    """,
    """
    def x(y):
        if y:
            return
        print()
    """,
    # with return value
    """
    def x(y):
        if not y:
            return 1
        return 2
    """,
    """
    def x(y):
        if not y:
            return 1
        elif y - 10:
            return 2
        else:
            return 3
    """,
    """
    def x(y):
        for i in range(10):
            if i > 100:
                return i
        else:
            return 1
    """,
    """
    def x(y):
        try:
            return 1
        except:
            return 2
    """,
    """
    def x(y):
        try:
            return 1
        finally:
            return 2
    """,
    # inner function
    """
    def x(y):
        if not y:
            return 1
        def inner():
            return
        return 2
    """,
    """
    def x(y):
        if not y:
            return
        def inner():
            return 1
    """,
    # raise as last return
    """
    def x(y):
        if not y:
            return 1
        raise Exception
    """,
    # last line in while loop
    """
    def x(y):
        while True:
            if y > 0:
                return 1
            y += 1
    """,
    # exclude empty functions
    """
    def x(y):
        return None
    """,
    # return inner with statement
    """
    def x(y):
        with y:
            return 1
    """,
    # assign return value
    """
    def x(y):
        a = 1
        print(a)
        return a
    """,
    """
    def x():
        a = 1
        if y:
            return a
        a = a + 2
        print(a)
        return a
    """,
    """
    def x():
        a = {}
        a['b'] = 2
        return a
    """,
    """
    def x():
        a = []
        a.append(2)
        return a
    """,
    """
    def x():
        a = lambda x: x
        a()
        return a
    """,
)


@pytest.mark.parametrize('src', error_not_exists, ids=_ids(error_not_exists))
def test_error_not_exists(src):
    assert_not_error(ReturnVisitor, src)


implicit_return_value = (
    """
    def x(y):
        if not y:
            return  # here
        return 1
    """,
)


@pytest.mark.parametrize(
    'src', implicit_return_value, ids=_ids(implicit_return_value)
)
def test_implicit_return_value(src):
    assert_error(ReturnVisitor, src, ImplicitReturnValue)


unnecessary_return_none = (
    """
    def x(y):
        if not y:
            return
        return None  # here
    """,
)


@pytest.mark.parametrize(
    'src', unnecessary_return_none, ids=_ids(unnecessary_return_none)
)
def test_unnecessary_return_none(src):
    assert_error(ReturnVisitor, src, UnnecessaryReturnNone)


implicit_return = (
    # if/elif/else
    """
    def x(y):
        if not y:
            return 1
        # here
    """,
    """
    def x(y):
        if not y:
            print()  # here
        else:
            return 2
    """,
    """
    def x(y):
        if not y:
            return 1
        elif y - 100:
            print()  # here
        else:
            return 2
    """,
    """
    def x(y):
        if not y:
            return 1
        else:
            print()  # here
    """,
    # for
    """
    def x(y):
        for i in range(10):
            if i > 10:
                return i
        # here
    """,
    """
    def x(y):
        for i in range(10):
            if i > 10:
                return i
        else:
            print()  # here
    """,
)


@pytest.mark.parametrize('src', implicit_return, ids=_ids(implicit_return))
def test_implicit_return(src):
    assert_error(ReturnVisitor, src, ImplicitReturn)


unnecessary_assign = (
    """
    def x():
        a = 1
        return a  # here
    """,
    """
    def x():
        a = 1
        print()
        return a  # here
    """,
    """
    def x():
        a = 1
        print(a)
        a = 2
        return a  # here
    """,
    """
    def x():
        a = 1
        if True:
            return a  # here
        a = 2
        print(a)
        return a
    """,
)


@pytest.mark.parametrize(
    'src', unnecessary_assign, ids=_ids(unnecessary_assign)
)
def test_unnecessary_assign(src):
    assert_error(ReturnVisitor, src, UnnecessaryAssign)
