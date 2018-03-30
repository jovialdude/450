test = {
  'name': 'Python Version Check',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> python_version = get_version()
          >>> assert "3" in python_version
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> python_version = get_version()
          >>> assert "\n" not in python_version
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> python_version = get_version()
          >>> assert "GCC" not in python_version
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> source =  "".join(inspect.getsourcelines(get_version)[0])
          >>> assert "sys.version" in source
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from hw0 import get_version
      >>> import inspect
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
