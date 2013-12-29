import sqlalchemy as sa
from os import environ

db = environ['FIELDWORKDB']

engine = sa.create_engine(db)
connection = engine.connect()

metadata = sa.MetaData()
alljoined = sa.Table('alljoined', metadata,
                     sa.Column('Analysis', sa.Text),
                     sa.Column('Type', sa.Text),
                     sa.Column('Recording', sa.Text),
                     sa.Column('Transcription', sa.Text),
                     sa.Column('Gloss', sa.Text),
                     sa.Column('Target_Tone', sa.VARCHAR(50)),
                     sa.Column('First_Syllable_Tone', sa.VARCHAR(2)),
                     sa.Column('Second_Syllable_Tone', sa.VARCHAR(2)),
                     sa.Column('Frame', sa.CHAR(3)),
                     sa.Column('Left_Frame', sa.CHAR(1)),
                     sa.Column('Right_Frame', sa.CHAR(1)),
                     sa.Column('Number_of_Syllables', sa.INT()),
                     sa.Column('Speaker_Name', sa.Text),
                     sa.Column('Speaker_Age', sa.Text),
                     sa.Column('Speaker_Gender', sa.CHAR(1))
                     )

#metadata.reflect(bind = engine, schema = 'FieldWork')

#inspector = sa.engine.reflection.Inspector.from_engine(engine)

#from_clause = metadata.tables['FieldWork.AnalysisType'].join(
              #metadata.tables['FieldWork.Analysis']).join(
              #metadata.tables['FieldWork.Utterance']).join(
              #metadata.tables['FieldWork.Sentence']).join(
              #metadata.tables['FieldWork.Speaker'])

#tables = [val for key, val in metadata.tables.iteritems()
          #if key not in ['FieldWork.Language', 'FieldWork.DataSet']]

#columns = [col for t in tables for col in t.columns
           #if not (col.name.endswith('_id') or
                   #col.name.startswith('date_'))]

