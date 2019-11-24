import random

class Student():
    def __init__(self, sanity, sleep_debt):
        self.sanity = sanity
        self.sleep_debt = sleep_debt

    def will_study(self, date_time):
        return date_time - self.next_midterm() < 4.0

    def do_work(self, work):
        self.sleep_debt += work.time_required
        if work.time_required > 5:
            self.sanity -= work.time_required - 5

    def apply_for_internship(self, application, internship):
        return internship.process(application)

    def check_sanity(self):
        if self.sleep_debt > 12:
            self.sanity += (10 - self.sleep_debt)//2
        if self.sanity < -100:
            self.panic()

    def panic(self):
        return

class Austin(Student):

    def enroll(self, course):
        if course.type == 'humanity':
            return 'Error: Schedule Conflict\tUnable to enroll in ' + course.name

    def apply_for_internship(self, application, internship):
        self.internship = internship
        return internship.accepted


class Jennifer(Student):

    def will_study(self, date_time):
        self.panic()
        return True


class Jeffery(Student):

    def wake_up(self, time):
        if time < 1300:
            return 'no'
        else:
            self.awake = True

class Larry(Student):

    def will_study(self, date_time):
        return False

    def do_work(self, work):
        if random.random() < 0.1:
            return Student.do_work(self, work)
        else:
            return 'nah'
