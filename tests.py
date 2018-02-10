import unittest
import movie_cut


class TestCleanDir(unittest.TestCase):

    def test_clean_dir(self):
        self.assertEqual(movie_cut.clear_dir('lib', 'usr', 'local'), 'lib/usr/local')


if __name__ == '__main__':
    unittest.main()