from flask import Flask, render_template, redirect, request
import datetime

app = Flask(__name__)

blogs = [{"title":"Title2"}]
users = {"user":"pass"}

logged_in = False;


@app.route('/')
def displaylist():
    return render_template('list.html', blogs=blogs)


@app.route('/dashboard')
def display():
    if(logged_in):
        return render_template('dashboard.html', blogs=blogs)
    else:
        return redirect("/login")


@app.route('/add')
def add():
    if (logged_in):
        return render_template('add.html', blogs=blogs)
    else:
        return redirect("/login")


@app.route('/edit', methods=['GET'])
def edit():
    if (logged_in):
        index = int(request.args["index"])
        return render_template('edit.html', blogpost=blogs[index-1], index=index)
    else:
        return redirect("/login")


@app.route('/submit', methods=['POST'])
def submit():
    if (not logged_in):
        return redirect("/")

    global status
    print(request.form)
    title = request.form['title']
    author = request.form['author']
    date = datetime.datetime.now()
    content = request.form['content']
    index = request.form.get(
        'index'
    )
    print(index)
    post = {"title": title, "date": date, "author": author, "content": content}
    print(post)

    if title == "":
        status = "Title required."
        return redirect("/")
    elif author == "":
        status = "Author required."
        return redirect("/")
    elif date == "":
        status = "Date required."
        return redirect("/")
    elif content == "":
        status = "No content"
        return redirect("/")
    else:
        if(index is None):
            blogs.append(post)
        else:
            blogs[int(index)-1] = post

    return redirect("/dashboard")


@app.route('/login', methods=['GET'])
def loginview():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    global logged_in
    print("inside post", request.form)
    username = str(request.form['username'])
    passw = str(request.form['password'])
    if(users[username]==passw):
        logged_in = True
        return redirect("/dashboard")
    else:
        return redirect("/login", message="Login Error")


@app.route('/clear', methods=['POST'])
def clear():

    del blogs[:]
    return redirect("/")


@app.route('/delete', methods=['POST'])
def delete():
    delete_index = int(request.form['index'])
    del blogs[delete_index-1]
    return redirect("/dashboard")


if __name__ == "__main__":
    app.run()