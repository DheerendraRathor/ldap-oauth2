import logging


class SuppressDeprecatedWarnings(logging.Filter):
    """
    Suppress deprecated warnings defined in WARNINGS_TO_SUPPRESS
    """
    WARNINGS_TO_SUPPRESS = [
        'RemovedInDjango19Warning'
    ]

    def filter(self, record):
        return not any([warn in record.getMessage() for warn in self.WARNINGS_TO_SUPPRESS])
