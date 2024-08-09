from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "keycipher" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "cipher_message" VARCHAR(500) NOT NULL
);
CREATE TABLE IF NOT EXISTS "usercipher" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "cipher_key" VARCHAR(500) NOT NULL,
    "url" VARCHAR(500) NOT NULL,
    "key_cipher_id_id" INT NOT NULL UNIQUE REFERENCES "keycipher" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
