from sqlalchemy import select, update, delete
from sqlalchemy.orm import aliased
from models import Films, Tag, ConnectionTable, session


class CRUD:
    dataBase = session()

    def create_film(self, film: dict):
        with self.dataBase as db:
            create = [Films(name=film['name'], year=film['year'], rating=film['rating'])]
            con_tab = []
            for rate in film['tags']:
                create.append(Tag(name=rate))
            db.add_all(create)
            db.commit()
            for i in range(len(film['tags'])):
                con_tab.append(ConnectionTable(film_id=create[0].id, tag_id=create[i+1].id))
            db.add_all(con_tab)
            db.commit()

            answer = dict(id=create[0].id,
                          name=create[0].name,
                          year=create[0].year,
                          tags=[create[item].name for item in range(1, len(create))],
                          rating=create[0].rating)

            return answer

    def get_films(self, year: int, tags: list):
        with self.dataBase as db:
            query = db.query(Films) \
            .join(ConnectionTable, Films.id == ConnectionTable.film_id, isouter=True) \
            .join(Tag, Tag.id == ConnectionTable.tag_id, isouter=True) \
            .where(Films.year == year or Tag.name == tags[0] or Tag.name == tags[1] or Tag.name == tags[2]).all()
            answer = []
            for i in query:
                answer.append(self.get_film(i.id))
            return answer


    def get_film(self, film_id: int):
        result = self.get_result(film_id)
        answer = [dict(id=result[0][0],
                       name=result[0][1],
                       year=result[0][2],
                       tags=[item[3] for item in result],
                       rating=result[0][4])]

        return answer

    def update_comment(self, film_id: int, new_film: dict):
        result = self.get_result(film_id)
        with self.dataBase as db:
            film = db.get(Films, film_id)
            film.name = new_film['name']
            film.year = new_film['year']
            film.rating = new_film['rating']
            for tag in range(len(new_film['tags'])):
                upd = (update(Tag).where(Tag.id == result[tag][-1]).values(name=new_film['tags'][tag]))
                db.execute(upd)
            db.commit()
        return self.get_film(film_id)

    def delete_film(self, film_id: int):
        answer = self.get_film(film_id)
        result = self.get_result(film_id)
        with self.dataBase as db:
            query = delete(Films).where(Films.id == result[0][0])
            db.execute(query)
            for tag in range(len(result)):
                query = delete(Tag).where(Tag.id == result[tag][-3])
                db.execute(query)
                query = delete(ConnectionTable).where(ConnectionTable.tag_id == result[tag][-3])
                db.execute(query)
            db.commit()
            return answer



    def get_result(self, film_id):
        with self.dataBase as db:
            c = aliased(ConnectionTable)
            f = aliased(Films)
            t = aliased(Tag)
            query = (
                select(
                    f.id,
                    f.name,
                    f.year,
                    t.name,
                    f.rating,
                    t.id,
                    c.film_id,
                    c.tag_id
                )
                .select_from(c)
                .join(t, t.id == c.tag_id, isouter=True)
                .join(f, f.id == c.film_id, isouter=True)
                .filter(f.id == film_id)
            )
            result = db.execute(query).all()
            return result