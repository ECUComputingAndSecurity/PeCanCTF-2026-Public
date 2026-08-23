from flask import Flask, request, render_template, make_response, redirect
import docx
import sqlite3

app = Flask(__name__, static_url_path='')

def allowed_file(filename):
	return "." in filename and filename.split(".", 1)[1].lower() == "docx"

def get_creator(file_stream):
    doc = docx.Document(file_stream)
    core_properties = doc.core_properties
    author = getattr(core_properties, "author", "")

    return author
     

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    file = request.files["file"]

    if not file:
        return "No file selected"
    
    if file.filename == "":
        return "No file selected"

    if not allowed_file(file.filename):
        return "Not an allowed file name"
    
    author = get_creator(file.stream)

    if author == "":
        return "Could not find file author"
        
    
    conn = sqlite3.connect("file:office.db?mode=ro", uri=True)
    try:
        cursor = conn.cursor()
        query = "SELECT name FROM docs WHERE creator = '" + author.lower() + "';"
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as e:
        results = [str(e)]
    finally:
        cursor.close()
        conn.close()
			
    return render_template("index.html", results=results, name_searched=author)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=80)