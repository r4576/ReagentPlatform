from djongo import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    objects = models.DjongoManager()

    id = models.ObjectIdField(db_column='_id', primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userName = models.TextField()
    code = models.TextField()
    history = models.TextField()

    def __str__(self):
        return self.code


class HistoryController:
    def __init__(self, userHistory):
        self.userHistory = userHistory
        self.historyList = userHistory.history.split(" ")

    def addHistory(self, newHistory):
        self.historyList.append(newHistory)

    def deleteHistory(self, oldHistory):
        if oldHistory in self.historyList:
            self.historyList.remove(oldHistory)

    def saveHistory(self):
        historyText = " ".join(self.historyList)
        self.userHistory.history = historyText
        self.userHistory.save()
