from django.db import models
from account.models import Account
from django.utils.timezone import now

# Create your models here.

##################### Classroom Relationship Models #####################

class ClassRoom(models.Model):
    '''
    class_name: The name of the class
    class_id: The id generated by teachers that django will check by to put students in class
    '''
    class_name = models.CharField(max_length=100, null=True, blank=True)
    #Equivalent to course_ID on canvas
    class_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.class_name

class User_To_Class(models.Model):
    '''
    user_id: If Account is deleted, then User_to_Class doesn't exist
    class_id: If ClassRoom is deleted, then User_to_Class doesn't exist
    '''
    user_id = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    #Equivalent to course_ID on canvas
    class_id = models.OneToOneField(ClassRoom, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user_id
    
##################### Curriculum Related Models #####################

class Topic(models.Model):
    '''
    topic_name: Name of the topic
    tree_image: Image field that places images in static folder
    topic_number: topic number relative to other topics
    progress_plant1: plant showing at 0-20%
    progress_plant2: plant showing at 20-40%
    progress_plant3: plant showing at 40-60%
    progress_plant4: plant showing at 60-80%
    progress_plant5: plant showing at 80-100%
    '''
    topic_name = models.CharField(max_length=100)
    tree_image = models.ImageField(null=True, blank=True)
    topic_number = models.IntegerField(null=True)
    progress_plant1 = models.ImageField(blank=True, null=True)
    progress_plant2 = models.ImageField(blank=True, null=True)
    progress_plant3 = models.ImageField(blank=True, null=True)
    progress_plant4 = models.ImageField(blank=True, null=True)
    progress_plant5 = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.topic_name

class Unit(models.Model):
    '''
    unit_id: made automically with id
    unit_name: name of unit
    number_of_lessons: meant to be an aggregrate of all of the lessons for a specific unit
    topic_id: relationship to topic, if topic is deleted, all units are deleted
    unit_icon: image field for icon
    unit_number: the number that the unit is relative to other units
    '''
    unit_name = models.CharField(max_length=100, blank=True, null=True)
    number_of_lessons = models.IntegerField(default=1)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    unit_icon = models.ImageField(blank=True, null=True)
    unit_number = models.IntegerField(null=True)

    def __str__(self):
        return self.unit_name
    
class Lesson(models.Model):
    '''
    unit_id: relationship to Unit, deletes all lessons of a unit
    lesson_id: Own key made from id
    lesson_name: name of lesson
    video_link: Uses for right now Youtube embedded links for videos
    video_script: Uses JsonField with timestamps as dict
    lesson_num: the lesson number relative to other lessons in unit
    '''
    unit_id = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    lesson_name = models.CharField(max_length=100, blank=True, null=True)
    video_link = models.TextField()
    video_script = models.JSONField(null=True, blank=True)
    lesson_num = models.IntegerField(null=True)

    def __str__(self):
        return self.lesson_name

class Quiz(models.Model):
    '''
    lesson_id: relationship to lesson, if lesson deletes, then quiz is gone
    content: quiz content in json format
    '''
    lesson_id = models.OneToOneField(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    content = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.lesson_id.lesson_name

##################### User Related Models ########################

class Lessons_Completed(models.Model):
    '''
    lesson_id: connection to Lesson to see if user completed lesson
    user_id: connection to refer back to the user
    lesson_completed: to show how many lessons are completed for that topic
    lesson_grade: the highest score that you get for a specific lesson
    attempts: the amount of attempts a user tried
    date_attempted: the most recent date that the user took the quiz
    '''
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    lesson_completed = models.BooleanField(default=False)
    lesson_grade = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)
    date_attempted = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.user_id.first_name}: {self.lesson_id.lesson_name}'

class Topic_Tree(models.Model):
    '''
    user_id: connection to user for tree naming
    tree_name: the tree name that the user wants for the topic
    topic_id: the topic that the tree name is connected to
    '''
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    tree_name = models.CharField(max_length=20, null=True, blank=True)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user_id.first_name}: {self.topic_id.topic_name}'

class Lesson_Assignment(models.Model):
    '''
    user_id: connection to user for progress of a specific assignment
    lesson_id: connection to specific lesson
    assigned: boolean field to see if lesson was assigned by teacher and shows it on student side
    date_due: date that teacher set that lesson would be due
    date_available: date that the lesson would be available for the student to see
    attempts_max: the amount of attempts that the teacher set for the student
    '''
    user_id = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    assigned = models.BooleanField(default=False)
    date_due = models.DateTimeField(default=now)
    date_available = models.DateTimeField(default=now)
    attempts_max = models.IntegerField(default=3)

    def __str__(self):
        return f'{self.user_id.first_name}: {self.lesson_id.lesson_name}'
    