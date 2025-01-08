import galois
import numpy as np
from config import BCH_N, BCH_K, validate_bch_params

class BCH:
    def __init__(self):
        """
        Initialize a BCH code with parameters from config.py
        """
        validate_bch_params()
        self.n = BCH_N
        self.k = BCH_K
        self.bch = galois.BCH(self.n, self.k)
        self.field = self.bch.field
        
    def koduj(self, message):
        """
        Encode a message using BCH code.
        
        Args:
            message: Input message as a list of bits
            
        Returns:
            Encoded message as a list
        """
        if len(message) != self.k:
            raise ValueError(f"Message length must be {self.k} bits")
            
        # Convert message to GF array
        message_gf = self.field(message)
        # Encode the message
        encoded = self.bch.encode(message_gf)
        # Convert back to regular list
        return encoded.tolist()
        
    def dekoduj(self, received):
        """
        Decode a received message using BCH code.
        
        Args:
            received: Received message (possibly with errors)
            
        Returns:
            Decoded message as a list
        """
        if len(received) != self.n:
            raise ValueError(f"Received message length must be {self.n} bits")
            
        # Convert received message to GF array
        received_gf = self.field(received)
        # Decode with error count
        decoded, _ = self.bch.decode(received_gf, errors=True)
        # Convert back to regular list
        return decoded.tolist()
        