import sqlalchemy as sa


engine = sa.create_engine('mysql://fieldwork:7d3zXWhi#hdI@localhost')
connection = engine.connect()

metadata = sa.MetaData()
metadata.reflect(bind = engine, schema = 'FieldWork')

inspector = sa.engine.reflection.Inspector.from_engine(engine)

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

