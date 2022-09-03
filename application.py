from flask import Flask

def find_prime(n):
    result = 0
    prime_numbers = [2, 3]
    i = 3
    if (0 < n < 3):
        # print(n, 'th Prime Number is :', prime_numbers[n - 1])
        result=prime_numbers[n - 1]
    elif (n > 2):
        while (True):
            i += 1
            status = True
            for j in range(2, int(i / 2) + 1):
                if (i % j == 0):
                    status = False
                    break
            if (status == True):
                prime_numbers.append(i)
            if (len(prime_numbers) == n):
                break
        # print(n, 'th Prime Number is :', prime_numbers[n - 1])
        result=prime_numbers[n - 1]
    else:
        # print('Please Enter A Valid Number')
        pass
    return result
# print a nice greeting.
def say_hello(n = "1"):
    try:
        n=int(n)
    except:
        pass
    return '<p>%s</p>\n' % find_prime(n)


# some bits of text for the page.
header_text = '''
    <html>\n<head> <title>EB Flask Test</title> </head>\n<body>'''
instructions = '''
    <p><em>Hint</em>: This backend return the N-th prime number! Append a intrger
    to the URL (for example: <code>/17</code>) to find the 17th prime number.</p>\n'''
home_link = '<p><a href="/">Back</a></p>\n'
footer_text = '</body>\n</html>'

# EB looks for an 'application' callable by default.
application = Flask(__name__)

# add a rule for the index page.
application.add_url_rule('/', 'index', (lambda: header_text +
    say_hello() + instructions + footer_text))

# add a rule when the page is accessed with a name appended to the site
# URL.
application.add_url_rule('/<username>', 'hello', (lambda username:
    header_text + say_hello(username) + home_link + footer_text))

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()