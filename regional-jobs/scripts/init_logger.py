#!/usr/bin/env python3
import json
import logging
import sys
import os

def setup_logger():
    logger = logging.getLogger("bucket-sync-init")
    logger.setLevel(logging.INFO)
    
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "time": self.formatTime(record),
                "level": record.levelname,
                "message": record.getMessage(),
                "component": "init",
                "hostname": os.environ.get("HOSTNAME", "unknown"),
                "pod_index": os.environ.get("POD_INDEX", "unknown"),
                "total_pods": os.environ.get("TOTAL_PODS", "unknown")
            }
            
            for key, value in record.__dict__.items():
                if key not in ['args', 'asctime', 'created', 'exc_info', 'exc_text', 
                              'filename', 'funcName', 'id', 'levelname', 'levelno',
                              'lineno', 'module', 'msecs', 'message', 'msg', 'name', 
                              'pathname', 'process', 'processName', 'relativeCreated', 
                              'stack_info', 'thread', 'threadName']:
                    log_record[key] = value
                
            return json.dumps(log_record)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    
    return logger

# Export the logger function
if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Logger module initialized")
    
    # Let Python know this module can be imported
    print("Logger ready for import")
