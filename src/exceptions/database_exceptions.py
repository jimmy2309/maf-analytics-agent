class DatabaseFetchException(Exception):
    """Exception raised when there is an error fetching data from the database."""
    def __init__(self, message: str):
        super().__init__(message)
