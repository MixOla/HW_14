import sqlite3


class DataBase:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()


    def get_by_title(self, query):
        """ Возвращает информацию о фильме по названию фильма """

        self.cursor.execute(f"""
                            SELECT title, country, release_year, listed_in, description
                            FROM netflix
                            WHERE title LIKE '%{query}%'
                            ORDER BY release_year DESC
                            LIMIT 1

                            """)

        result = self.cursor.fetchone()
        return {
            'title': result[0],
            'country': result[1],
            'release_year': result[2],
            'genre': result[3],
            'description': result[4]
        }

    def get_by_release_year(self, year_from, year_till):
        """ Возвращает список 100 фильмов, вышедших в период с year_from по year_till  """

        self.cursor.execute(f"""
                            SELECT title, release_year
                            FROM netflix
                            WHERE release_year BETWEEN {year_from} AND {year_till}
                            ORDER BY release_year ASC
                            LIMIT 100
                            """)

        result = self.cursor.fetchall()
        result_list = []
        keys = ['title', 'release_year']
        for item in result:
            result_list.append(dict(zip(keys, item)))

        return result_list

    def get_by_genre(self, genre):
        """ Функция получает название жанра в качестве аргумента и возвращает
        10 самых свежих фильмов в формате json  """

        self.cursor.execute(f"""SELECT title, description, listed_in 
                            FROM netflix
                            WHERE listed_in LIKE '%{genre}%'
                            ORDER BY release_year DESC
                            LIMIT 10
                            """)

        result = self.cursor.fetchall()
        result_list = []
        keys = ['title', 'description']
        for item in result:
            result_list.append(dict(zip(keys, (item[0], item[1]))))

        return result_list


    def get_by_rating(self, rating):
        """ Функция реализует поиск по возрастной группе """
        rat_dict = {
            "children": ("G", "G"),
            "family": ("G", "PG", "PG-13"),
            "adult": ("R", "NC-17")
        }
        self.cursor.execute(f"""SELECT title, rating, description FROM netflix
                            WHERE rating IN {rat_dict.get(rating, ("R"))}""")

        result = self.cursor.fetchall()

        result_list = []
        keys = ['title', 'rating', 'description']
        for film in result_list:
            result_list.append(dict(zip(keys, (film[0], film[1], film[2].rstrip('\n')))))

        return result


    def get_by_actors(self, actor_1, actor_2):
        """ Функция получает в качестве аргумента имена двух актеров,
         сохраняет всех актеров из колонки cast и возвращает список тех,
         кто играет с ними в паре больше 2 раз"""

        self.cursor.execute(f"""
                            SELECT netflix.cast 
                            FROM netflix
                            WHERE netflix.cast LIKE '%{actor_1}%'
                            AND netflix.cast LIKE '%{actor_2}%'
                            """)
        result = self.cursor.fetchall()
        # Получим список актеров, состоящий из строк
        result_1 = []
        for i in range(len(result)):
            for actors in result:
                result_1.extend(actors)

        # Получим список актеров
        result_2 = []
        for text in result_1:
            result_2.extend(text.split(", "))

        actors_d = {}.fromkeys(result_2, 0)
        for a in result_2:
            actors_d[a] += 1

        res_list_of_actors = []
        for key, value in actors_d.items():
            if value > 2 and key not in [actor_1, actor_2]:
                res_list_of_actors.append(key)

        return res_list_of_actors


    def get_by_3_params(self, type, release_year, genre):
        """ Функция получает название жанра, год выпуска и тип (сериал или фильм)
         в качестве аргумента и возвращает список названий подходящих фильмов """
        self.cursor.execute(f"""
                            SELECT title, description, type, release_year, listed_in 
                            FROM netflix
                            WHERE listed_in LIKE '%{genre}%'
                            AND type = '{type}'
                            AND release_year = {release_year}
                            """)

        result = self.cursor.fetchall()
        result_list = []
        keys = ['title', 'description']
        for item in result:
            result_list.append(dict(zip(keys, (item[0], item[1]))))
        return result_list


