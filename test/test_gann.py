import unittest
import numpy
from app.core.gann.gann import GANN
from unittest.mock import patch, MagicMock


class TestGANN(unittest.TestCase):
    def test_convert_weights_to_dna(self):
        _result = GANN.convert_weights_to_dna([[[1, 2], [3, 4]], [5, 6]])
        numpy.testing.assert_array_equal(_result, [1, 2, 3, 4, 5, 6])

    def test_convert_dna_to_weights(self):
        _shape = [1, 2, 1]
        _dna = [1, 2, 3, 4, 5, 6, 7]
        _result = GANN.convert_dna_to_weights(_dna, _shape)
        numpy.testing.assert_array_equal(_result[0], [[1, 2], [3, 4]])
        numpy.testing.assert_array_equal(_result[1], [[5], [6], [7]])

    def test_merge_dna(self):
        dna0 = [0, 2, 4, 6, 8]
        dna1 = [1, 3, 5, 7, 9]
        mask = [False, True, True, False, True]

        result = GANN.cross_over_dna(dna0, dna1, mask)

        numpy.testing.assert_array_equal(result, [0, 3, 5, 6, 9])

    @patch('app.core.gann.gann.monte_carlo.generate')
    def test_cross_over(self, mock_monte_carlo):
        mock_monte_carlo.return_value = [True, False, True, True, False]

        gann0 = GANN([4, 1], [0, 2, 4, 6, 8])
        gann1 = GANN([4, 1], [1, 3, 5, 7, 9])
        expected = [[[1], [2], [5], [7], [8]]]

        result = gann0.cross_over(gann1)

        numpy.testing.assert_array_equal(result.layer_weights, expected)

    @patch('app.core.gann.gann.random.random')
    def test_mutate_dna_with_mask(self, mock_random):
        mock_random.return_value = -3

        dna = [0, 2, 4, 6, 8]
        mask = [False, True, True, False, True]
        expected = [0, -5, -3, 6, 1]

        result = GANN.mutate_dna_with_mask(dna, mask)

        numpy.testing.assert_array_equal(result, expected)

    @patch('app.core.gann.gann.random.random')
    @patch('app.core.gann.gann.monte_carlo.generate')
    def test_mutate(self, mock_monte_carlo, mock_random):
        mock_monte_carlo.return_value = [False, False, True, False, False]
        mock_random.return_value = -3

        gann = GANN([4, 1], [0, 2, 4, 6, 8])
        expected = [[[0], [2], [-3], [6], [8]]]

        gann.mutate(0)

        numpy.testing.assert_array_equal(gann.layer_weights, expected)

    @patch('app.core.gann.gann.GANN.cross_over')
    def test_mate(self, mock_cross_over):
        mock_fake_gann = MagicMock()
        mock_cross_over.return_value = mock_fake_gann

        gann1 = GANN([4, 1], [0, 2, 4, 6, 8])
        gann2 = GANN([4, 1], [1, 3, 5, 7, 9])
        result = gann1.mate(gann2, 0.25)

        self.assertEqual(mock_fake_gann, result)
        mock_cross_over.assert_called_with(gann2)
        mock_fake_gann.mutate.assert_called_with(0.25)


if __name__ == '__main__':
    unittest.main()
