from flask import Flask, render_template, redirect, request, session, url_for
import csv

app = Flask(__name__)


@app.route('/')
def route_index():
    database = read_database("database.csv")
    url_list = []
    for data in database:
        url_list.append(data[0])
    return render_template("list.html", database=database)


@app.route('/story')
def route_edit():
    update = None
    return render_template("form.html", update=update)


@app.route('/story/<story_id>')
def route_update(story_id):
    update = 1
    database = read_database("database.csv")
    title = database[int(story_id)-1][1]
    story = database[int(story_id)-1][2]
    criteria = database[int(story_id)-1][3]
    value = database[int(story_id)-1][4]
    estimation = database[int(story_id)-1][5]
    status = database[int(story_id)-1][6]
    return render_template('form.html', title=title, story=story, criteria=criteria, value=value, estimation=estimation, status=status, update=update)


@app.route('/save-story', methods=['POST'])
def route_save():
    database = read_database("database.csv")
    user_story = []
    try:
        user_story.append(int(database[-1][0])+1)
    except IndexError:
        user_story.append("1")
    user_story.append(request.form["title"])
    user_story.append(request.form["story"])
    user_story.append(request.form["criteria"])
    user_story.append(request.form["value"])
    user_story.append(request.form["estimation"])
    user_story.append(request.form["status"])
    database.append(user_story)
    with open("database.csv", "w") as data:
        writer = csv.writer(data)
        writer.writerows(database)
    return redirect('/')


def read_database(datafile):
    with open(datafile, "r") as database:
        table = list(list(row) for row in csv.reader(database, delimiter=','))
    return table


app.secret_key = "you!never!guess!this"

if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
