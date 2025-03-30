class UserWithAddressNotFoundError(Exception):
    """Exception raised when a user is not found by address."""

    def __init__(self, address: str):
        self.address = address
        super().__init__(f"User with address {address} not found.")


class UserWithUsernameNotFoundError(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User with username {username} not found.")


class PostNotFoundError(Exception):
    """Exception raised when a post is not found."""

    def __init__(self, post_id: str):
        self.post_id = post_id
        super().__init__(f"Post with ID {post_id} not found.")


class TipNotFoundError(Exception):
    """Exception raised when a tip is not found."""

    def __init__(self, tip_id: int):
        self.tip_id = tip_id
        super().__init__(f"Tip with ID {tip_id} not found.")
