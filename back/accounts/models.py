from djongo import models


class UserHistory(models.Model):
    objects = models.DjongoManager()

    id = models.ObjectIdField(db_column='_id', primary_key=True)
    email = models.EmailField()
    history = models.TextField()


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
