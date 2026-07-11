from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0001_initial"),
        ("tracking", "0002_developerapikey_allowed_ips_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="trackingsession",
            name="assigned_organizations",
            field=models.ManyToManyField(
                blank=True,
                related_name="monitored_tracking_sessions",
                to="organizations.organization",
            ),
        ),
    ]
