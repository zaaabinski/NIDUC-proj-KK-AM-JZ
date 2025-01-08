# Global BCH parameters
BCH_N = 15  # Codeword length
BCH_K = 5  # Message length

# Function to validate BCH parameters
def validate_bch_params():
    """
    Validate that the BCH parameters are valid.
    Raises ValueError if parameters are invalid.
    """
    if BCH_N <= 0 or BCH_K <= 0:
        raise ValueError("BCH parameters must be positive integers")
    if BCH_K >= BCH_N:
        raise ValueError("Message length (k) must be less than codeword length (n)")
    if not (BCH_N - 1).bit_length() <= 8:  # Max field size GF(2^m) where m <= 8
        raise ValueError("Codeword length (n) too large for implementation") 