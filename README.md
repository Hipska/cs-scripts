# Mailchimp DMP script

mailchimp csv export: https://docs.google.com/spreadsheets/d/1ArDqAQuEE0wLu1q6Lyayql2kSbGcnJ5LxGhmsyZp4Jo/edit?usp=sharing

## GOALS

- [x] get the export into mailchimp
- [x] overview of possible tags in mailchimp
- [x] sync mailchimp and mongo (cs)
- [ ] cron on daily basis
- [ ] keep track of changes (events) -> daily raport
- [ ] modular code -> extend to DMP in later stage

## Model

- firstname
- lastname
- email
- tags (csv)

## Caveats

### Mongo

- new added
- tages added

### Mailchimp

- user can unsubscribe
- manually added -> clean duplicates

## How-To-Run

Firstly, go to `config.py` and specify the right credentials and audience ID.

If you want to run everything in one go. Run `db_to_chimp.py` first, run `chimp_to_db.py` after that.

### tags

Returns all unique tags present in mailchimp

- `python3 tags.py`

Returns a set which contains all unique tags

### Cross-validate

Cross-validates Mailchimp and database

- `python3 cross_validate.py`

## Notes

- Wie zijn contacts in CSV maar niet in db (400)
- Backup maken mailchimp to csv

- Volledige flow simuleren in test mailchimp

## mailen naar luc

- wie zijn contacten
- verder verloop

## flow test

- nieuw contact in mailchimp
- na sync in admin dash
- unsubben in mailchimp
- na sync niet meer subbed in db
