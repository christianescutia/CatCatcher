# import needed to connect to postgress server
import psycopg2

# define database connection data
conn = psycopg2.connect(
    host = "ec2-54-90-13-87.compute-1.amazonaws.com",
    database = "ddg16dt0q9df1t",
    user = "ofxriywaexambz",
    password = "15180294c0a4537da6c6cb7f5ecd6931aa138f1e2968d802268b942554828624",
    port = "5432"
)

# create cursor
c = conn.cursor()

# add user to database
# SELECT username, pwd from Users WHERE username = 'cheraten';
username = 'cheraten'
password = 'testpwd1'
sql_command = "SELECT username, pwd FROM users WHERE username = \'" + str(username) +"\'"

# executeb SQL Command
c.execute( sql_command)

# commit changes
conn.commit()

username_d = ''
password_d = ''

for x in c:
    username_d = str(x[0])
    password_d = str(x[1])

print('Data Found:')
print(username_d)
print(password_d)

# close database connection
conn.close()