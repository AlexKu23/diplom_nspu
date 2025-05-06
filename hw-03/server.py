import typing as tp
import pandas as pd
import gspread
from flask import Flask, request, render_template
from werkzeug.wrappers import Response
from config import VARS


app = Flask(__name__)
# app.config["DEBUG"] = True


def get_table(name_hw: str) -> pd.DataFrame:
    """
    Connects to Google Sheets API and gets a table with homework

    Parameters:
        name_hw: The name of homework

    Returns:
        The pd.DataFrame with the results of homework
    """
    if getattr(get_table, "__gc", None) is None:
        get_table.__gc = gspread.service_account(filename=VARS.CREDENTIAL)
        get_table.__sh = get_table.__gc.open_by_key(VARS.SHEET_KEY)

    df = pd.DataFrame(get_table.__sh.worksheet(name_hw).get_all_records())
    df.columns = ["Id", "Name", "Group", "Link", "Scores"]
    df.Scores = df.Scores.replace(r"^\s*$", 0, regex=True)
    return df


def get_score(scores: int) -> int:
    """
    The number of points determines what grade to give to the person

    Parameters:
        scores: Points scored by a person for a task

    Returns:
        2 <= The grade <= 5
    """
    if scores > 50:
        return 5
    elif scores > 30:
        return 4
    elif scores >= 1:
        return 3
    return 2


class InvalidRequest(Exception):
    status_code = 400

    def __init__(self, message):
        super().__init__()
        self.message = message

    def to_dict(self):
        rv = {"status": "Bad request", "message": self.message}
        return rv


@app.errorhandler(InvalidRequest)
def invalid_request(e):
    return e.to_dict(), e.status_code


@app.route("/names")
def names() -> tp.Dict[str, tp.List[str]]:
    df = get_table("hw-01")
    return {"names": df.Name.str.split().str[-1].to_list()}


@app.route("/<hw_name>/mean_score")
def mean_score(hw_name: str) -> str:
    df = get_table(hw_name)
    ms = df.Scores.mean()
    return {"mean": ms}


@app.route("/<hw_name>/<int:group_id>/mean_score")
def mean_score_by_group(hw_name: str, group_id: int) -> str:
    df = get_table(hw_name)
    ms = df.groupby("Group").mean().loc[group_id].Scores
    return {"mean": ms}


@app.route("/mean_score")
def mean_score_from_get() -> str:
    hw_name = request.args.get("hw_name")
    group_id = int(request.args.get("group_id"))
    df = get_table(hw_name)
    ms = df.groupby("Group").mean().loc[group_id].Scores
    return {"mean": ms}


@app.route("/mark")
def mark() -> str:
    hw1 = get_table("hw-01")
    hw2 = get_table("hw-02")
    hw3 = get_table("hw-03")

    sum_scores = pd.concat([hw1, hw2, hw3]).groupby("Id").Scores.sum()
    scores = sum_scores.apply(get_score)

    df = hw1[["Id", "Group"]].merge(scores, on="Id")
    df = df.set_index("Id")
    df.loc[9, "Scores"] = 5  # Михаил Окань

    if "student_id" in request.args:
        student_id = int(request.args.get("student_id"))
        return str(df.loc[student_id, "Scores"])

    group_id = int(request.args.get("group_id"))
    ms = df.groupby("Group").mean().loc[group_id].Scores
    return {"grade": ms}


@app.route("/course_table")
def course_table() -> Response:
    if "hw_name" in request.args:
        hw_name = request.args.get("hw_name")
        df = get_table(hw_name)
        title = "PythonES2021"
        if "group_id" in request.args:
            group_id = int(request.args.get("group_id"))
            title = f"Группа {group_id}"
            df = df[df.Group == group_id]

        return render_template(
            "course_table.html", columns=df.columns, rows=df.values, title=title
        )
    else:
        raise InvalidRequest("It looks like you forgot to specify hw_name")


if __name__ == "__main__":
    app.run("0.0.0.0", port=1337)
