import logging 



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('app_log.log', mode='a', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - {"methodName": %(methodName)s, "timeAPI": %(elapse_time)s, "hostName": "localhost:%(port)s", "ipAddress": %(client_ip)s , "port": %(port)s", "message" : %(message)s, "data" : %(data)s}')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
