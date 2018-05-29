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


def connect_db():
    try:
        db = psycopg2.connect(database=DBNAME)
    except:
        print "something wrong to connect the datebase"


def query_pop_title():
    c = db.cursor()

