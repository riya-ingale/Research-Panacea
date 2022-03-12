from django.db import models


# Create your models here.

class Conference(models.Model):
    name = models.CharField(max_length=500)
    date = models.IntegerField()
    month = models.CharField(max_length=10)
    year = models.CharField(max_length=10)
    info = models.TextField(null=True)
    website = models.CharField(max_length=500)
    address = models.CharField(max_length=1000)
    image = models.CharField(max_length=500, null=True)
    saves = models.IntegerField(default=0)
    timedate = models.DateField(null=True)

class Users(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, null=True)
    contactno = models.IntegerField(null=True)
    user_type = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=100, null=True)
    profession = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    skills = models.CharField(max_length=500,null=True)
    description = models.CharField(max_length=200, null=True)
    languages = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(upload_to = 'users_media/pictures', null = True)
    scholar = models.CharField(max_length=500, null=True)
    orchid = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at  = models.DateTimeField(null=True)


class ResearchPapers(models.Model):
    title = models.CharField(max_length=500)
    abstract = models.TextField()
    collab_ids = models.CharField(max_length=500, null=True)
    conference_name = models.CharField(max_length=200,null=True)
    journal_name = models.CharField(max_length=200,null=True)
    domain = models.CharField(max_length=200, null=True)
    keywords = models.TextField(null=True)
    doi = models.CharField(max_length=300,null=True)
    media = models.FileField(upload_to = 'users_media/research_papers',null=True)
    published_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Saved(models.Model):
    user_id = models.IntegerField(null=True)
    conference_id = models.IntegerField(null=True)

class Threads(models.Model):
    user_id = models.IntegerField(null=True) #pk of user
    research_id = models.IntegerField(null=True) #pk of research ppr
    reply_id = models.IntegerField()
    content = models.TextField()
    upvotes = models.IntegerField()
    media = models.FileField(upload_to = 'users_media/thread_media',max_length=200,null = True)
    is_viewed = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)

class WorkExp(models.Model):
    user_id = models.IntegerField(null=True)
    organization = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=200,null=True)
    location = models.CharField(max_length=200,null=True)
    media = models.FileField(upload_to = 'users_media/workexp',null=True)
    description = models.TextField(null=True)
    ongoing = models.BinaryField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

class Education(models.Model):
    user_id = models.IntegerField(null=True)
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    grade = models.CharField(max_length=200,null=True)
    description = models.TextField(null=True)
    media = models.FileField(upload_to = 'users_media/education',null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

class Certification(models.Model):
    user_id = models.IntegerField(null=True)
    course_name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    link = models.TextField(null=True)
    credential_id = models.CharField(max_length=200,null=True)
    completition_date = models.DateTimeField()

class Events(models.Model):
    organizer = models.IntegerField()
    dates = models.DateTimeField()
    address = models.TextField(null=True)
    event_name = models.CharField(max_length=200)
    media = models.ImageField('events/media',null=True)
    media_1 = models.ImageField('events/media1',null=True)
    media_2 = models.ImageField('events/media2',null=True)
    media_3 = models.ImageField('events/media3',null=True)
    media_4 = models.ImageField('events/media4',null=True)
    pdf = models.FileField('events/pdf',null=True)
    save = models.IntegerField(default=0)
    verify = models.BinaryField(null=True)
    speaker = models.CharField(max_length = 200, null=True)
    domain = models.TextField(null=True)
    website = models.TextField(null=True)

class UserEvent(models.Model):
    user_id = models.IntegerField(null=True)
    event_id = models.IntegerField(null=True)

# Research Papers saved by users
class UserResearch(models.Model):
    user_id = models.IntegerField(null=True)
    research_id = models.IntegerField(null=True)

# User_id has saved Research Paper of id = research_id
class SavedResearchPapers(models.Model):
    user_id = models.IntegerField(null=True)
    research_id = models.IntegerField(null=True)

    