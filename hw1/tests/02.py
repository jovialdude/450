test = {
  'name': 'Check hw1.pcap exists',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> assert "hw1.pcap.b64" in os.listdir(".")
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': False,
      'setup': r"""
      >>> import os
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
