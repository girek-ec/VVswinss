from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0005_alter_post_meta_description_de_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpageconfiguration",
            name="post_default_social_image",
            field=models.ImageField(
                blank=True,
                editable=False,
                help_text="Se genera automáticamente en JPEG 1200 × 630 desde la imagen por defecto.",
                null=True,
                upload_to="seo/defaults/blog/",
                verbose_name="Imagen social por defecto",
            ),
        ),
    ]
