class TokenCounter:
    def __init__(self):
        self.sent_tokens = 0
        self.received_tokens = 0

    def add_sent(self, token_count):
        self.sent_tokens += token_count

    def add_received(self, token_count):
        self.received_tokens += token_count

    def total_tokens(self):
        return self.sent_tokens + self.received_tokens

    def display(self):
        return_string = "Sent: " + self.sent_tokens + " Received: " + self.received_tokens
        print(f"Tokens sent to OpenAI: {self.sent_tokens}")
        print(f"Tokens received from OpenAI: {self.received_tokens}")
        print(f"Total tokens used: {self.total_tokens()}")
        return return_string