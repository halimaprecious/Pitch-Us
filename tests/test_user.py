import unittest
from app.models import User,Comment, Pitch
from app import db

class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User(password = 'mamamia')
    def test_password_setter(self):
        self.assertTrue(self.new_user.password_hash is not None)
    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password
    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('mamamia'))

class CommentModelTest(unittest.TestCase):
    def setUp(self):
       self.new_comment = Comment(id=1, user_id = 3, comment = 'bueno',pitch_id = '10',date_posted='2022-05-08')
    def test_comment_variables(self):
       self.assertEquals(self.new_comment.comment,'bueno')
       self.assertEquals(self.new_comment.date_posted,'2022-05-05')
       self.assertEquals(self.new_comment.user_id, 3)
    def test_save_comment(self):
        self.assertTrue(len(Comment.query.all())>0)
        
class PitchModelTest(unittest.TestCase):
    def test_save_pitch(self):
        self.assertTrue(len(Pitch.query.all())>0)