#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
import traceback

# Import the logger module
sys.path.append('/scripts')
from init_logger import setup_logger

logger = setup_logger()

def main():
    logger.info("Queue initializer starting")
    
    queue_dir = Path('/queue')
    queue_dir.mkdir(exist_ok=True)
    
    # Get environment variables
    pod_index = int(os.environ.get("POD_INDEX", "0"))
    total_pods = int(os.environ.get("TOTAL_PODS", "1"))
    
    logger.info(f"Pod index: {pod_index}, Total pods: {total_pods}")

    # Load bucket pairs from config
    config_path = Path('/etc/bucket-config/bucket-pairs.json')
    try:
        with open(config_path) as f:
            bucket_pairs = json.load(f)
            
        logger.info(f"Loaded {len(bucket_pairs)} bucket pairs from config")
        
        # Divide bucket pairs among pods
        pod_pairs = []
        for i, pair in enumerate(bucket_pairs):
            if i % total_pods == pod_index:
                pod_pairs.append(pair)
                
        logger.info(f"This pod will process {len(pod_pairs)} bucket pairs")
        
        # Create work items
        for i, pair in enumerate(pod_pairs):
            item_path = queue_dir / f"item_{i}.json"
            with open(item_path, 'w') as f:
                json.dump(pair, f)
            logger.info(f"Created work item: {item_path.name}", extra={
                "source_bucket": pair.get("sourceBucket", "unknown"),
                "dest_bucket": pair.get("destBucket", "unknown")
            })
            
        logger.info("Queue initialization complete")
        
    except Exception as e:
        logger.error(f"Error initializing queue: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
