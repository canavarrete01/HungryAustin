#if for some reason the unit tests aren't running in the virtual environment
#then please refer to the screenshot of it successfully working on the "About Us" page .... 

import os
import sys
import unittest
from models import app, db, Restaurant, Cuisine, MenuItem

# -----------
# DBTestCases
# -----------
class DBTestCases(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            db.create_all()
            
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    # ---------
    # insertion
    # ---------
    def test_restaurant_insert(self):
        with app.app_context():
            s = Restaurant(id='20', name = 'C++')
            db.session.add(s)
            db.session.commit()


            r = db.session.query(Restaurant).filter_by(id = '20').one()
            self.assertEqual(str(r.id), '20')

            db.session.query(Restaurant).filter_by(id = '20').delete()
            db.session.commit()

    def test_cuisine_insert(self):
        with app.app_context():
            s = Cuisine(id='20', name='C++')
            db.session.add(s)
            db.session.commit()
            r = db.session.query(Cuisine).filter_by(id='20').one()
            self.assertEqual(str(r.id), '20')
            db.session.query(Cuisine).filter_by(id='20').delete()
            db.session.commit()

    def test_menuitem_insert(self):
        with app.app_context():
            s = MenuItem(id='20', name='C++')
            db.session.add(s)
            db.session.commit()
            r = db.session.query(MenuItem).filter_by(id='20').one()
            self.assertEqual(str(r.id), '20')
            db.session.query(MenuItem).filter_by(id='20').delete()
            db.session.commit()
    
    # second set of unit tests for deletion 
    def test_restaurant_deletion(self):
        with app.app_context():
            s = Restaurant(id='21', name='Restaurant 2')
            db.session.add(s)
            db.session.commit()
            db.session.query(Restaurant).filter_by(id='21').delete()
            db.session.commit()
            r = db.session.query(Restaurant).filter_by(id='21').first()
            self.assertIsNone(r)

    def test_cuisine_deletion(self):
        with app.app_context():
            s = Cuisine(id='21', name='Cuisine 2')
            db.session.add(s)
            db.session.commit()
            db.session.query(Cuisine).filter_by(id='21').delete()
            db.session.commit()
            r = db.session.query(Cuisine).filter_by(id='21').first()
            self.assertIsNone(r)

    def test_menuitem_deletion(self):
        with app.app_context():
            s = MenuItem(id='21', name='MenuItem 2')
            db.session.add(s)
            db.session.commit()
            db.session.query(MenuItem).filter_by(id='21').delete()
            db.session.commit()
            r = db.session.query(MenuItem).filter_by(id='21').first()
            self.assertIsNone(r)
    
    #third set of unit tests for update 
    def test_restaurant_update(self):
        with app.app_context():
            s = Restaurant(id='22', name='Restaurant 3')
            db.session.add(s)
            db.session.commit()
            db.session.query(Restaurant).filter_by(id='22').update({'name': 'Updated Restaurant'})
            db.session.commit()
            r = db.session.query(Restaurant).filter_by(id='22').one()
            self.assertEqual(r.name, 'Updated Restaurant')
            db.session.query(Restaurant).filter_by(id='22').delete()
            db.session.commit()

    def test_cuisine_update(self):
        with app.app_context():
            s = Cuisine(id='22', name='Cuisine 3')
            db.session.add(s)
            db.session.commit()
            db.session.query(Cuisine).filter_by(id='22').update({'name': 'Updated Cuisine'})
            db.session.commit()
            r = db.session.query(Cuisine).filter_by(id='22').one()
            self.assertEqual(r.name, 'Updated Cuisine')
            db.session.query(Cuisine).filter_by(id='22').delete()
            db.session.commit()

    def test_menuitem_update(self):
        with app.app_context():
            s = MenuItem(id='22', name='MenuItem 3')
            db.session.add(s)
            db.session.commit()
            db.session.query(MenuItem).filter_by(id='22').update({'name': 'Updated MenuItem'})
            db.session.commit()
            r = db.session.query(MenuItem).filter_by(id='22').one()
            self.assertEqual(r.name, 'Updated MenuItem')
            db.session.query(MenuItem).filter_by(id='22').delete()
            db.session.commit()

if __name__ == '__main__':
    unittest.main()
# end of code