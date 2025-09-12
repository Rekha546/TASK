from django.db import migrations

def copy_requester_to_requested_by(apps, schema_editor):
    TopicRequest = apps.get_model('accounts', 'TopicRequest')
    for req in TopicRequest.objects.all():
        if req.requester:
            req.requested_by = req.requester
            req.save()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_requester_to_requested_by, migrations.RunPython.noop),
    ]