import pandas as pd
import numpy as np
import pytest

from bot import msg2list, msg2df, predict, select_file_type


def test_msg2list():
    msg = "hba1c:7.14,   ubp:132.6,   lbp:103.3,   bmi:41.39,  age:35, glycemia: 6.79, gender:1, insulin:0.62;"
    answer = ["hba1c:7.14", "ubp:132.6", "lbp:103.3", "bmi:41.39",
              "age:35", "glycemia:6.79", "gender:1", "insulin:0.62"]
    assert msg2list(msg) == answer

    msg = "hba1c:7.14,   ubp:132.6,   lbp:103.3,   bmi:41.39,  age:35, glycemia: 6.79, gender:1, insulin:0.62"
    answer = ["hba1c:7.14", "ubp:132.6", "lbp:103.3", "bmi:41.39",
              "age:35", "glycemia:6.79", "gender:1", "insulin:0.62"]
    assert msg2list(msg) == answer

    msg = "hba1c:7.14,   ubp:132.6,   lbp:103.3,   bmi:41.39,  age:35, glycemia: 6.79,   gender:1, insulin:0.62;" \
          "hba1c:6.42,   ubp:121.7,   lbp:90.3,   bmi:34.74,  age:18, glycemia: 5.54,   gender:1, insulin:0.25;"
    answer = ["hba1c:7.14", "ubp:132.6", "lbp:103.3", "bmi:41.39",
              "age:35", "glycemia:6.79", "gender:1", "insulin:0.62",
              "hba1c:6.42", "ubp:121.7", "lbp:90.3", "bmi:34.74",
              "age:18", "glycemia:5.54", "gender:1", "insulin:0.25"]
    assert msg2list(msg) == answer


def test_msg2df():
    msg_data = ["hba1c:7.14", "ubp:132.6", "lbp:103.3", "bmi:41.39",
                "age:35", "glycemia:6.79", "gender:1", "insulin:0.62"]
    answer = pd.DataFrame(np.array([[7.14, 132.6, 103.3, 41.39, 35, 6.79, 1, 0.62]]),
                          columns=['hba1c', 'ubp', 'lbp', 'bmi', 'age', 'glycemia', 'gender', 'insulin'])
    assert msg2df(msg_data).equals(answer)

    msg_data = ["hba1c:7.14", "ubp:132.6", "lbp:103.3", "bmi:41.39",
                "age:35", "glycemia:6.79", "gender:1", "insulin:0.62",
                "hba1c:6.42", "ubp:121.7", "lbp:90.3", "bmi:34.74",
                "age:18", "glycemia:5.54", "gender:1", "insulin:0.25"]
    answer = pd.DataFrame(np.array([[7.14, 132.6, 103.3, 41.39, 35, 6.79, 1, 0.62],
                                    [6.42, 121.7, 90.3, 34.74, 18, 5.54, 1, 0.25]]),
                          columns=['hba1c', 'ubp', 'lbp', 'bmi', 'age', 'glycemia', 'gender', 'insulin'])
    assert msg2df(msg_data).equals(answer)

    msg_data = ["hbc:7.14", "ubp:132.6", "lbp:103.3", "bmi:41.39",
                "age:35", "glycemia: 6.79", "gender:1", "insulin:0.62"]
    with pytest.raises(ValueError) as error:
        msg2df(msg_data)
    assert "Ошибка в имени признака!" == error.value.args[0]

    msg_data = ["hba1c:7.14", "ubp:132.6", "lbp:103.3", "bmi:41.39",
                "age:35", "glycemia: 6.79", "gender:1"]
    with pytest.raises(ValueError) as error:
        msg2df(msg_data)
    assert "All arrays must be of the same length" == error.value.args[0]


def test_predict():
    df = pd.DataFrame(np.array([[7.14, 132.6, 103.3, 41.39, 35, 6.79, 1, 0.62]]),
                      columns=['hba1c', 'ubp', 'lbp', 'bmi', 'age', 'glycemia', 'gender', 'insulin'])
    answer = "2"
    assert predict(df) == answer

    df = pd.DataFrame(np.array([[7.14, 132.6, 103.3, 41.39, 35, 6.79, 1, 0.62],
                                [6.42, 121.7, 90.3, 34.74, 18, 5.54, 1, 0.25]]),
                      columns=['hba1c', 'ubp', 'lbp', 'bmi', 'age', 'glycemia', 'gender', 'insulin'])
    answer = "2, 1"
    assert predict(df) == answer


def test_select_file_type():
    file_path = "example.json"
    df = pd.DataFrame(np.array([[7.14, 132.6, 103.3, 41.39, 35, 6.79, 1, 0.62]]),
                      columns=['hba1c', 'ubp', 'lbp', 'bmi', 'age', 'glycemia', 'gender', 'insulin'])
    answer = "result.json", df.to_json(orient="records").encode()
    assert select_file_type(file_path, df) == answer

    file_path = "example.csv"
    df = pd.DataFrame(np.array([[7.14, 132.6, 103.3, 41.39, 35, 6.79, 1, 0.62]]),
                      columns=['hba1c', 'ubp', 'lbp', 'bmi', 'age', 'glycemia', 'gender', 'insulin'])
    answer = "result.csv", df.to_csv(index=False).encode()
    assert select_file_type(file_path, df) == answer


if __name__ == '__main__':
    pytest.main()


