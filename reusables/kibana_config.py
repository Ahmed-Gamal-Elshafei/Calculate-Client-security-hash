import json
import logging
from logstash import LogstashHandler


class JSONLogFormatter(logging.Formatter):
    """
    A custom log formatter to output logs in JSON format.
    """

    def __init__(self, datefmt="%Y-%m-%d %H:%M:%S"):
        super().__init__()
        self.datefmt = datefmt

    def format(self, record):
        log_message = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger_name": record.name,
            "message": record.getMessage(),
            "user_id": getattr(record, "user_id", None),
            "status": getattr(record, "status", None),
            "debug_level": getattr(record, "debug_level", None),
            "in_progress_delta": getattr(record, "in_progress_delta", None),
            "fail_delta": getattr(record, "fail_delta", None),
        }
        return json.dumps(log_message)


class KibanaLogging:
    """
    A utility class for configuring and using a logger that sends logs to Logstash for Kibana visualization.
    """

    @staticmethod
    def get_logger(logger_name="python_app_logger", logstash_host="localhost", logstash_udp_port=5044):
        """
        Retrieve a logger configured for Logstash with JSON formatting.

        Args:
            logger_name (str): The name of the logger.
            logstash_host (str): The hostname of the Logstash server.
            logstash_udp_port (int): The UDP port for Logstash.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger(logger_name)

        if not logger.handlers:
            # Set up basic logging configuration
            logging.basicConfig(level=logging.INFO)

            # Add Logstash handler
            logstash_handler = LogstashHandler(
                host=logstash_host,
                port=logstash_udp_port,
                version=1
            )
            # Apply JSON formatter to the Logstash handler
            json_formatter = JSONLogFormatter()
            # logstash_handler.setFormatter(json_formatter)

            logger.addHandler(logstash_handler)
            logger.propagate = False  # Prevent log propagation

        return logger

    @staticmethod
    def kibana_info_log(logger, message, user_id=None, status=None, debug_level=None, function_name=None,
                        in_progress_delta=None,
                        fail_delta=None):
        """
        Log an informational message to Kibana with structured fields in JSON format.

        Args:
            logger (logging.Logger): Logger instance.
            message (str): The log message.
            user_id (str): Optional user ID.
            status (str): Optional status information.
            debug_level (str): Optional debug level.
            function_name (str): Optional function name.
            in_progress_delta (int): Optional progress delta.
            fail_delta (int): Optional failure delta.
        """
        logger.info(message, extra={
            "user_id": user_id,
            "status": status,
            "debug_level": debug_level,
            "function_name": function_name,
            "in_progress_delta": in_progress_delta,
            "fail_delta": fail_delta,
        })

    @staticmethod
    def kibana_error_log(logger, message, user_id=None, status=None, debug_level=None, function_name=None,
                         in_progress_delta=None,
                         fail_delta=None):
        """
        Log an error message to Kibana with structured fields in JSON format.

        Args:
            logger (logging.Logger): Logger instance.
            message (str): The log message.
            user_id (str): Optional user ID.
            status (str): Optional status information.
            debug_level (str): Optional debug level.
            function_name (str): Optional function name.
            in_progress_delta (int): Optional progress delta.
            fail_delta (int): Optional failure delta.
        """
        logger.error(message, extra={
            "user_id": user_id,
            "status": status,
            "debug_level": debug_level,
            "function_name": function_name,
            "in_progress_delta": in_progress_delta,
            "fail_delta": fail_delta,
        })
