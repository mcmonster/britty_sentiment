from flask import render_template, request
from pattern.en import sentiment

from app import app

@app.route('/', methods = ["GET"])
def index():
    return render_template("upload_file.html")

@app.route('/sentiment_analysis', methods = ["POST"])
def sentiment_analysis():
    file_contents             = request.json["file_contents"]
    include_strongly_negative = request.json["include_strongly_negative"]
    include_strongly_positive = request.json["include_strongly_positive"]

    print "FileContents:", file_contents
    print "IncludeStronglyNegative:", include_strongly_negative
    print "IncludeStronglyPositive:", include_strongly_positive

    sentences = file_contents.split(".")
    results   = ""
    for iter in range(len(sentences)):
        polarity, subjectivity = sentiment(sentences[iter])
       
        if ((include_strongly_positive and (polarity > 0.7)) or
            (include_strongly_negative and (polarity < -0.7))):
            results += '<div class="entry">'
            results += "<b>File:</b>&nbsp;&nbsp;" + request.json["file"] + "&nbsp;&nbsp;"
            results += "<b>Polarity:</b>&nbsp;&nbsp;" + str(polarity) + "&nbsp;&nbsp;"
            results +=" <b>Subjectivity:</b>&nbsp;&nbsp;" + str(subjectivity) + "<br />"
            if iter-2 >= 0:
                results += sentences[iter-2] + " "
            if iter-1 >= 0:
                results += sentences[iter-1] + " "
            results += '<span style="color:red; font-size: 150%;">' + sentences[iter] + ' </span>'
            if iter+1 < len(sentences):
                results += sentences[iter+1] + " "
            if iter+2 < len(sentences):
                results += sentences[iter+2] + " "
            results += "</div><br />"

    return results
