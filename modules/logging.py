import logging

log_level = logging.INFO
log = logging.getLogger()
if not log.handlers:
    log.setLevel(log_level)
    log_formatter = logging.Formatter(
                             fmt='%(asctime)s.%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                             datefmt='%Y-%m-%d %H:%M:%S')
    ch = logging.StreamHandler()
    ch.setFormatter(log_formatter)
    ch.setLevel(log_level)
    log.addHandler(ch)
