from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("geofencing", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="geofence",
            name="shape_type",
            field=models.CharField(
                choices=[("circle", "Circle"), ("rectangle", "Rectangle"), ("square", "Square")],
                default="circle",
                help_text="Choose a circle, rectangle, or equal-sided square boundary.",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="geofence",
            name="address",
            field=models.CharField(blank=True, help_text="Nearest building, street, locality/LGA, state, and country returned by Google Maps.", max_length=500),
        ),
        migrations.AddField(model_name="geofence", name="north_latitude", field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
        migrations.AddField(model_name="geofence", name="south_latitude", field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
        migrations.AddField(model_name="geofence", name="east_longitude", field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
        migrations.AddField(model_name="geofence", name="west_longitude", field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
        migrations.AlterField(
            model_name="geofence",
            name="radius_meters",
            field=models.PositiveIntegerField(default=250, help_text="Circle radius in meters. Rectangle and square maps update this to the center-to-corner distance."),
        ),
    ]
