from typing import Optional
from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from app import db, login

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    f_name: so.Mapped[str] = so.mapped_column(sa.String(45), index=True)
    l_name: so.Mapped[str] = so.mapped_column(sa.String(45), index=True)

    bio: so.Mapped[str] = so.mapped_column(sa.String(180), index=True)

    apartment_id: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, sa.ForeignKey('apartment.id'), nullable=True)

    apartment : so.Mapped[Optional['Apartment']] = so.relationship(
        back_populates='users'
        )

    preference: so.WriteOnlyMapped['User_Preference'] = so.relationship(back_populates='user')
    sent_messages: so.Mapped[list["message"]] = so.relationship(
        "message", 
        foreign_keys="message.sender_id",
        back_populates="sender"
    )
    
    received_messages: so.Mapped[list["message"]] = so.relationship(
        "message", 
        foreign_keys="message.receiver_id", 
        back_populates="receiver"
    )

    sent_rating: so.Mapped[list["rating"]] = so.relationship(
        "rating", 
        foreign_keys="rating.sender_id",
        back_populates="sender"
    )
    
    received_rating: so.Mapped[list["rating"]] = so.relationship(
        "rating", 
        foreign_keys="rating.receiver_id", 
        back_populates="receiver"
    )

    user1_bp_u: so.Mapped[list["match"]] = so.relationship(
        "match", 
        foreign_keys="match.user1",
        back_populates="user1_bp"
    )
    
    user2_bp_u: so.Mapped[list["match"]] = so.relationship(
        "match", 
        foreign_keys="match.user2", 
        back_populates="user2_bp"
    )

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

class message(db.Model):

    message_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    receiver_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    sender_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    message: so.Mapped[str] = so.mapped_column(sa.String(180), index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(default=datetime.now(timezone.utc))

    sender: so.Mapped["User"] = so.relationship(
        "User", 
        foreign_keys=[sender_id],
        back_populates="sent_messages"
    )
    
    receiver: so.Mapped["User"] = so.relationship(
        "User", 
        foreign_keys=[receiver_id], 
        back_populates="received_messages"
    )

class rating(db.Model):

    rating_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    receiver_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    sender_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    message: so.Mapped[str] = so.mapped_column(sa.String(180), index=True)

    sender: so.Mapped["User"] = so.relationship(
        "User", 
        foreign_keys=[sender_id],
        back_populates="sent_rating"
    )
    
    receiver: so.Mapped["User"] = so.relationship(
        "User", 
        foreign_keys=[receiver_id], 
        back_populates="received_rating"
    )

class match(db.Model):

    match_id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user1: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    user2: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    percentage: so.Mapped[float] = so.mapped_column()

    user1_bp: so.Mapped["User"] = so.relationship(
        "User", 
        foreign_keys=[user1],
        back_populates="user1_bp_u"
    )
    
    user2_bp: so.Mapped["User"] = so.relationship(
        "User", 
        foreign_keys=[user2], 
        back_populates="user2_bp_u"
    )

class Apartment(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(45), index=True)
    display_name: so.Mapped[str] = so.mapped_column(sa.String(45), index=True)
    url_slug: so.Mapped[str] = so.mapped_column(sa.String(45), index=True)

    users: so.Mapped[list["User"]] = so.relationship(
        "User",
        back_populates="apartment"
    )

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))
    