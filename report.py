import psycopg2

DBNAME = "news"

# most popular three atticles
query_pop_title = (
    "select articles.title, count(*) "
    "from articles, log "
    "where log.path like concat ('%', articles.slug) "
    "and log.status = '200 OK'"
    "group by articles.title "
    "order by count desc limit 3;"
)

# select the most popular author
query_pop_author = (
    "select authors.name, count(*) "
    "from authors, articles, log "
    "where log.path like concat ('%', articles.slug) "
    "and log.status = '200 OK' "
    "and authors.id = articles.author "
    "group by authors.name "
    "order by count desc;"
)

# query to find the day when the server have errors more than 1%
query_error = (
    "select day, percentage from ("
    "select day, round((sum(numerator)/(select count(*) from log where "
    "date(time) = day) * 100), 2) as percentage from "
    "(select date(time) as day, count (*) as numerator from log "
    "where status not like '%200%' group by day) "
    "as log_percentage group by day order by percentage desc) as final_query "
    "where percentage >= 1"
)


# def connect_db():
#     try:
#         db = psycopg2.connect(database=DBNAME)
#         print "connect the database"
#     except:
#         print "something wrong to connect the database"


def pop_title():
    c = db.cursor()
    try:
        c.execute(query_pop_title)
    except:
        print "something wrong with qurying the articles"
    row = c.fetchall()
    print '''
    \n
    +--------------------------------+
    |                                |
    |   Three Most Popular Articles  |
    |                                |
    |      XX      XXXXX    XXXXX    |
    |    XXXX          X        X    |
    |   XX  X          X        X    |
    |       X      XXXXX     XXXX    |
    |       X      X            X    |
    |    XXXXXX    XXXXX    XXXXX    |
    |                                |
    +--------------------------------+
    \n
    '''
    for p in row:
        print "   ", p[0], " -- ", p[1], " (views)"
    return

 
def pop_author():
    c = db.cursor()
    try:
        c.execute(query_pop_author)
    except:
        print "something wrong with qurying the authors"
    row = c.fetchall()
    print '''
    \n
    +--------------------------------+
    |                                |
    |   Three Most Popular Authors   |
    |                                |
    |      XX      XXXXX    XXXXX    |
    |    XXXX          X        X    |
    |   XX  X          X        X    |
    |       X      XXXXX     XXXX    |
    |       X      X            X    |
    |    XXXXXX    XXXXX    XXXXX    |
    |                                |
    +--------------------------------+
    \n
    '''
    for p in row:
        print "   ", p[0], " -- ", p[1], " (views)"
    return


def error():
    c = db.cursor()
    try:
        c.execute(query_error)
    except:
        print "something wrong with qurying the server error"
    row = c.fetchall()
    print '''
    \n 
    +-----------------------------------+
    |                                   |
    | The Day Server Error More Than 1% |
    |                                   |
    |                                   |
    |                                   |
    |           XX       XXXX    XX     |
    |         XXXX       X  X   XX      |
    |       XXX  X       XXXX  XX       |
    |            X             X        |
    |            X            X         |
    |            X           XX         |
    |            X         XXX  XXXX    |
    |       XXXXXXXXXX    XX    X  X    |
    |                    XX     XXXX    |
    +-----------------------------------+
    \n
    '''
    for p in row:
        print "   ", p[0], "--", p[1], '% errors'
    return


# connect_db()
try:
    db = psycopg2.connect(database=DBNAME)
    print "connect the database"
except:
    print "something wrong to connect the database"
pop_title()
pop_author()
error()
db.close()