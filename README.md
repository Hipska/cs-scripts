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

### DB to Mailchimp

Retrieves all unique email addresses from both matches and plekjes from the database, compares them with mailchimp and adds new unique ones to mailchimp

- `python3 db_to_chimp.py`

Returns nothing, but will print out these statistics:

```
Encountered 0 new subscribers and added them to mailchimp
Encountered 312 subscribers that were already in the database
Encountered 0 errors
```

### Mailchimp to db

Retrieves all email addresses from mailchimp and compares them to the email database. Ignores duplicates, adds unknown ones to the database and updates ones that have changes.

- `python3 chimp_to_db.py`

Returns nothing, but will print out these statistics:

```
Encountered 303 emails that were already stored and had no changes
Encountered 0 emails that had changes, updated them
Encountered 0 new emails, added them
```
