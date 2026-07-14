from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("notifications", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="scope",
            field=models.CharField(choices=[("system", "System"), ("safety", "Safety"), ("tracking", "Tracking"), ("emergency", "Emergency"), ("account", "Account")], default="system", help_text="Controls how the app categorizes and visually prioritizes this message.", max_length=30),
        ),
        migrations.AddField(model_name="notification", name="show_as_popup", field=models.BooleanField(default=True, help_text="Show this message as an in-app dialog the next time the recipient is active.")),
        migrations.AddField(model_name="notification", name="read_at", field=models.DateTimeField(blank=True, null=True)),
        migrations.AlterField(model_name="notification", name="payload", field=models.JSONField(blank=True, default=dict, help_text='Optional JSON such as {"type":"route.alert","session_id":12,"action_url":"/live-map"}. Never include passwords or secrets.')),
    ]
