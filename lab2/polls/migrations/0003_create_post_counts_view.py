from django.db import migrations

SQL_CREATE_VIEW = """
CREATE VIEW IF NOT EXISTS polls_post_counts AS
SELECT p.author_id AS person_id, COUNT(p.id) AS total_posts
FROM polls_post p
GROUP BY p.author_id;
"""

SQL_DROP_VIEW = """
DROP VIEW IF EXISTS polls_post_counts;
"""

class Migration(migrations.Migration):
    dependencies = [
        ('polls', '0002_alter_category_options_alter_person_email_and_more'),
    ]

    operations = [
        migrations.RunSQL(SQL_CREATE_VIEW, SQL_DROP_VIEW),
    ]
