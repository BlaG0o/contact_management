from main import application, create_random_contact
from routes import *
from random import choice,sample
from string import printable, ascii_uppercase
from urllib.parse import quote
import unittest

class FlaskTestCase(unittest.TestCase):
    #Test missing paths status code
    def test_missing_paths_status(self):
        tester = application.test_client(self)
        random_path = ''.join(choice(printable) for i in range(choice(range(100))))
        print(f'Testing missing path: /{random_path}')
        response = tester.get(quote(f'/{random_path}'))
        self.assertTrue(response.status_code == 200)
        
    #Test missing paths content data
    def test_missing_paths_content(self):
        tester = application.test_client(self)
        random_path = ''.join(choice(printable) for i in range(choice(range(100))))
        print(f'Testing missing path: /{random_path}')
        response = tester.get(quote(f'/{random_path}'))
        self.assertIn(b'"message":"No such path!"',response.data)
        
        
    #Test index status code
    def test_index_status(self):
        print('Testing status for path: /')
        tester = application.test_client(self)
        response = tester.get("/")
        self.assertTrue(response.status_code == 200)
    
    #Test index content type
    def test_index_content(self):
        print('Testing content type for path: /')
        tester = application.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.content_type,"application/json")
        
    #Test index with POST
    def test_index_post(self):
        print('Testing POST request for path: /')
        tester = application.test_client(self)
        response = tester.post("/")
        self.assertEqual(response.status_code,405)
        
    #Test index with PATCH
    def test_index_patch(self):
        print('Testing PATCH request for path: /')
        tester = application.test_client(self)
        response = tester.patch("/")
        self.assertEqual(response.status_code,405)
        
    #Test index with DELETE
    def test_index_delete(self):
        print('Testing DELETE request for path: /')
        tester = application.test_client(self)
        response = tester.delete("/")
        self.assertEqual(response.status_code,405)
        
    #Test search status code
    def test_search_status(self):
        print('Testing status for path: /search/<username>')
        tester = application.test_client(self)
        random_username = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        response = tester.get(f"/search/{random_username}")
        self.assertTrue(response.status_code == 200)
        
    #Test index with POST
    def test_search_post(self):
        print('Testing POST request at path: /search/<username>')
        tester = application.test_client(self)
        random_username = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        response = tester.post(f"/search/{random_username}")
        self.assertEqual(response.status_code,405)
        
    #Test index with PATCH
    def test_search_patch(self):
        print('Testing PATCH request at path: /search/<username>')
        tester = application.test_client(self)
        random_username = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        response = tester.patch(f"/search/{random_username}")
        self.assertEqual(response.status_code,405)
        
    #Test index with DELETE
    def test_search_delete(self):
        print('Testing DELETE request at path: /search/<username>')
        tester = application.test_client(self)
        random_username = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        response = tester.delete(f"/search/{random_username}")
        self.assertEqual(response.status_code,405)
        
    #Test search content type
    def test_search_status(self):
        print('Testing content type for path: /search/<username>')
        tester = application.test_client(self)
        random_username = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        response = tester.get(f"/search/{random_username}")
        self.assertEqual(response.content_type,"application/json")
        
    #Test search for known username
    def test_search_known(self):
        print('Testing content for path: /search/blag0')
        tester = application.test_client(self)
        response = tester.get("/search/blag0", content_type="application/json")
        self.assertIn(b'"first_name":"Blagoy"',response.data)
        
    #Test search for unknown username
    def test_search_unknown(self):
        print('Testing content for path: /search/POR')
        tester = application.test_client(self)
        response = tester.get("/search/POR", content_type="application/json")
        self.assertIn(b'"message":"No record found!"',response.data)
        
    #Test create status code
    def test_create_status(self):
        print('Testing status for path: /create/<username>/<first_name>/<last_name>/<email>')
        tester = application.test_client(self)
        username = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        first_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        last_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        email = ''.join(choice(ascii_uppercase) for i in range(23)) + "@gmail.com"
        response = tester.post(f'/create/{username}/{first_name}/{last_name}/{email}')
        self.assertEqual(response.status_code,200)
        
    #Test create GET
    def test_create_get(self):
        print('Testing GET request at path: /create/<username>/<first_name>/<last_name>/<email>')
        tester = application.test_client(self)
        username = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        first_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        last_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        email = ''.join(choice(ascii_uppercase) for i in range(23)) + "@gmail.com"
        response = tester.get(f'/create/{username}/{first_name}/{last_name}/{email}')
        self.assertEqual(response.status_code,405)
        
    #Test create PATCH
    def test_create_patch(self):
        print('Testing PATCH request at path: /create/<username>/<first_name>/<last_name>/<email>')
        tester = application.test_client(self)
        username = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        first_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        last_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        email = ''.join(choice(ascii_uppercase) for i in range(23)) + "@gmail.com"
        response = tester.patch(f'/create/{username}/{first_name}/{last_name}/{email}')
        self.assertEqual(response.status_code,405)
        
    #Test create DELETE
    def test_create_delete(self):
        print('Testing DELETE request at path: /create/<username>/<first_name>/<last_name>/<email>')
        tester = application.test_client(self)
        username = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        first_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        last_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        email = ''.join(choice(ascii_uppercase) for i in range(23)) + "@gmail.com"
        response = tester.delete(f'/create/{username}/{first_name}/{last_name}/{email}')
        self.assertEqual(response.status_code,405)
        
    #Test create content type
    def test_create_content_type(self):
        print('Testing status for path: /create/<username>/<first_name>/<last_name>/<email>')
        tester = application.test_client(self)
        username = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        first_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        last_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        email = ''.join(choice(ascii_uppercase) for i in range(23)) + "@gmail.com"
        response = tester.post(f'/create/{username}/{first_name}/{last_name}/{email}')
        self.assertEqual(response.content_type,"application/json")
    
    #Test create content    
    def test_create_content(self):
        print('Testing status for path: /create/<username>/<first_name>/<last_name>/<email>')
        tester = application.test_client(self)
        username = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        first_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        last_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        email = ''.join(choice(ascii_uppercase) for i in range(23)) + "@gmail.com"
        response = tester.post(f'/create/{username}/{first_name}/{last_name}/{email}')
        self.assertTrue(bytes(f'"username":"{username}"', "utf-8") in response.data)
        
    #Test create with missing parts
    def test_create_missing_parts(self):
        print('Testing with missing parts into the path: /create/<username>/<first_name>/<last_name>/<email>')
        tester = application.test_client(self)
        username = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        first_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        last_name = ''.join(choice(ascii_uppercase) for i in range(choice(range(1,33))))
        email = ''.join(choice(ascii_uppercase) for i in range(23)) + "@gmail.com"
        paths = [
            f'/create/{username}/{first_name}/{last_name}',
            f'/create/{username}/{first_name}/{email}',
            f'/create/{username}/{last_name}/{email}',
            f'/create/{first_name}/{last_name}/{email}',
            f'/{username}/{first_name}/{last_name}/{email}',
        ]
        response = tester.post(paths[choice(range(len(paths)))])
        self.assertTrue(b'"message":"No such path!"' in response.data)
        
    #Test update status code
    def test_update_status(self):
        print('Testing status code for path: /update/<username>/<column>/<value>')
        tester = application.test_client(self)
        random_username = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        cols = [
            "first_name",
            "last_name",
            "email"
        ]
        column = choice(cols)
        if column == "email":
            random_value = ''.join(choice(ascii_uppercase) for i in range(choice(range(23)))) + '@gmail.com'
        else:
            random_value = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        
        response = tester.patch(f"/update/{random_username}/{column}/{random_value}")
        self.assertEqual(response.status_code,200)
        
    #Test update with GET
    def test_update_get(self):
        print('Testing GET request at path: /update/<username>/<column>/<value>')
        tester = application.test_client(self)
        random_username = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        cols = [
            "first_name",
            "last_name",
            "email"
        ]
        column = choice(cols)
        if column == "email":
            random_value = ''.join(choice(ascii_uppercase) for i in range(choice(range(23)))) + '@gmail.com'
        else:
            random_value = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        
        response = tester.post(f"/update/{random_username}/{column}/{random_value}")
        self.assertEqual(response.status_code,405)
        
    #Test update with POST
    def test_update_post(self):
        print('Testing POST request at path: /update/<username>/<column>/<value>')
        tester = application.test_client(self)
        random_username = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        cols = [
            "first_name",
            "last_name",
            "email"
        ]
        column = choice(cols)
        if column == "email":
            random_value = ''.join(choice(ascii_uppercase) for i in range(choice(range(23)))) + '@gmail.com'
        else:
            random_value = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        
        response = tester.post(f"/update/{random_username}/{column}/{random_value}")
        self.assertEqual(response.status_code,405)
        
    #Test update with DELETE
    def test_update_delete(self):
        print('Testing DELETE request at path: /update/<username>/<column>/<value>')
        tester = application.test_client(self)
        random_username = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        cols = [
            "first_name",
            "last_name",
            "email"
        ]
        column = choice(cols)
        if column == "email":
            random_value = ''.join(choice(ascii_uppercase) for i in range(choice(range(23)))) + '@gmail.com'
        else:
            random_value = ''.join(choice(ascii_uppercase) for i in range(choice(range(32))))
        
        response = tester.post(f"/update/{random_username}/{column}/{random_value}")
        self.assertEqual(response.status_code,405)
        
    #Test update with known username
    def test_update_known(self):
        print('Testing with known username for path: /update/<username>/<column>/<value>')
        tester = application.test_client(self)
        response = tester.patch("/update/blag0/first_name/TestName")
        self.assertIn(b'"first_name":"TestName"',response.data)
        
    #Test update with unknown username
    def test_update_known(self):
        print('Testing with unknown username for path: /update/<username>/<column>/<value>')
        tester = application.test_client(self)
        response = tester.patch("/update/POR/first_name/TestName")
        self.assertIn(b'"message":"No record found!"',response.data)
        
    #Test add_email status
    def test_mail_status(self):
        print('Testing status code for path: /add_email/<username>/<value>')
        tester = application.test_client(self)
        response = tester.post("/add_email/blag0/testemail@testdomain.com")
        self.assertTrue(response.status_code,200)
        
    #Test add_email GET
    def test_mail_get(self):
        print('Testing GET request at path: /add_email/<username>/<value>')
        tester = application.test_client(self)
        response = tester.get("/add_email/blag0/testemail@testdomain.com")
        self.assertTrue(response.status_code,405)
        
    #Test add_email PATCH
    def test_mail_patch(self):
        print('Testing PATCH request at path: /add_email/<username>/<value>')
        tester = application.test_client(self)
        response = tester.patch("/add_email/blag0/testemail@testdomain.com")
        self.assertTrue(response.status_code,405)
        
    #Test add_email DELETE
    def test_mail_delete(self):
        print('Testing DELETE request at path: /add_email/<username>/<value>')
        tester = application.test_client(self)
        response = tester.delete("/add_email/blag0/testemail@testdomain.com")
        self.assertTrue(response.status_code,405)
        
    #Test add_email content type
    def test_mail_content_type(self):
        print('Testing content type for path: /add_email/<username>/<value>')
        tester = application.test_client(self)
        response = tester.post("/add_email/blag0/testemail@testdomain.com")
        self.assertEqual(response.content_type,"application/json")
        
    #Test add_email content with known data
    def test_mail_content_known(self):
        print('Testing content type for path: /add_email/<username>/<value>')
        tester = application.test_client(self)
        response = tester.post("/add_email/blag0/testemail@testdomain.com")
        self.assertIn(b'"first_name":"Blagoy"',response.data)
        
    #Test add_email content with unknown data
    def test_mail_content_unknown(self):
        print('Testing content type for path: /add_email/<username>/<value>')
        tester = application.test_client(self)
        response = tester.post("/add_email/POR/testemail@testdomain.com")
        self.assertIn(b'"message":"Record not found!"',response.data)
        
    #Test delete status
    def test_delete_status(self):
        print('Testing status code for path: /delete/<username>')
        tester = application.test_client(self)
        username = session.query(Contact).filter_by(valid_till_date = None).first().username
        response = tester.delete(f"/delete/{username}")
        self.assertTrue(response.status_code,405)
        
    #Test delete GET
    def test_delete_get(self):
        print('Testing GET request at path: /delete/<username>')
        tester = application.test_client(self)
        username = session.query(Contact).filter_by(valid_till_date = None).first().username
        response = tester.delete(f"/delete/{username}")
        self.assertTrue(response.status_code,405)
        
    #Test delete PATCH
    def test_delete_patch(self):
        print('Testing PATCH request at path: /delete/<username>')
        tester = application.test_client(self)
        username = session.query(Contact).filter_by(valid_till_date = None).first().username
        response = tester.delete(f"/delete/{username}")
        self.assertTrue(response.status_code,405)
        
    #Test delete DELETE
    def test_delete_delete(self):
        print('Testing DELETE request at path: /delete/<username>')
        tester = application.test_client(self)
        username = session.query(Contact).filter_by(valid_till_date = None).first().username
        response = tester.delete(f"/delete/{username}")
        self.assertTrue(response.status_code,200)
        
    #Test delete content type
    def test_delete_content_type(self):
        print('Testing content type for path: /delete/<username>')
        tester = application.test_client(self)
        username = session.query(Contact).filter_by(valid_till_date = None).first().username
        response = tester.delete(f"/delete/{username}")
        self.assertEqual(response.content_type,"application/json")
        
    #Test delete content with known data
    def test_delete_content_known(self):
        print('Testing content type for path: /delete/<username>')
        tester = application.test_client(self)
        username = session.query(Contact).filter_by(valid_till_date = None).first().username
        response = tester.delete(f"/delete/{username}")
        self.assertIn(b'"message":"Record deleted!"',response.data)
        
    #Test delete content with unknown data
    def test_delete_content_unknown(self):
        print('Testing content type for path: /delete/<username>')
        tester = application.test_client(self)
        response = tester.delete("/delete/POR")
        self.assertIn(b'"message":"No record found!"',response.data)
        
    

if __name__ == "__main__":
    create_random_contact()
    unittest.main()