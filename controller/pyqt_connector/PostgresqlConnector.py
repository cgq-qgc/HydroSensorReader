import sqlalchemy.exc
from PyQt4 import QtCore

from database.class_SQLAlchemy_Connecteur import AdapteurBD
from pattern.observer_pattern.Observable import Observable, Notification
from pattern.observer_pattern.MessageType import Message

LOCALHOST = 'localhost:5432'
RNCAN_SERVER = 's-stf-ngwd.nrn.nrcan.gc.ca'

class PLSQL_pyqt_thread(Observable, QtCore.QThread):
	def __init__(self):

		QtCore.QThread.__init__(self)
		Observable.__init__(self)

		self._nombreEssai = 0
		self.utilisateur = None
		self.password = None
		self.serveur = ""
		self.connectionTentative = 0
		self.BD = None

	def setUser(self, utilisateur, password):
		print("setUser")
		self.utilisateur = utilisateur
		self.password = password
	def message_sender(self,message):
		return message

	def _connectAttempt(self):
		try:

			self.notifyObserver(
				Notification("Essai de connexion au serveur " + self.serveur,
				             Message.BD_CONNECTION_MESSAGE))
			message = self.message_sender("Essai de connexion au serveur " + self.serveur)
			self.BD = AdapteurBD('hydrogeo_terrain', self.utilisateur, self.password,
			                     self.serveur)
			return True
		except Exception as e:
			raise e

	def connectToNRCanServer(self):
		self.serveur = RNCAN_SERVER
		print("connectToNRCanServer")
		self._connectAttempt()

	def connectToLocalServer(self):
		self.serveur = LOCALHOST
		print("connectToLocalServer")
		self._connectAttempt()

	def run(self):

		"""
			Permet de se connecter à la BD avec les champs remplis
			- Change le btn_connexion pour dire - CHANGER UTILISATEUR -
			- Autorise l'entrées des différents GroupBox
			- Affiche un champ de bienvenue
			:return:
			:rtype:
			"""
		print("QThread running")
		self.notifyObserver(Notification("Début d'essai de connexion", Message.BD_CONNECTION_STARTED))
		try:
			if self.utilisateur == '' and self.password == '':
				raise Exception('Aucune information entrée')
			# Teste de la connexion
			# try:
			# 	self.connectToNRCanServer()
			# except:
			# 	pass

			if (self.BD == None):
				self.connectToLocalServer()
			if (self.BD == None):
				raise Exception

			self.notifyObserver(Notification("Connection au serveur {} réussi".format(self.serveur),
			                                 Message.BD_CONNECTION_MESSAGE))
			self.notifyObserver(Notification(self.serveur, Message.BD_CONNECTION_OK))

		except sqlalchemy.exc.OperationalError as e:
			print(str(e))
			if ("FATAL:  password authentication failed for user" in str(e)):
				self.notifyObserver(Notification(str(e), Message.BD_BAD_PASSWORD))
			else:
				# self.connectToLocalServer()
				self.notifyObserver(Notification(str(e), Message.BD_BAD_USER))

		except Exception as e:
			if 'FATAL: authentification par mot de passe' in str(e):
				self.notifyObserver(Notification("Mauvais identifiants de connexion", Message.BD_BAD_USER))
			else:
				self.notifyObserver(Notification(str(e), Message.BD_CONNECTION_FAILED))

		finally:
			try:
				self.BD.closeConnexion()
			except:
				pass
			self.deleteLater()
