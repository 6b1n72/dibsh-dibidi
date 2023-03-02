#!/usr/bin/python3
import sqlite3
from datetime import datetime
from os import system


class Reading(object):
    def __init__(self):
        self.name = None
        self.studentId = None
        self.time = None
        self.wordCount = None
        self.learnedOrKnownWords = None
        self.wordPerMinute = None
        self.percentageOfLearnedWords = None
        self.readingAbility = None
        self.conDb = sqlite3.connect("student.db")
        self.cur = self.conDb.cursor()

        self.startAndGetValues()

    def getInfo(self):
        self.name = input("Name: ")
        self.studentId = input("Id: ")
        self.time = int(input("Time(minute): "))
        self.wordCount = int(input("Countered words: "))
        self.learnedOrKnownWords = int(input("knownWords: "))
        self.percentageOfLearnedWords = None
        system("cls")

    def startAndGetValues(self):
        banner = """
            ===================================================================
            |                   Welcome to idiots world.                      |
            |                                                                 |
            | 0. clear.                                                       |
            | 1. add student.                                                 |
            | 2. change values of a student(id).                              |
            | 3. delete student.                                              |
            | 4. get csv.                                                     |
            | 5. showDataBase.                                                |
            | 6. deleteTable.                                                 |
            | 7. exit.                                                        |
            ===================================================================
        """
        print(banner)
        condition = (input("  >> "))

        match condition:
            case "0":
                system("cls")
                self.startAndGetValues()

            case "1":
                self.getInfo()
                self.calculation()
                self.startAndGetValues()

            case "2":
                self.editValue(input("Id: "))
                self.startAndGetValues()

            case "3":
                self.deleteStudent(input("Id: "))

            case "4":
                self.getCsv()
                self.startAndGetValues()

            case "5":
                self.showDb()
                self.startAndGetValues()

            case "6":
                self.deleteTable()
                self.startAndGetValues()

            case "7":
                print("Bye!")

            case _:
                system("cls")
                self.startAndGetValues()

    def calculation(self):
        """
        consist of some calculation to find out our object readingAbility.
        :return:
        """
        self.wordPerMinute = (60 * self.wordCount) / (self.time * 60)
        self.percentageOfLearnedWords = (self.learnedOrKnownWords/self.wordCount)*100
        self.readingAbility = (self.wordPerMinute * self.percentageOfLearnedWords) / 100
        self.createTable()

    def createTable(self):
        """
        connect to db and create table of contents.
        :return:
        """
        try:
            self.cur.execute("CREATE TABLE students (name varchar(20), studentId varchar(12),time INT, wordCount INT, readAbility FLOAT, date time)")
        except sqlite3.OperationalError as error:
            self.pushToDb()

    def pushToDb(self):
        """
        pushing the data of objects to our simple small table.
        :return:
        """
        params = (self.name, self.studentId, self.time, self.wordCount, self.readingAbility, datetime.now())
        self.cur.execute("INSERT INTO students VALUES(?, ?, ?, ?, ?, ?)", params)
        self.conDb.commit()

    def editValue(self, id):
        self.getInfo()
        self.cur.execute(f"UPDATE students SET name={self.name}, studentId={self.studentId}, time={self.time}, wordCount={self.wordCount}, readAbility={self.readingAbility} WHERE studentId={id}")

    def deleteStudent(self, id):
        self.cur.execute(f"DELETE FROM students WHERE studentId={id}")

    def deleteTable(self):
        self.cur.execute("DROP TABLE students")

    def getCsv(self):
        with open("bbkhti.csv", "w") as csvfile:
            for row in self.cur.execute("SELECT * FROM students"):
                csvfile.write(f"{row[0]}/{row[1]},{row[2]},{row[3]},{row[4]},{row[5]}\n")
            csvfile.close()


    def showDb(self):
        for row in self.cur.execute("SELECT * FROM students"):
            print(f"name: {row[0]}/{row[1]}\ntime: {row[2]}\ncounteredWords: {row[3]}\nreadingAbility: {row[4]}\ndate: {row[5]}")
            print("\n______________________________________________________\n")


if __name__ == "__main__":
    student = Reading()
    student.cur.close()
    print("\n\nsuccessful!")
