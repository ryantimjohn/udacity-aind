from functools import reduce
import operator

def dict_helper(dict, arr):
    try:
        return reduce(operator.getitem, arr, dict)
    except KeyError:
        return ""

movie = {

  "poster": {

    "color": {

      "size": "1024x768",

      "path": "This is the poster path for color"

    },

    "bw": {

      "path": "This is the poster path for back and white poster"

    }

  },

  "adult": False,

  "overview": "Jack Reacher must uncover the truth behind a major government conspiracy in order to clear his name. On the run as a fugitive from the law, Reacher uncovers a potential secret from his past that could change his life forever.",

  "release_date": "2016-10-19",

  "genre_ids": [

    53,

    28,

    80,

    18,

    9648

  ],

  "id": 343611,

  "original_title": "Jack Reacher: Never Go Back",

  "original_language": "en",

  "title": "Jack Reacher: Never Go Back",

  "backdrop_path": "/4ynQYtSEuU5hyipcGkfD6ncwtwz.jpg",

  "popularity": 26.818468,

  "vote_count": 201,

  "video": False,

  "vote_average": 4.19

}


print(dict_helper(movie, ["poster", "bw", "path"]))

print(dict_helper(movie, ["poster", "bw", "size"]))
