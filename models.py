from app import db


################################################################
################################################################
################################################################
rel_table = db.Table('tags',
    db.Column('input_id', db.Integer, db.ForeignKey('input.id'), primary_key=True),
    db.Column('form_id', db.Integer, db.ForeignKey('form.id'), primary_key=True)
)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), default='')
    slug = db.Column(db.String(140), default='')
    inputs = db.relationship(
        'Input', secondary=rel_table, lazy='subquery',
        backref=db.backref('forms', lazy=True))
    xpaths = db.relationship(
        'Xpath', lazy='subquery',
        backref=db.backref('forms', lazy=True))

    def __repr__(self):
        return '{name}'.format(
            name=self.name)


class Param(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), default='')
    value = db.Column(db.String(140), default='')
    check_xpath = db.Column(db.String(250), default='')
    xpaths = db.Column(db.Integer, db.ForeignKey('xpath.id'))


class Xpath(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    xpath = db.Column(db.String(140), default='')
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'))
    params = db.relationship(
        'Param', lazy='subquery',
        backref=db.backref('Xpath', lazy=True))

    def __repr__(self):
        return '{xpath}'.format(
            xpath=self.xpath)


class Input(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140), default='')
    name = db.Column(db.String(140), default='')
    type = db.Column(db.String(140), default='checkbox')
    value = db.Column(db.String(140), default='')

    def __repr__(self):
        return '{text}<{type}>'.format(
            text=self.text,
            type=self.type)


################################################################
################################################################
################################################################
class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domen = db.Column(db.String(140), unique=True)
    wap = db.Column(db.String(140), default='')
    web = db.Column(db.String(140), default='')

    def __repr__(self):
        return '{domen}: ({wap}, {web})'.format(
            domen=self.domen,
            wap=self.wap,
            web=self.web)


class ListForm(db.Model):
    name = db.Column(db.String(140), unique=True)
    slug = db.Column(db.String(140), unique=True, primary_key=True)
    wap = db.Column(db.String(140), default='')
    web = db.Column(db.String(140), default='')


class SurfTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    landing_url = db.Column(db.String(256))
    tds_url = db.Column(db.String(256))
    traffic_type = db.Column(db.String(3))
    email_type = db.Column(db.String(3))
    country = db.Column(db.String(2))

    def __repr__(self):
        return '{email} {country} {type} {landing}'.format(
            email=self.email_type,
            country=self.country,
            type=self.traffic_type,
            landing=self.landing_url)
