# class Hamming:
#     def __init__(self, n=15, k=11):
#         """
#         Class handling encoding and decoding using Hamming code (15,11).
#         :param n: Length of encoded data (15 for Hamming code).
#         :param k: Length of original data (11 for Hamming code, 8 for this task).
#         """
#         self.n = n  # Length of encoded data (15)
#         self.k = k  # Length of original data (8)
#         self.parity_bits = 4  # For Hamming code (15,11) we have 4 parity bits
#
#     def _calculate_parity_bits(self, data):
#         """
#         Calculate parity bits based on input data.
#         :param data: Original input data as a list of bits (e.g., [1, 0, 1, 0])
#         :return: Parity bits as a list of bits.
#         """
#         parity = [0] * self.parity_bits
#
#         # Calculate parity bits
#         for i in range(self.parity_bits):
#             mask = 1 << i
#             for j in range(self.n):
#                 if j & mask:
#                     parity[i] ^= data[j]
#
#         return parity
#
#     def encode(self, data):
#         """
#         Encode data using Hamming code (15,11).
#         :param data: Original input data as a string of 0s and 1s (e.g., "11010011")
#         :return: Encoded data as a list of bits.
#         """
#         if len(data) != 8:  # Expecting 8 bits of data
#             raise ValueError("Input data length must be 8 bits.")
#
#         # Convert input data to a list of bits
#         data_bits = [int(bit) for bit in data]
#
#         # Encoded message - 15 bits, initialize with zeros
#         encoded = [0] * self.n
#         data_index = 0
#
#         # Insert data bits at appropriate positions, skipping parity bit positions
#         for i in range(self.n):
#             # Parity bits should be at positions 0, 1, 3, 7 (1-based indexing)
#             if i == 0 or i == 1 or i == 3 or i == 7:
#                 continue
#             encoded[i] = data_bits[data_index]
#             data_index += 1
#
#         # Calculate parity bits
#         parity_bits = self._calculate_parity_bits(encoded)
#
#         # Insert parity bits at appropriate positions
#         encoded[0], encoded[1], encoded[3], encoded[7] = parity_bits
#
#         return encoded
#
#     def decode(self, data):
#         """
#         Decode Hamming code (15,11) data.
#         :param data: Encoded data as a list of bits (e.g., [1, 0, 1, 1, 0, 0, 1])
#         :return: Original data (8 bits) as a string of bits.
#         """
#         if len(data) != self.n:
#             raise ValueError(f"Input data length must be {self.n} bits.")
#
#         # Check parity bits
#         parity_bits = [data[0], data[1], data[3], data[7]]
#         check = self._calculate_parity_bits(data)
#
#         # If parity check indicates an error, correct it
#         error_position = sum([2 ** i for i in range(self.parity_bits) if check[i] != parity_bits[i]])
#
#         if error_position > 0:
#             # Correct the error (index starts from 1, so subtract 1)
#             data[error_position - 1] ^= 1
#
#         # Decode: remove parity bits and return original data
#         return ''.join(str(data[i]) for i in range(self.n) if i not in [0, 1, 3, 7])
#
#
# # Example usage:
# hamming = Hamming()
#
# # Encode data
# input_data = "11010011"
# encoded_data = hamming.encode(input_data)
# print(f"Encoded data: {encoded_data}")
#
# # Simulate transmission with error
# encoded_data[2] ^= 1  # Simulate error in the 3rd bit (index 2)
# print(f"Data after error: {encoded_data}")
#
# # Decode data
# decoded_data = hamming.decode(encoded_data)
# print(f"Decoded data: {decoded_data}")
