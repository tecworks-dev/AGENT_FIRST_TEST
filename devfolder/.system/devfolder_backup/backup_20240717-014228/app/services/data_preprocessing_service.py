
# Purpose: Handles data preprocessing for AI models.
# Description: This service provides methods for cleaning text, tokenizing, and encoding data for use in AI models.

from typing import List
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
import traceback

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class DataPreprocessingService:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text: str) -> str:
        """
        Clean the input text by removing special characters, converting to lowercase,
        and removing extra whitespace.

        Args:
            text (str): The input text to be cleaned.

        Returns:
            str: The cleaned text.
        """
        try:
            # Convert to lowercase
            text = text.lower()
            # Remove special characters and digits
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        except Exception as e:
            print(f"Error in clean_text: {str(e)}")
            traceback.print_exc()
            return text

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize the input text into a list of words, removing stop words.

        Args:
            text (str): The input text to be tokenized.

        Returns:
            List[str]: A list of tokenized words.
        """
        try:
            # Tokenize the text
            tokens = word_tokenize(text)
            # Remove stop words
            tokens = [token for token in tokens if token not in self.stop_words]
            return tokens
        except Exception as e:
            print(f"Error in tokenize: {str(e)}")
            traceback.print_exc()
            return []

    def encode_data(self, data: List[str]) -> List[List[int]]:
        """
        Encode a list of strings into a list of integer lists using a simple
        vocabulary-based encoding.

        Args:
            data (List[str]): A list of strings to be encoded.

        Returns:
            List[List[int]]: A list of lists of integers representing the encoded data.
        """
        try:
            # Create a vocabulary from all unique words in the data
            vocabulary = sorted(set(word for text in data for word in self.tokenize(text)))
            word_to_index = {word: index for index, word in enumerate(vocabulary)}

            encoded_data = []
            for text in data:
                tokens = self.tokenize(text)
                encoded_text = [word_to_index.get(word, len(vocabulary)) for word in tokens]
                encoded_data.append(encoded_text)

            return encoded_data
        except Exception as e:
            print(f"Error in encode_data: {str(e)}")
            traceback.print_exc()
            return []

    def debug_info(self, method_name: str, input_data: Any, output_data: Any) -> None:
        """
        Print debug information for a method if DEBUG is True.

        Args:
            method_name (str): The name of the method being debugged.
            input_data (Any): The input data to the method.
            output_data (Any): The output data from the method.
        """
        if DEBUG:
            print(f"Debug info for {method_name}:")
            print(f"Input: {input_data}")
            print(f"Output: {output_data}")
            print("-" * 50)

# Set DEBUG to True for debugging statements
DEBUG = True

# Example usage
if __name__ == "__main__":
    preprocessor = DataPreprocessingService()

    # Test clean_text
    text = "This is a SAMPLE text with 123 numbers and $pecial characters!"
    cleaned_text = preprocessor.clean_text(text)
    preprocessor.debug_info("clean_text", text, cleaned_text)

    # Test tokenize
    tokenized_text = preprocessor.tokenize(cleaned_text)
    preprocessor.debug_info("tokenize", cleaned_text, tokenized_text)

    # Test encode_data
    sample_data = [
        "This is the first example.",
        "Here's another example with different words.",
        "And a third example to encode."
    ]
    encoded_data = preprocessor.encode_data(sample_data)
    preprocessor.debug_info("encode_data", sample_data, encoded_data)
