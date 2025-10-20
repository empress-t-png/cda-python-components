#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
# 

import logging
import paho.mqtt.client as mqttClient

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient

class MqttClientConnector(IPubSubClient):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, clientID: str = None):
		"""
		Default constructor. This will set remote broker information and client connection
		information based on the default configuration file contents.
		
		@param clientID Defaults to None. Can be set by caller. If this is used, it's
		critically important that a unique, non-conflicting name be used so to avoid
		causing the MQTT broker to disconnect any client using the same name. With
		auto-reconnect enabled, this can cause a race condition where each client with
		the same clientID continuously attempts to re-connect, causing the broker to
		disconnect the previous instance.
		"""
		self.config = ConfigUtil()
		self.dataMsgListener = None
		
		self.host = self.config.getProperty(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
		self.port = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_MQTT_PORT)
		self.keepAlive = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		self.defaultQos = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.DEFAULT_QOS_KEY, ConfigConst.DEFAULT_QOS)
		
		if not clientID:
			self.clientID = ConfigConst.CONSTRAINED_DEVICE
		else:
			self.clientID = clientID
		
		logging.info('	MQTT Client ID:   ' + self.clientID)
		logging.info('	MQTT Broker Host: ' + self.host)
		logging.info('	MQTT Broker Port: ' + str(self.port))
		logging.info('	MQTT Keep Alive:  ' + str(self.keepAlive))
		
		self.mqttClient = mqttClient.Client(client_id=self.clientID, clean_session=True)
		self.mqttClient.on_connect = self.onConnect
		self.mqttClient.on_disconnect = self.onDisconnect
		self.mqttClient.on_message = self.onMessage
		self.mqttClient.on_publish = self.onPublish
		self.mqttClient.on_subscribe = self.onSubscribe

	def connectClient(self) -> bool:
		if not self.mqttClient:
			logging.warning("MQTT client not yet initialized.")
			return False
		
		try:
			logging.info("Connecting to MQTT broker at host: " + self.host + " port: " + str(self.port))
			self.mqttClient.connect(self.host, self.port, self.keepAlive)
			self.mqttClient.loop_start()
			return True
		except Exception as e:
			logging.error("Failed to connect to MQTT broker: " + str(e))
			return False
		
	def disconnectClient(self) -> bool:
		if not self.mqttClient:
			logging.warning("MQTT client not yet initialized.")
			return False
		
		try:
			logging.info("Disconnecting from MQTT broker: " + self.host)
			self.mqttClient.loop_stop()
			self.mqttClient.disconnect()
			return True
		except Exception as e:
			logging.error("Failed to disconnect from MQTT broker: " + str(e))
			return False
		
	def onConnect(self, client, userdata, flags, rc):
		logging.info("[Callback] Connected to MQTT broker. Result code: " + str(rc))
		
	def onDisconnect(self, client, userdata, rc):
		logging.info("[Callback] Disconnected from MQTT broker. Result code: " + str(rc))
		
	def onMessage(self, client, userdata, msg):
		logging.info("[Callback] Message received on topic: " + msg.topic)
		
		if self.dataMsgListener:
			try:
				self.dataMsgListener.handleIncomingMessage(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, msg.payload.decode('utf-8'))
			except Exception as e:
				logging.error("Failed to handle incoming message: " + str(e))
			
	def onPublish(self, client, userdata, mid):
		logging.debug("[Callback] Message published. Message ID: " + str(mid))
	
	def onSubscribe(self, client, userdata, mid, granted_qos):
		logging.info("[Callback] Subscribed to topic. Message ID: " + str(mid) + " QoS: " + str(granted_qos))
	
	def onActuatorCommandMessage(self, client, userdata, msg):
		"""
		This callback is defined as a convenience, but does not
		need to be used and can be ignored.
		
		It's simply an example for how you can create your own
		custom callback for incoming messages from a specific
		topic subscription (such as for actuator commands).
		
		@param client The client reference context.
		@param userdata The user reference context.
		@param msg The message context, including the embedded payload.
		"""
		logging.info("[Callback] Actuator command message received on topic: " + msg.topic)
		
		if self.dataMsgListener:
			try:
				self.dataMsgListener.handleIncomingMessage(ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, msg.payload.decode('utf-8'))
			except Exception as e:
				logging.error("Failed to handle actuator command message: " + str(e))
	
	def publishMessage(self, resource: ResourceNameEnum = None, msg: str = None, qos: int = ConfigConst.DEFAULT_QOS):
		if not self.mqttClient:
			logging.warning("MQTT client not yet initialized.")
			return False
		
		if not resource:
			logging.warning("Resource is None. Unable to publish message.")
			return False
		
		if qos < 0 or qos > 2:
			qos = ConfigConst.DEFAULT_QOS
		
		topic = resource.value
		
		try:
			logging.info("Publishing message to topic: " + topic)
			msgInfo = self.mqttClient.publish(topic, msg, qos)
			msgInfo.wait_for_publish()
			return True
		except Exception as e:
			logging.error("Failed to publish message: " + str(e))
			return False
	
	def subscribeToTopic(self, resource: ResourceNameEnum = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS):
		if not self.mqttClient:
			logging.warning("MQTT client not yet initialized.")
			return False
		
		if not resource:
			logging.warning("Resource is None. Unable to subscribe to topic.")
			return False
		
		if qos < 0 or qos > 2:
			qos = ConfigConst.DEFAULT_QOS
		
		topic = resource.value
		
		try:
			logging.info("Subscribing to topic: " + topic)
			
			if callback:
				self.mqttClient.message_callback_add(topic, callback)
			
			self.mqttClient.subscribe(topic, qos)
			return True
		except Exception as e:
			logging.error("Failed to subscribe to topic: " + str(e))
			return False
	
	def unsubscribeFromTopic(self, resource: ResourceNameEnum = None):
		if not self.mqttClient:
			logging.warning("MQTT client not yet initialized.")
			return False
		
		if not resource:
			logging.warning("Resource is None. Unable to unsubscribe from topic.")
			return False
		
		topic = resource.value
		
		try:
			logging.info("Unsubscribing from topic: " + topic)
			self.mqttClient.unsubscribe(topic)
			return True
		except Exception as e:
			logging.error("Failed to unsubscribe from topic: " + str(e))
			return False

	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		if listener:
			self.dataMsgListener = listener
			return True
		return False
