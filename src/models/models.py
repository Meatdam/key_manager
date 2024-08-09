from tortoise import fields
from tortoise.models import Model


class KeyCipher(Model):
    id = fields.IntField(pk=True)
    cipher_message = fields.CharField(max_length=500)

    additional_info: fields.OneToOneRelation["UserCipher"]

    def __str__(self):
        return f'{self.cipher_message}'


class UserCipher(Model):
    id = fields.IntField(pk=True)
    cipher_key = fields.CharField(max_length=500)
    url = fields.CharField(max_length=500)
    key_cipher_id = fields.OneToOneField(
        model_name="models.KeyCipher",
        related_name="cipher_id",
        on_delete=fields.CASCADE,)
