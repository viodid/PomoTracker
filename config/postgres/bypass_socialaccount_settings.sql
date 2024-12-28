INSERT INTO socialaccount_socialapp (id, provider, name, client_id, secret, settings, key, provider_id)
VALUES (2, 'google', 'google', 1, 123, '{}', 1, 1);

INSERT INTO socialaccount_socialapp_sites (id, site_id, socialapp_id)
VALUES (1, 2, 2);
