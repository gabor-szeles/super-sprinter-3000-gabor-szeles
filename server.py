from flask import Flask, render_template, redirect, request, session, url_for
import csv

app = Flask(__name__)


@app.route('/')
def route_index():
    database = read_database("database.csv")
    return render_template("list.html", database=database)


@app.route('/story')
def route_edit():
    update = None
    return render_template("form.html", update=update)


@app.route('/story/<story_id>')
def route_update(story_id):
    update = 1
    database = read_database("database.csv")
    for data in database:
        if data[0] == story_id:
            id_ = data[0]
            title = data[1]
            story = data[2]
            criteria = data[3]
            value = data[4]
            estimation = data[5]
            status = data[6]
    return render_template('form.html', database=database, id=id_, title=title, story=story, criteria=criteria,
                           value=value, estimation=estimation, status=status, update=update)


@app.route('/save-story', methods=['POST'])
def route_save():
    database = read_database("database.csv")
    user_story = build_story()
    try:
        id_list = []
        for data in database:
            id_list.append(int(data[0]))
        user_story.insert(0, max(id_list)+1)
    except IndexError:
        user_story.insert(0, "1")
    database.append(user_story)
    export_data("database.csv", database)
    return redirect('/')


@app.route('/delete/<story_id>', methods=['POST'])
def route_delete(story_id):
    database = read_database("database.csv")
    for lists in database:
        if lists[0] == story_id:
            database.remove(lists)
    export_data("database.csv", database)
    return redirect('/')


@app.route('/update-story/<story_id>', methods=['POST'])
def route_save_update(story_id):
    database = read_database("database.csv")
    user_story = build_story()
    user_story.insert(0, story_id)
    for lists in database:
        if lists[0] == story_id:
            database.remove(lists)
    database.append(user_story)
    export_data("database.csv", database)
    return redirect('/')


def build_story():
    user_story = []
    user_story.append(request.form["title"])
    user_story.append(request.form["story"])
    user_story.append(request.form["criteria"])
    user_story.append(request.form["value"])
    user_story.append(request.form["estimation"])
    user_story.append(request.form["status"])
    return user_story


def read_database(datafile):
    with open(datafile, "r") as database:
        table = list(list(row) for row in csv.reader(database, delimiter=','))
    return table


def export_data(export_file, database):
    with open(export_file, "w") as data:
        writer = csv.writer(data)
        writer.writerows(database)


if __name__ == "__main__":
    app.secret_key = "you!never!guess!this"
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
