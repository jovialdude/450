test = {
  'name': 'Sorted Scores',
  'points': 4,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> names = order_scores()
          >>> assert "name" not in names
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> names = order_scores()
          >>> names
          ['Shawn', 'Samuel', 'Allen', 'Mabel', 'Ian', 'Clayton', 'Ethan', 'Kate', 'Nicholas', 'Mable']
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from hw0 import order_scores
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
