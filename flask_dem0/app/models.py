from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    f_name: so.Mapped[str] = so.mapped_column(sa.String(45), index=True)
    l_name: so.Mapped[str] = so.mapped_column(sa.String(45), index=True)

    bio: so.Mapped[str] = so.mapped_column(sa.String(180), index=True)

    preference: so.WriteOnlyMapped['User_Preference'] = so.relationship(back_populates='user')

    def __repr__(self):
        return f'<User: {self.username}>, <Password: {self.password_hash}>, <{self.f_name}, {self.l_name}>'
    
class Preference(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    name: so.Mapped[str] = so.mapped_column(sa.String(45), index=True)

    user_preference: so.WriteOnlyMapped['User_Preference'] = so.relationship(back_populates='preference')


class User_Preference(db.Model):

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True, primary_key=True)
    preference_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Preference.id), index=True, primary_key=True)

    user: so.Mapped[User] = so.relationship(back_populates='preference')

    preference: so.Mapped[Preference] = so.relationship(back_populates='user_preference')

    rank: so.Mapped[int] = so.mapped_column(index=True)