import py_eureka_client.eureka_client as eureka_client

def eurekaConfig(PORT,service_name):
    your_rest_server_port = 8761
    # The flowing code will register your server to eureka server and also start to send heartbeat every 30 seconds
    eureka_client.init(eureka_server="http://eureka-server:8761",
    app_name=service_name,
    instance_port=PORT)