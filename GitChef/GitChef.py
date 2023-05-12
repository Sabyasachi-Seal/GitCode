import os

import lxml.html as lx
import requests
import shutil
from bs4 import BeautifulSoup as BS

username = input('CodeChef Username: ')
password = input('CodeChef Password: ')
scan_username = input('CodeChef Username of the user to be scraped: ')
problems = {}

extensions = {'ADA': '.abd', 'C++14': '.cpp', 'JAVA': '.java', 'PYPY': '.py', 'PYTH': '.py', 'PYTH 3.6': '.py',
              'C#': '.cs',
              'PAS fpc': '.pas', 'PAS gpc': '.pas', 'RUBY': '.ruby', 'PHP': '.php', 'GO': '.go', 'NODEJS': '.js',
              'HASK': '.hs', 'SCALA': 'scala', 'D': '.d', 'PERL': '.pl', 'PERL6': '.pl', 'FORT': '.f', 'WSPC': '.ws',
              'CAML': '.ml', 'BF': '.bf', 'ASM': '.asm', 'CLPS': '.cli', 'PRLG': '.pro', 'ICON': '.icn',
              'SCM qobi': '.scm', 'ST': '.st', 'NICE': '.nice', 'LUA': '.lua', 'BASH': '.sh', 'NEM': '.n',
              'LISP sbcl': '.lisp', 'LISP clisp': '.lisp', 'SCM guile': '.scm', 'JS': '.js', 'PYPY3': '.py', 'C': '.c',
              'PIKE': '.pike', 'C++ 4.0.0-8': '.cpp', 'C++ 4.3.2': '.cpp', 'C++ 4.8.1': '.cpp', 'C++ 4.9.2': '.cpp',
              'C++ 6.3': '.cpp', 'C++ g++-4.1': '.cpp', 'C++ MPI': '.cpp', 'C++11': '.cpp', 'C99 strict': '.c',
              'CLOJ': '.clj', 'PYTH 3.1.2': '.py', 'PYTH 3.4': '.py', 'PYTH 3.5': '.py', 'SCM chicken': '.scm',
              'COB': '.cob', 'ERL': '.erl', 'F#': '.fs', 'kotlin': '.kt', 'JAR': '.jar', 'KTLN': '.ktl', 'ICK': '.i',
              'R': '.r', 'rust': '.rust', 'swift': '.swift', 'SQL': '.sql', 'TEXT': '.txt', 'TCL': '.tcl'}
headers = {
    'user-agent': 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/77.0.3865.120 Safari/537.36 OPR/64.0.3417.92'
}

with requests.session() as s:
    def main():
        try:
            login = s.get('https://www.codechef.com/', headers=headers)
            login_html = lx.fromstring(login.text)
            hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
            form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
            form['name'] = username
            form['pass'] = password
            form['form_id'] = 'new_login_form'
            response = s.post('https://www.codechef.com/',
                              data=form, headers=headers)
            if response.url == 'https://www.codechef.com/node':
                print('Logged in!')
                get_problems()
            elif response.url == 'https://www.codechef.com/session/limit':
                print(
                    'Session limit reached! Logout of all active sessions before continuing!')
            else:
                print('Login failed! Check credentials and try again!')
            s.get('https://www.codechef.com/logout', headers=headers)
            print('Logged out!')
        except:
            print('Some error occurred!')
        s.get('https://www.codechef.com/logout', headers=headers)

    def get_problems():
        print('Fetching AC problems!')
        len_username = len(scan_username)
        r = s.get('https://www.codechef.com/users/' +
                  scan_username, headers=headers)
        data = r.text
        soup = BS(data, 'html5lib')
        for link in soup.find_all('a'):
            x = str(link.get('href'))
            if 'status' in x and scan_username in x:
                x = x[:len(x) - len_username - 1]
                ls = x.split('/')
                if len(ls) == 3:
                    contest_code = 'PRACTICE'
                    problem_code = str(ls[2])
                else:
                    contest_code = str(ls[1])
                    problem_code = str(ls[3])
                if contest_code not in problems.keys():
                    problems[contest_code] = []
                problems[contest_code].append(problem_code)
        extract_solutions()

    def extract_solutions():
        print('Extracting solutions!')
        for i in problems:
            try:
                os.mkdir(str('CodeChef Solutions/' + scan_username + '/' + i))
            except:
                print('Some error occurred during creation of folders!')
            for j in problems[i]:
                try:
                    if i == 'PRACTICE':
                        r = s.get(
                            'https://www.codechef.com/status/' + j + ',' + scan_username +
                            '?sort_by=All&sorting_order=asc&language=All&status=15&Submit=GO',
                            headers=headers)
                    else:
                        r = s.get(
                            'https://www.codechef.com/' + i + '/status/' + j + ',' + scan_username +
                            '?sort_by=All&sorting_order=asc&language=All&status=15&Submit=GO',
                            headers=headers)
                    data = r.text
                    soup = BS(data, 'html5lib')
                    ls = soup.findAll('td', {'width': '60'})
                    sol_id = ls[0].text
                    r = s.get('http://www.codechef.com/viewsolution/' +
                              sol_id, headers=headers)
                    data = r.text
                    soup = BS(data, 'html5lib')
                    st = str(soup)
                    lang_code = st[st.index(
                        'languageShortName') + 20:st.index('solutionMemory') - 3]
                    r = s.get(
                        'http://www.codechef.com/viewplaintext/' + sol_id, headers=headers)
                    data = r.text
                    soup = BS(data, 'html5lib')
                    code = soup.findAll('pre')[0].text
                    filename = j + ' ' + sol_id + extensions[lang_code]
                    path = str('CodeChef Solutions/' +
                               scan_username + '/' + i + '/' + filename)
                    code_file = open(path, 'w+')
                    code_file.write(code)
                    code_file.close()
                    print(filename + ' saved')
                except:
                    print(f'Could not save for {j}')

if __name__ == "__main__":
    try:
        print('Creating directory CodeChef Solutions')
        os.mkdir('CodeChef Solutions')
    except FileExistsError:
        print('Directory CodeChef Solutions already exists!')
    try:
        os.mkdir(str('CodeChef Solutions/' + scan_username))
    except FileExistsError:
        print('Directory CodeChef Solutions/' +
              scan_username + ' already exists!')
        print('Deleting directory CodeChef Solutions/' + scan_username)
        shutil.rmtree(str('CodeChef Solutions/' + scan_username))
        print('Creating directory CodeChef Solutions/' + scan_username)
        os.mkdir(str('CodeChef Solutions/' + scan_username))
    main()
