import unittest
from BCH import BCH

class TestBCH(unittest.TestCase):
    def setUp(self):
        self.bch = BCH(n=15, k=5)

    def test_encoding_decoding_no_errors(self):
        """Test encoding and decoding with no errors."""
        message = [1, 0, 1, 1, 0]  # 5-bit message
        encoded = self.bch.koduj(message)
        self.assertEqual(len(encoded), 15)  # Check encoded length
        decoded = self.bch.dekoduj(encoded)
        self.assertEqual(message, decoded)  # Check if decoded matches original

    def test_single_error_correction(self):
        """Test correction of single error."""
        message = [1, 1, 0, 0, 1]
        encoded = self.bch.koduj(message)
        # Introduce single error
        encoded[5] ^= 1  # Flip bit at position 5
        decoded = self.bch.dekoduj(encoded)
        self.assertEqual(message, decoded)

    def test_double_error_correction(self):
        """Test correction of two errors."""
        message = [1, 0, 1, 1, 1]
        encoded = self.bch.koduj(message)
        # Introduce two errors
        encoded[3] ^= 1
        encoded[10] ^= 1
        decoded = self.bch.dekoduj(encoded)
        self.assertEqual(message, decoded)

    def test_triple_error_correction(self):
        """Test correction of three errors."""
        message = [1, 0, 0, 1, 1]
        encoded = self.bch.koduj(message)
        # Introduce three errors
        encoded[2] ^= 1
        encoded[7] ^= 1
        encoded[12] ^= 1
        decoded = self.bch.dekoduj(encoded)
        self.assertEqual(message, decoded)

    def test_too_many_errors(self):
        """Test behavior with more than 3 errors."""
        message = [0, 1, 1, 0, 1]
        encoded = self.bch.koduj(message)
        # Introduce four errors
        encoded[2] ^= 1
        encoded[7] ^= 1
        encoded[12] ^= 1
        encoded[14] ^= 1
        decoded = self.bch.dekoduj(encoded)
        # May not match original message due to too many errors
        self.assertEqual(len(decoded), 5)  # But should still return k bits

    def test_invalid_message_length(self):
        """Test handling of invalid message length."""
        message = [1, 0, 1]  # Too short
        with self.assertRaises(ValueError):
            self.bch.koduj(message)

    def test_invalid_received_length(self):
        """Test handling of invalid received message length."""
        received = [1] * 10  # Wrong length
        with self.assertRaises(ValueError):
            self.bch.dekoduj(received)

if __name__ == '__main__':
    unittest.main() 