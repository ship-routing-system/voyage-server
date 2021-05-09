

def timer(logger_name):
    import logging
    logger = logging.getLogger(logger_name)
    def decorator(func):
        import time
        def wrapper(*args):
            nonlocal logger, func
            start = time.time()
            result = func(*args)
            end = time.time()
            logger.info("%s 함수가 실행하는 데, %s 시간이 소요되고 있습니다", func.__name__, f"{end-start:.4f}")
            return result
        return wrapper
    return decorator