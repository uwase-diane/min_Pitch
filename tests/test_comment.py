import unittest
from app.models import Comment, Pitch
from app import db

class TestPitchComment(unittest.TestCase):

    def setUp(self):
        self.new_pitch = Pitch(post = "doit", category='Quotes')
        self.new_comment = Comment(comment = "good comment", pitch=self.new_pitch)
        
    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))


    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment,"good comment")
        self.assertEquals(self.new_comment.pitch,self.new_pitch, 'do it')