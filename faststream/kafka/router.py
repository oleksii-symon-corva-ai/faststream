from typing import Any, Dict, Optional

from faststream._compat import override
from faststream.kafka.asyncapi import Publisher
from faststream.kafka.shared.router import KafkaRouter as BaseRouter


class KafkaRouter(BaseRouter):
    """A class to represent a Kafka router.

    Attributes:
        _publishers : Dictionary of publishers

    Methods:
        _get_publisher_key : Get the key for a publisher
        _update_publisher_prefix : Update the prefix of a publisher
        publisher : Create a new publisher

    """

    _publishers: Dict[str, Publisher]  # type: ignore[assignment]

    @override
    @staticmethod
    def _get_publisher_key(publisher: Publisher) -> str:  # type: ignore[override]
        """Get the publisher key.

        Args:
            publisher: The publisher object.

        Returns:
            The publisher key.

        """
        return publisher.topic

    @override
    @staticmethod
    def _update_publisher_prefix(  # type: ignore[override]
        prefix: str,
        publisher: Publisher,
    ) -> Publisher:
        """Updates the prefix of a publisher.

        Args:
            prefix: The prefix to be added to the publisher's topic.
            publisher: The publisher object to be updated.

        Returns:
            The updated publisher object.

        """
        publisher.topic = prefix + publisher.topic
        return publisher

    @override
    def publisher(  # type: ignore[override]
        self,
        topic: str,
        key: Optional[bytes] = None,
        partition: Optional[int] = None,
        timestamp_ms: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        reply_to: str = "",
        batch: bool = False,
        # AsyncAPI information
        title: Optional[str] = None,
        description: Optional[str] = None,
        schema: Optional[Any] = None,
        include_in_schema: bool = True,
    ) -> Publisher:
        """Publishes a message to a topic.

        Args:
            topic (str): The topic to publish the message to.
            key (bytes, optional): The key associated with the message.
            partition (int, optional): The partition to publish the message to.
            timestamp_ms (int, optional): The timestamp of the message in milliseconds.
            headers (Dict[str, str], optional): Additional headers for the message.
            reply_to (str, optional): The topic to reply to.
            batch (bool, optional): Whether to publish the message as part of a batch.
            title (str, optional): The title of the message.
            description (str, optional): The description of the message.

        Returns:
            Publisher: The publisher object used to publish the message.

        """
        new_publisher = self._update_publisher_prefix(
            self.prefix,
            Publisher(
                topic=topic,
                key=key,
                partition=partition,
                timestamp_ms=timestamp_ms,
                headers=headers,
                reply_to=reply_to,
                title=title,
                batch=batch,
                _description=description,
                _schema=schema,
                include_in_schema=(
                    include_in_schema
                    if self.include_in_schema is None
                    else self.include_in_schema
                ),
            ),
        )
        publisher_key = self._get_publisher_key(new_publisher)
        publisher = self._publishers[publisher_key] = self._publishers.get(
            publisher_key, new_publisher
        )
        return publisher
