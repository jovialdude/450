test = {
  'name': 'Alternative Sums',
  'points': 4,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> source =  "".join(inspect.getsourcelines(alternative_sum)[0])
          >>> assert "start" in source
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> import multiprocessing, time
          >>> p = multiprocessing.Process(target=alternative_sum, name="sum", args=(-5,-4))
          >>> p.start()
          >>> time.sleep(3)
          >>> assert not p.is_alive()
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> return_list = alternative_sum(-1,2)
          >>> assert return_list == []
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> return_list = alternative_sum(3,-10)
          >>> assert return_list == []
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> return_list = alternative_sum(3,30)
          >>> assert return_list == []
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> return_list = alternative_sum(10,7)
          >>> print(return_list)
          [10, 20, 40, 50, 70, 110, 160]
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> return_list = alternative_sum(10,20)
          >>> assert len(return_list) == 20
          >>> assert return_list[10] == 730
          >>> assert return_list[-1] == 22790
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from hw0 import alternative_sum
      >>> import multiprocessing, time, inspect
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
