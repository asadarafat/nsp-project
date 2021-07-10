from jsonbender.core import Transport


class BenderTestMixin(object):
    def assert_bender(self, bender, source, expected_value,
                      context=None, msg=None):
        context = context or {}
        got = bender(Transport(source, context))
        self.assertEqual(got, expected_value, msg)

